"""Fungsi pembersihan teks untuk QueryLens."""

from __future__ import annotations

import math
import re

import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
STOP_WORDS = set(stopwords.words("english"))


def clean_text(text):
    """Membersihkan kalimat dengan menghapus angka, tanda baca, dan stopword."""
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
    lowered = re.sub(r"[^a-z\s]", " ", lowered)
    tokens = lowered.split()
    tokens = [token for token in tokens if token and token not in STOP_WORDS]
    return " ".join(tokens)
