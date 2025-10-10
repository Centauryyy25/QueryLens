/* global fetch */

const API_BASE = ""; // same origin

const PLACEHOLDER_SVG = `data:image/svg+xml;base64,${btoa(`
<svg xmlns='http://www.w3.org/2000/svg' width='320' height='200'>
  <defs>
    <linearGradient id='g' x1='0%' y1='0%' x2='100%' y2='100%'>
      <stop offset='0%' stop-color='#312e81' stop-opacity='0.85'/>
      <stop offset='100%' stop-color='#0f172a' stop-opacity='0.9'/>
    </linearGradient>
  </defs>
  <rect width='320' height='200' fill='url(#g)' rx='24' ry='24'/>
  <text x='50%' y='52%' dominant-baseline='middle' text-anchor='middle'
        font-family='Segoe UI, Arial' font-size='28' fill='white' opacity='0.85'>QueryLens</text>
  </svg>`)}
`;

const el = {
  query: document.getElementById("query"),
  searchBtn: document.getElementById("searchBtn"),
  results: document.getElementById("results"),
};

function escapeHtml(str) {
  return str
    .replaceAll(/&/g, "&amp;")
    .replaceAll(/</g, "&lt;")
    .replaceAll(/>/g, "&gt;")
    .replaceAll(/"/g, "&quot;")
    .replaceAll(/'/g, "&#039;");
}

function highlight(text, query) {
  const q = query.trim();
  if (!q) return escapeHtml(text);
  const pattern = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "ig");
  return escapeHtml(text).replace(pattern, (m) => `<mark>${m}</mark>`);
}

function renderResults(items, query) {
  if (!items || items.length === 0) {
    el.results.innerHTML = `<div class="panel" style="text-align:center;color:var(--muted)">Tidak ada hasil.</div>`;
    return;
  }
  el.results.innerHTML = items.map((it) => {
    const img = it.image_url && it.image_url.startsWith("http") ? it.image_url : PLACEHOLDER_SVG;
    const url = it.url && it.url.startsWith("http") ? it.url : "";
    const metaSpans = [
      `Skor relevansi: ${Number(it.score).toFixed(3)}`,
      it.published_at ? `Terbit: ${escapeHtml(it.published_at)}` : null,
    ].filter(Boolean).map((s) => `<span>${s}</span>`).join("");
    return `
      <article class="result-card">
        <div class="result-card__media">
          <img src="${img}" alt="Thumbnail artikel" loading="lazy" onerror="this.src='${PLACEHOLDER_SVG}'" />
        </div>
        <div class="result-card__body">
          <div class="result-card__badge">${escapeHtml(it.category || "Unknown")}</div>
          <h3 class="result-card__title">${escapeHtml(it.title || "Tanpa judul")}</h3>
          <div class="result-card__snippet">${highlight(it.text || "", query)}</div>
          <div class="result-card__meta">${metaSpans}</div>
          <div class="result-card__actions">${url ? `<a class="result-card__button" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">Buka Artikel</a>` : ""}</div>
        </div>
      </article>`;
  }).join("");
}

async function doSearch() {
  const query = el.query.value.trim();
  if (!query) {
    el.results.innerHTML = `<div class="panel" style="text-align:center;color:var(--muted)">Masukkan kata kunci.</div>`;
    return;
  }
  el.searchBtn.disabled = true;
  el.searchBtn.textContent = "Mencari...";
  try {
    const res = await fetch(`${API_BASE}/api/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: 5 })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    const data = await res.json();
    renderResults(data, query);
  } catch (e) {
    el.results.innerHTML = `<div class="panel" style="color:#fecaca;border-color:#fecaca">Terjadi kesalahan: ${escapeHtml(String(e.message || e))}</div>`;
  } finally {
    el.searchBtn.disabled = false;
    el.searchBtn.textContent = "Cari";
  }
}

el.searchBtn.addEventListener("click", doSearch);
el.query.addEventListener("keydown", (e) => { if (e.key === "Enter") doSearch(); });
