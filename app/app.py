import re

import streamlit as st

from search_engine import SearchEngine

DATASET_PATH = "Dataset/NewsArticelAll_Enchant.xlsx"
DEFAULT_TOP_K = 5
MAX_TOP_K = 20

st.set_page_config(page_title="QueryLens - News Search Engine")
st.title("QueryLens - News Search Engine")


@st.cache_resource(show_spinner=False)
def load_engine() -> SearchEngine:
    return SearchEngine(DATASET_PATH)


search_engine = load_engine()
available_categories = ["All"] + search_engine.get_categories()

selected_category = st.selectbox("Pilih kategori:", available_categories)
top_k = st.slider("Jumlah hasil ditampilkan:", min_value=1, max_value=MAX_TOP_K, value=DEFAULT_TOP_K)
query = st.text_input("Masukkan kata kunci:")

if st.button("Cari") and query:
    results = search_engine.search(query, top_k=top_k, category=selected_category)
    st.subheader("Hasil Pencarian:")

    if not results:
        st.info("Tidak ada hasil yang cocok untuk pencarian ini.")
    else:
        relevant = sum(1 for item in results if selected_category in ("All", item["category"]))
        precision_at_k = relevant / len(results)

        for item in results:
            snippet = item["text"] or ""
            if snippet:
                pattern = re.compile(re.escape(query), re.IGNORECASE)
                snippet = pattern.sub(lambda match: f"<mark>{match.group(0)}</mark>", snippet)
            st.markdown(f"### {item['title']} ({item['category']})")
            if item.get("published_at"):
                st.caption(item["published_at"])
            st.markdown(snippet if snippet else "_Ringkasan tidak tersedia._", unsafe_allow_html=True)
            if item.get("url"):
                st.markdown(f"[Baca selengkapnya]({item['url']})")
            st.caption(f"Relevansi skor: {item['score']}")
            st.write("---")

        st.metric(label=f"Precision@{len(results)}", value=f"{precision_at_k:.2f}")
else:
    st.caption("Masukkan kata kunci kemudian tekan tombol Cari untuk memulai pencarian.")
