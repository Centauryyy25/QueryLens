import os
from typing import Dict, List, Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import clean_text


class SearchEngine:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self.df = self._load_dataset(data_path)
        self._prepare_dataframe()
        self.vectorizer = TfidfVectorizer()
        self.doc_vectors = self.vectorizer.fit_transform(self.df["clean_text"])

    def _load_dataset(self, data_path: str) -> pd.DataFrame:
        ext = os.path.splitext(data_path)[1].lower()
        if ext == ".csv":
            return pd.read_csv(data_path)
        if ext in {".xlsx", ".xls"}:
            try:
                return pd.read_excel(data_path)
            except ImportError as exc:
                raise ImportError(
                    "Loading Excel datasets requires openpyxl. Install it with `pip install openpyxl`."
                ) from exc
        raise ValueError(f"Unsupported dataset format: {ext}")

    def _prepare_dataframe(self) -> None:
        text_columns = [col for col in ("full_content", "content", "description", "title") if col in self.df.columns]
        if not text_columns:
            raise ValueError(
                "Dataset must contain at least one of the following columns: full_content, content, description, title."
            )

        self.df[text_columns] = self.df[text_columns].fillna("").astype(str)
        self.df[text_columns] = self.df[text_columns].applymap(str.strip)

        self.df["raw_text"] = self.df.apply(
            lambda row: " ".join(value for value in (row[col] for col in text_columns) if value),
            axis=1,
        )

        self.df["clean_text"] = self.df["raw_text"].apply(clean_text)
        self.df["snippet"] = self.df["raw_text"].str.slice(0, 500)

        if "category" in self.df.columns:
            self.df["category"] = self.df["category"].fillna("Unknown").astype(str).str.strip()
            self.df.loc[self.df["category"] == "", "category"] = "Unknown"
        else:
            self.df["category"] = "Unknown"

        if "title" in self.df.columns:
            self.df["title"] = self.df["title"].fillna("").astype(str).str.strip()
            missing_title = self.df["title"] == ""
            self.df.loc[missing_title, "title"] = self.df.loc[missing_title, "snippet"].str.slice(0, 80)
        else:
            self.df["title"] = self.df["snippet"].str.slice(0, 80)

        if "published_at" in self.df.columns:
            published = pd.to_datetime(self.df["published_at"], errors="coerce")
            self.df["published_at_display"] = published.dt.strftime("%Y-%m-%d %H:%M").fillna("")
        else:
            self.df["published_at_display"] = ""

        if "url" in self.df.columns:
            self.df["url"] = self.df["url"].fillna("").astype(str).str.strip()
        else:
            self.df["url"] = ""

        self.df = self.df[self.df["clean_text"] != ""].reset_index(drop=True)

    def get_categories(self) -> List[str]:
        categories = sorted({value for value in self.df["category"] if value})
        return categories

    def search(self, query: str, top_k: int = 5, category: Optional[str] = None) -> List[Dict[str, str]]:
        if not query:
            return []

        query_clean = clean_text(query)
        if not query_clean:
            return []

        query_vector = self.vectorizer.transform([query_clean])
        similarities_all = cosine_similarity(query_vector, self.doc_vectors).flatten()

        if category and category != "All":
            mask = self.df["category"] == category
            if not mask.any():
                return []
            doc_indices = list(self.df[mask].index)
            similarities = similarities_all[mask.to_numpy()]
        else:
            doc_indices = list(self.df.index)
            similarities = similarities_all

        if not doc_indices:
            return []

        top_k = min(top_k, len(doc_indices))
        ranked_positions = similarities.argsort()[::-1][:top_k]

        results = []
        for position in ranked_positions:
            score = float(similarities[position])
            if score <= 0:
                continue
            idx = doc_indices[position]
            row = self.df.loc[idx]
            results.append(
                {
                    "title": row["title"],
                    "category": row["category"],
                    "text": row["snippet"],
                    "score": round(score, 3),
                    "url": row["url"],
                    "published_at": row["published_at_display"],
                }
            )
        return results
