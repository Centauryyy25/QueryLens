# 🔎 QueryLens : Mini Search Engine Buat News Articles  

Project ini adalah **sistem pencarian dokumen** simpel yang dibangun pakai **TF-IDF** + **Cosine Similarity**, terus di-bungkus jadi web app dengan **Streamlit**.  
Intinya: dari data teks mentah → jadi search engine mini yang interaktif. 🔥  

---

## 🚀 Fitur Utama  
- **Keyword Search** → Ketik query, dapet artikel paling relevan.  
- **Category Filter** → Bisa pilih kategori berita (Business, Politics, Sport, Tech, Entertainment).  
- **Highlight Result** → Kata kunci otomatis di-highlight.  
- **Custom Top-K** → Atur jumlah hasil (Top-5, Top-10, dst).  
- **Precision@K** → Metode evaluasi simpel biar lebih *machine learning vibe*.  

---

## 🛠️ Tech Stack  
- **Bahasa**: Python 3.9+  
- **Library**:  
  - [scikit-learn](https://scikit-learn.org/stable/) → TF-IDF + Cosine Similarity  
  - [pandas](https://pandas.pydata.org/) → Data wrangling  
  - [NLTK](https://www.nltk.org/) → Preprocessing teks  
  - [Streamlit](https://streamlit.io/) → Web interface (frontend + backend langsung jadi)  

---

## 📂 Struktur Project  
```
QueryLens/
├── Dataset/
│ └── bbc_news.csv # Dataset (hasil konversi dari .txt ke .csv)
│
├── app/
│ ├── app.py # Streamlit app utama
│ ├── preprocessing.py # Preprocessing teks
│ └── search_engine.py # Core TF-IDF + Cosine Similarity
│
├── requirements.txt # Dependency Python
└── README.md # Dokumentasi project
```
---

## 📊 Dataset  
- Source: **[BBC News Dataset (Kaggle)](https://www.kaggle.com/datasets/pariza/bbc-news-summary)**  
- Udah diproses jadi CSV dengan field:  
  - `title` → judul artikel (atau kalimat pertama)  
  - `category` → kategori berita  
  - `text` → isi artikel lengkap  

---

## 💻 Cara Jalanin Lokal  
1. Clone repo ini  
   ```bash
   git clone https://github.com/Centauryyy25/QueryLens.git
   cd QueryLens

---
```
👤 Author
===
Created by Ilham Ahsan Saputra
🎓 Informatics Student
💻 Junior Network Engineer | AI & ML Enthusiast

📌 “Turning raw data into meaningful insights through Machine Learning.”
```
