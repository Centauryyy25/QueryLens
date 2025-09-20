import streamlit as st
import re
from search_engine import SearchEngine

st.title("🔎 Mini Search Engine - BBC News")

# Load Search Engine
search_engine = SearchEngine("Dataset/bbc_news.csv")

# 🔹 Fitur 1: Filter kategori
categories = ["All"] + sorted(search_engine.df['category'].unique())
selected_category = st.selectbox("Pilih kategori:", categories)

# 🔹 Fitur 2: Slider top-k hasil
top_k = st.slider("Jumlah hasil ditampilkan:", 1, 20, 5)

# Input query
query = st.text_input("Masukkan kata kunci:")

if st.button("Cari") and query:
    results = search_engine.search(query, top_k=top_k, category=selected_category)

    st.subheader("Hasil Pencarian:")

    # 🔹 Evaluasi sederhana: precision@k (berapa banyak hasil dari kategori yg sesuai query)
    relevant = sum(1 for r in results if selected_category in ["All", r['category']])
    precision_at_k = relevant / len(results) if results else 0

    for r in results:
        # 🔹 Fitur 3: Highlight keyword
        pattern = re.compile(f"({query})", re.IGNORECASE)
        highlighted_text = pattern.sub(r"<mark>\1</mark>", r['text'])

        st.markdown(f"### {r['title']} ({r['category']})")
        st.markdown(highlighted_text, unsafe_allow_html=True)
        st.caption(f"Relevansi skor: {r['score']}")
        st.write("---")

    # 🔹 Fitur 4: Tampilkan evaluasi sederhana
    st.metric(label=f"Precision@{top_k}", value=f"{precision_at_k:.2f}")
