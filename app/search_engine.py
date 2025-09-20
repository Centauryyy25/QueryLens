import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import clean_text

class SearchEngine:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df['clean_text'] = self.df['text'].apply(clean_text)

        self.vectorizer = TfidfVectorizer()
        self.doc_vectors = self.vectorizer.fit_transform(self.df['clean_text'])

    def search(self, query, top_k=5, category=None):
        query_clean = clean_text(query)
        query_vector = self.vectorizer.transform([query_clean])

        similarities = cosine_similarity(query_vector, self.doc_vectors).flatten()

        # filter by category (jika dipilih user)
        if category and category != "All":
            mask = self.df['category'] == category
            indices = self.df[mask].index
            similarities = similarities[indices]
            doc_indices = indices
        else:
            doc_indices = self.df.index

        top_indices = similarities.argsort()[-top_k:][::-1]
        results = []
        for i in top_indices:
            idx = doc_indices[i]
            results.append({
                "title": self.df.iloc[idx]['title'],
                "category": self.df.iloc[idx]['category'],
                "text": self.df.iloc[idx]['text'][:400] + "...",
                "score": round(similarities[i], 3)
            })
        return results
