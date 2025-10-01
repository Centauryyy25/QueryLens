"""Antarmuka pengguna Streamlit untuk aplikasi QueryLens."""

from __future__ import annotations

import html
import re
from typing import Iterable, Mapping

import streamlit as st

from search_engine import SearchEngine

DATASET_PATH = "Dataset/NewsArticelAll_Enchant.xlsx"
DEFAULT_TOP_K = 5
MAX_TOP_K = 20
IMAGE_PLACEHOLDER = "https://via.placeholder.com/320x200?text=QueryLens"

st.set_page_config(page_title="QueryLens - News Search Engine")
st.title("QueryLens - News Search Engine")


def inject_global_css() -> None:
    """Menambahkan gaya glassmorphism untuk tampilan kartu hasil."""
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;} /* Navbar pojok kanan atas */
        footer {visibility: hidden;}   /* Footer "Made with Streamlit" */
        header {visibility: hidden;}   /* Header Streamlit default */
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at 10% 20%, rgba(76, 29, 149, 0.35), transparent 55%),
                        radial-gradient(circle at 90% 10%, rgba(14, 116, 144, 0.3), transparent 45%),
                        radial-gradient(circle at 50% 80%, rgba(2, 132, 199, 0.25), transparent 40%),
                        #0f172a;
            color: #e2e8f0;
        }
        .result-card {
            display: grid;
            grid-template-columns: minmax(200px, 260px) 1fr;
            gap: 1.5rem;
            margin-bottom: 1.75rem;
            padding: 1.5rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 12px 40px rgba(15, 23, 42, 0.55);
            backdrop-filter: blur(18px) saturate(140%);
        }
        .result-card:hover {
            border-color: rgba(255, 255, 255, 0.25);
            transform: translateY(-3px);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .result-card__media img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }
        .result-card__badge {
            display: inline-flex;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            letter-spacing: 0.04em;
            background: rgba(56, 189, 248, 0.2);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #bae6fd;
            text-transform: uppercase;
        }
        .result-card__title {
            margin: 0.5rem 0 0.75rem;
            font-size: 1.35rem;
            color: #f8fafc;
        }
        .result-card__snippet {
            font-size: 0.95rem;
            line-height: 1.55rem;
            color: rgba(248, 250, 252, 0.85);
            margin-bottom: 1.15rem;
        }
        .result-card__snippet mark {
            background: rgba(244, 114, 182, 0.35);
            color: inherit;
            padding: 0 0.2rem;
            border-radius: 0.3rem;
        }
        .result-card__meta {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            font-size: 0.85rem;
            color: rgba(226, 232, 240, 0.7);
            margin-bottom: 1rem;
        }
        .result-card__meta span {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }
        .result-card__button {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.55rem 1.2rem;
            border-radius: 999px;
            border: 1px solid rgba(244, 114, 182, 0.45);
            background: linear-gradient(120deg, rgba(244, 114, 182, 0.3), rgba(59, 130, 246, 0.3));
            color: #fdf4ff;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .result-card__button:hover {
            transform: translateY(-2px);
            border-color: rgba(244, 114, 182, 0.75);
        }
        @media (max-width: 900px) {
            .result-card {
                grid-template-columns: 1fr;
            }
            .result-card__media img {
                height: 220px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def highlight_query(snippet: str, query: str) -> str:
    """Menyorot kemunculan kata kunci agar pengguna mudah menemukan konteks."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda match: f"<mark>{match.group(0)}</mark>", snippet)


@st.cache_resource(show_spinner=False)
def load_engine() -> SearchEngine:
    """Memuat mesin pencari hanya sekali untuk menghemat waktu respon Streamlit."""
    return SearchEngine(DATASET_PATH)


def render_result(items: Iterable[Mapping[str, str]], query: str) -> None:
    """Menampilkan daftar hasil pencarian dengan format yang ramah pengguna."""
    for item in items:
        title = html.escape(item["title"])
        category = html.escape(item["category"])
        url = item.get("url") or ""
        url_html = (
            f'<a class="result-card__button" href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">Buka Artikel</a>'
            if url
            else ""
        )
        image_url = item.get("image_url") or IMAGE_PLACEHOLDER
        snippet_raw = item.get("text") or ""
        snippet_html = "<em>Ringkasan tidak tersedia.</em>"
        if snippet_raw:
            escaped_snippet = html.escape(snippet_raw)
            snippet_html = highlight_query(escaped_snippet, query)

        meta_segments = [f"Skor relevansi: {item['score']:.3f}"]
        published = item.get("published_at") or ""
        if published:
            meta_segments.append(f"Terbit: {html.escape(published)}")
        meta_html = "".join(f"<span>{segment}</span>" for segment in meta_segments)

        card_html = f"""
        <div class="result-card">
            <div class="result-card__media">
                <img src="{html.escape(image_url)}" alt="Thumbnail artikel" loading="lazy" onerror="this.src='{IMAGE_PLACEHOLDER}'" />
            </div>
            <div class="result-card__body">
                <div class="result-card__badge">{category}</div>
                <h3 class="result-card__title">{title}</h3>
                <div class="result-card__snippet">{snippet_html}</div>
                <div class="result-card__meta">{meta_html}</div>
                <div class="result-card__actions">{url_html}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)


inject_global_css()

search_engine = load_engine()
available_categories = ["All"] + search_engine.get_categories()

selected_category = st.selectbox("Pilih kategori:", available_categories)
top_k = st.slider(
    "Jumlah hasil ditampilkan:",
    min_value=1,
    max_value=MAX_TOP_K,
    value=DEFAULT_TOP_K,
)
query = st.text_input("Masukkan kata kunci:")

if st.button("Cari") and query:
    results = search_engine.search(query, top_k=top_k, category=selected_category)
    st.subheader("Hasil Pencarian:")

    if not results:
        st.info("Tidak ada hasil yang cocok untuk pencarian ini.")
    else:
        render_result(results, query)
        relevant = sum(1 for item in results if selected_category in ("All", item["category"]))
        precision_at_k = relevant / len(results)
        st.metric(label=f"Precision@{len(results)}", value=f"{precision_at_k:.2f}")
else:
    st.caption("Masukkan kata kunci kemudian tekan tombol Cari untuk memulai pencarian.")
