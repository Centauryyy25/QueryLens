"""FastAPI backend for QueryLens.

Menyediakan endpoint untuk mengambil kategori dan melakukan pencarian.
Juga menyajikan frontend statis dari folder `web/` pada root repository.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .search_engine import SearchEngine, SearchResult


BASE_DIR = Path(__file__).resolve().parents[1]
# Bisa dioverride via env var QUERYLENS_DATASET
DATASET_PATH = Path(os.getenv("QUERYLENS_DATASET", str(BASE_DIR / "Dataset" / "NewsArticelAll_Enchant.xlsx")))
STATIC_DIR = BASE_DIR / "web"


class SearchRequest(BaseModel):
    """Payload permintaan pencarian dari klien."""

    query: str = Field(min_length=1, description="Kata kunci pencarian")
    top_k: int = Field(default=5, ge=1, le=50, description="Jumlah hasil dikembalikan")
    category: Optional[str] = Field(default=None, description="Filter kategori atau 'All'")


class SearchItem(BaseModel):
    """Representasi hasil individual ke klien (JSON)."""

    title: str
    category: str
    text: str
    score: float
    url: str
    published_at: str
    image_url: str


class CategoriesResponse(BaseModel):
    """Daftar kategori unik (termasuk 'All' di posisi awal)."""

    categories: List[str]


def create_app() -> FastAPI:
    app = FastAPI(title="QueryLens API", version="1.0.0")

    # CORS: long‑term you can tighten this (e.g., specific origins)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Load search engine once for the app lifetime
    if not DATASET_PATH.exists():
        raise RuntimeError(f"Dataset tidak ditemukan: {DATASET_PATH}")
    engine = SearchEngine(str(DATASET_PATH))

    @app.get("/api/categories", response_model=CategoriesResponse)
    def get_categories() -> CategoriesResponse:
        cats = ["All"] + engine.get_categories()
        return CategoriesResponse(categories=cats)

    @app.post("/api/search", response_model=List[SearchItem])
    def search(req: SearchRequest) -> List[SearchItem]:
        category = None if (req.category in (None, "", "All")) else req.category
        try:
            results = engine.search(req.query, top_k=req.top_k, category=category)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return [
            SearchItem(
                title=item.title,
                category=item.category,
                text=item.text,
                score=item.score,
                url=item.url,
                published_at=item.published_at,
                image_url=item.image_url,
            )
            for item in results
        ]

    @app.get("/api/health")
    def health() -> dict:
        return {"status": "ok", "documents": int(engine.df.shape[0])}

    # Serve static frontend if present
    if STATIC_DIR.exists():
        app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="web")

    return app


app = create_app()
