"""Utility pembersihan teks untuk QueryLens.

Berisi fungsi `clean_text` yang menormalkan input menjadi huruf kecil,
menghapus karakter non-huruf, memangkas spasi berlebih, dan menghapus stopword.
Fungsi ini aman terhadap input `None`, angka NaN, dan tipe non-string.
"""

from __future__ import annotations

from typing import Any
import math
import re
import warnings

try:
    import nltk
    from nltk.corpus import stopwords as nltk_stopwords
    # Upaya diam‑diam untuk memastikan stopwords tersedia.
    try:
        nltk.download("stopwords", quiet=True)
    except Exception:
        pass
    try:
        STOP_WORDS = set(nltk_stopwords.words("english"))
    except Exception as exc:  # pragma: no cover - bergantung lingkungan
        warnings.warn(
            f"Gagal memuat NLTK stopwords ({exc}); melanjutkan tanpa stopwords.",
            RuntimeWarning,
        )
        STOP_WORDS = set()
except Exception as exc:  # pragma: no cover - bergantung lingkungan
    warnings.warn(
        f"NLTK tidak tersedia ({exc}); melanjutkan tanpa stopwords.", RuntimeWarning
    )
    STOP_WORDS = set()


_NON_LETTER_RE = re.compile(r"[^a-z\s]")

__all__ = ["clean_text"]


def clean_text(text: Any) -> str:
    """Bersihkan teks mentah menjadi string siap‑vectorizer.

    - Mengubah ke string dan trim spasi.
    - Mengubah ke huruf kecil, menghapus karakter bukan a–z.
    - Menghapus token kosong dan stopword Inggris.

    Parameter
    ---------
    text: Any
        Input apa pun (string, angka, None). Non‑string akan di-cast ke string.

    Returns
    -------
    str
        Teks yang sudah dinormalisasi. Bisa menjadi string kosong jika tidak valid.
    """
    if text is None:
        return ""
    if isinstance(text, float) and math.isnan(text):
        return ""
    if not isinstance(text, str):
        text = str(text)

    text = text.strip()
    if not text:
        return ""

    lowered = text.lower()
    if lowered in {"nan", "nat", "none"}:
        return ""

    lowered = _NON_LETTER_RE.sub(" ", lowered)
    tokens = (tok for tok in lowered.split() if tok)
    cleaned = [tok for tok in tokens if tok not in STOP_WORDS]
    return " ".join(cleaned)
