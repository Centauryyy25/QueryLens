QueryLens UI Migration (Streamlit ➜ Static HTML + FastAPI)
=========================================================

Overview
--------
- UI dipindahkan dari Streamlit (`app/app.py`) ke frontend statis yang berada di folder `web/`.
- Backend menggunakan FastAPI pada `app/api.py`, memaparkan endpoint:
  - GET `/api/categories`
  - POST `/api/search` (body JSON: `{ query, top_k, category }`)
- Static frontend disajikan langsung oleh FastAPI pada root path (`/`).

Cara Menjalankan
----------------
1) Install dependency
```
pip install -r requirements.txt
```
2) Jalankan server (serve API dan UI statis)
```
uvicorn app.api:app --reload
```
3) Buka UI: `http://127.0.0.1:8000`
4) API Docs (Swagger): `http://127.0.0.1:8000/docs`

Struktur Relevan
----------------
```
app/
  api.py           # FastAPI: endpoint API + mount static
  search_engine.py # Logika mesin pencari (reuse)
  preprocessing.py # Util pembersihan teks (reuse)

web/
  index.html       # Frontend utama
  styles.css       # Stylesheet
  app.js           # Fetch API + render hasil
```

Catatan Migrasi
---------------
- Dependensi `streamlit` tidak lagi diperlukan dan sudah dihapus dari `requirements.txt`.
- Dataset default tetap: `Dataset/NewsArticelAll_Enchant.xlsx`. Pastikan file tersedia.
- Endpoint mengembalikan field yang sama dengan hasil `SearchEngine.search` agar kompatibel.

