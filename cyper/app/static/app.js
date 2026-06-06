const q = document.getElementById("q");
const results = document.getElementById("results");
const statusEl = document.getElementById("status");
let timer = null;

function escapeHtml(s) {
  return s.replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

function render(data) {
  if (!data.results.length) { results.innerHTML = "<p>No matches.</p>"; return; }
  results.innerHTML = data.results.map(r => {
    const cite = r.type === "guide"
      ? `Study guide · ${escapeHtml(r.title)}`
      : `${escapeHtml(r.file)} · p.${r.page}`;
    // r.html is sanitized server-side (bleach); r.text is plain and escaped here.
    const body = r.html ? r.html : `<p>${escapeHtml(r.text)}</p>`;
    return `<div class="result">
      <div class="meta">
        <span class="badge ${r.type}">${r.type}</span>
        <span>${escapeHtml(r.topic)}</span>
        <span>${cite}</span>
        <span class="score">sim ${r.score}</span>
      </div>
      <div class="body">${body}</div>
    </div>`;
  }).join("");
}

async function run() {
  const term = q.value.trim();
  if (term.length < 2) { results.innerHTML = ""; statusEl.textContent = ""; return; }
  statusEl.textContent = "Searching…";
  try {
    const res = await fetch(`/search?q=${encodeURIComponent(term)}&k=6`);
    const data = await res.json();
    statusEl.textContent = `${data.results.length} results for "${term}"`;
    render(data);
  } catch (e) {
    statusEl.textContent = "Error: " + e.message;
  }
}

q.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(run, 220); });
q.addEventListener("keydown", e => { if (e.key === "Enter") { clearTimeout(timer); run(); } });
