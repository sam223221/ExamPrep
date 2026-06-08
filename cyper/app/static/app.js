const q = document.getElementById("q");
const results = document.getElementById("results");
const statusEl = document.getElementById("status");
const typeChips = document.getElementById("typeChips");
const diffChips = document.getElementById("diffChips");
let timer = null;

const state = { type: "", diff: "" };

function escapeHtml(s) {
  return s.replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

function diffLabel(d) {
  return { easy: "Easy", medium: "Medium", hard: "Hard", "very-hard": "Very hard" }[d] || d;
}

function render(data) {
  if (!data.results.length) { results.innerHTML = "<p>No matches.</p>"; return; }
  results.innerHTML = data.results.map(r => {
    let cite;
    if (r.type === "guide") cite = `Study guide · ${escapeHtml(r.title)}`;
    else if (r.type === "qna") cite = `Simulated Q&A · ${escapeHtml(r.topic)}`;
    else if (r.type === "cmd") cite = `Command/Code · ${escapeHtml(r.topic)}`;
    else cite = `${escapeHtml(r.file)} · p.${r.page}`;
    const diffBadge = (r.type === "qna" && r.difficulty)
      ? `<span class="badge diff diff-${escapeHtml(r.difficulty)}">${escapeHtml(diffLabel(r.difficulty))}</span>`
      : "";
    // r.html is sanitized server-side (bleach); r.text is plain and escaped here.
    const body = r.html ? r.html : `<p>${escapeHtml(r.text)}</p>`;
    return `<div class="result">
      <div class="meta">
        <span class="badge ${r.type}">${r.type}</span>
        ${diffBadge}
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
  let url = `/search?q=${encodeURIComponent(term)}&k=6`;
  if (state.type) url += `&type=${encodeURIComponent(state.type)}`;
  if (state.type === "qna" && state.diff) url += `&difficulty=${encodeURIComponent(state.diff)}`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    const scope = state.type ? ` in ${state.type}${state.diff ? "/" + diffLabel(state.diff) : ""}` : "";
    statusEl.textContent = `${data.results.length} results for "${term}"${scope}`;
    render(data);
  } catch (e) {
    statusEl.textContent = "Error: " + e.message;
  }
}

function setActive(group, btn) {
  group.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
  btn.classList.add("active");
}

typeChips.addEventListener("click", e => {
  const btn = e.target.closest(".chip");
  if (!btn) return;
  state.type = btn.dataset.type;
  setActive(typeChips, btn);
  // difficulty row only applies to Q&A
  const showDiff = state.type === "qna";
  diffChips.hidden = !showDiff;
  if (!showDiff) {
    state.diff = "";
    setActive(diffChips, diffChips.querySelector('[data-diff=""]'));
  }
  run();
});

diffChips.addEventListener("click", e => {
  const btn = e.target.closest(".chip");
  if (!btn) return;
  state.diff = btn.dataset.diff;
  setActive(diffChips, btn);
  run();
});

q.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(run, 220); });
q.addEventListener("keydown", e => { if (e.key === "Enter") { clearTimeout(timer); run(); } });
