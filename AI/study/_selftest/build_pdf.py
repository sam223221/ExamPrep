# -*- coding: utf-8 -*-
"""Build the AI self-test HTML (questions + answer key) with rendered figures."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon, Rectangle
import numpy as np
import io, base64, json, html, re, os

DATA = os.path.join(os.path.dirname(__file__), "data")
OUT_HTML = os.path.join(os.path.dirname(__file__), "AI-Self-Test.html")

ORDER = ["L02", "L03", "L05", "L06", "L07", "L09a", "L09b", "L10", "L11", "L12"]
TITLES = {
    "L02": "L02 — Agents", "L03": "L03 — Uninformed Search", "L05": "L05 — Local Search",
    "L06": "L06 — Adversarial Search", "L07": "L07 — Constraint Satisfaction (CSP)",
    "L09a": "L09a — Bayesian Networks", "L09b": "L09b — Hidden Markov Models",
    "L10": "L10 — Intro to Machine Learning", "L11": "L11 — Regression", "L12": "L12 — Clustering",
}
EDGE = "#475569"; INK = "#0f172a"; ACCENT = "#be123c"

def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

# ---------- figure renderers ----------
def render_graph(s):
    nodes, edges = s["nodes"], s["edges"]
    directed = s.get("directed", True); orient = s.get("orientation", "LR")
    layers = {}
    for nd in nodes: layers.setdefault(nd.get("layer", 0), []).append(nd["id"])
    maxw = max(0.30 * len(nd["id"]) + 0.55 for nd in nodes)
    if orient == "TB":
        Ngap = max(2.4, maxw + 0.9); Lgap = 3.0
    else:
        Ngap = 2.4; Lgap = max(3.6, maxw + 1.3)
    pos = {}
    for L, ids in layers.items():
        k = len(ids)
        for i, nid in enumerate(ids):
            spread = (i - (k - 1) / 2) * Ngap
            pos[nid] = (L * Lgap, spread) if orient == "LR" else (spread, -L * Lgap)
    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    npatch = {}
    for nd in nodes:
        nid = nd["id"]; x, y = pos[nid]; hl = nd.get("highlight")
        fc = "#dcfce7" if hl == "goal" else ("#fef9c3" if hl == "start" else "#eef2ff")
        ec = "#15803d" if hl == "goal" else ("#b45309" if hl == "start" else "#1e293b")
        w = max(0.85, 0.30 * len(nid) + 0.55); h = 0.85
        box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                             boxstyle="round,pad=0.06,rounding_size=0.16",
                             fc=fc, ec=ec, lw=2, zorder=3)
        ax.add_patch(box); npatch[nid] = box
        ax.text(x, y, nid, ha="center", va="center", fontsize=10.5, fontweight="bold", color=INK, zorder=4)
    pairs = {(e["from"], e["to"]) for e in edges}
    for e in edges:
        u, v, lab = e["from"], e["to"], e.get("label")
        if u == v:
            x, y = pos[u]; ytop = y + 0.45
            ax.annotate("", xy=(x + 0.34, ytop), xytext=(x - 0.34, ytop),
                        arrowprops=dict(arrowstyle="-|>" if directed else "-", color=EDGE, lw=1.8,
                                        connectionstyle="arc3,rad=-2.6", mutation_scale=13, shrinkA=0, shrinkB=0))
            if lab: ax.text(x, y + 1.7, lab, ha="center", va="center", fontsize=9, color=ACCENT, fontweight="bold")
            continue
        rad = 0.18 if (v, u) in pairs else 0.0
        arr = FancyArrowPatch(pos[u], pos[v], connectionstyle=f"arc3,rad={rad}",
                              arrowstyle="-|>" if directed else "-", mutation_scale=16, color=EDGE, lw=1.8,
                              patchA=npatch[u], patchB=npatch[v], shrinkA=1, shrinkB=1, zorder=2)
        ax.add_patch(arr)
        if lab:
            mx, my = (pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2
            dx, dy = pos[v][0] - pos[u][0], pos[v][1] - pos[u][1]
            Ln = (dx * dx + dy * dy) ** 0.5 or 1
            ox, oy = -dy / Ln, dx / Ln; off = 0.4 + (0.55 if rad else 0)
            ax.text(mx + ox * off, my + oy * off, lab, ha="center", va="center", fontsize=9.5,
                    color=ACCENT, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"), zorder=5)
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 1.6, max(xs) + 1.6); ax.set_ylim(min(ys) - 1.6, max(ys) + 2.1)
    ax.set_aspect("equal"); ax.axis("off")
    return fig_to_b64(fig)

def render_tree(s):
    root, edges, goal = s["root"], s["edges"], s.get("goal")
    children = {}
    for p, c in edges: children.setdefault(p, []).append(c)
    pos = {}; leafx = [0]
    def dfs(node, d):
        ch = children.get(node, [])
        if not ch:
            x = leafx[0]; leafx[0] += 1; pos[node] = (x, -d); return x
        xs = [dfs(c, d + 1) for c in ch]; x = sum(xs) / len(xs); pos[node] = (x, -d); return x
    dfs(root, 0)
    fig, ax = plt.subplots(figsize=(6.2, 4.0)); VS = 1.5
    for p, c in edges:
        ax.plot([pos[p][0], pos[c][0]], [pos[p][1] * VS, pos[c][1] * VS], color="#94a3b8", lw=1.6, zorder=1)
    for node, (x, y) in pos.items():
        Y = y * VS; g = (node == goal)
        ax.add_patch(Circle((x, Y), 0.30, fc="#dcfce7" if g else "#eef2ff",
                            ec="#15803d" if g else "#1e293b", lw=2, zorder=3))
        ax.text(x, Y, node, ha="center", va="center", fontsize=10, fontweight="bold", zorder=4)
    xs = [p[0] for p in pos.values()]; ys = [p[1] * VS for p in pos.values()]
    ax.set_xlim(min(xs) - 0.7, max(xs) + 0.7); ax.set_ylim(min(ys) - 0.7, max(ys) + 0.7)
    ax.set_aspect("equal"); ax.axis("off")
    return fig_to_b64(fig)

def render_game_tree(s):
    root = s["node"]; pos = {}; meta = {}; edges = []; leafx = [0]; ctr = [0]
    def walk(node, d):
        myid = ctr[0]; ctr[0] += 1
        if "leaf" in node:
            x = leafx[0]; leafx[0] += 1; pos[myid] = (x, -d); meta[myid] = ("leaf", node["leaf"]); return x, myid
        kids = [walk(c, d + 1) for c in node.get("children", [])]
        x = sum(k[0] for k in kids) / len(kids); pos[myid] = (x, -d); meta[myid] = (node.get("player", "max"), None)
        for _, cid in kids: edges.append((myid, cid))
        return x, myid
    walk(root, 0)
    fig, ax = plt.subplots(figsize=(6.4, 4.0)); VS = 1.6; r = 0.26
    for p, c in edges:
        ax.plot([pos[p][0], pos[c][0]], [pos[p][1] * VS, pos[c][1] * VS], color="#94a3b8", lw=1.5, zorder=1)
    for nid, (x, y) in pos.items():
        Y = y * VS; t, val = meta[nid]
        if t == "leaf":
            ax.add_patch(Rectangle((x - r, Y - r), 2 * r, 2 * r, fc="#fee2e2", ec="#b91c1c", lw=1.8, zorder=3))
            ax.text(x, Y, str(val), ha="center", va="center", fontsize=10, fontweight="bold", zorder=4)
        elif t == "max":
            ax.add_patch(Polygon([(x, Y + r), (x - r, Y - r), (x + r, Y - r)], closed=True,
                                 fc="#dbeafe", ec="#1d4ed8", lw=1.8, zorder=3))
        else:
            ax.add_patch(Polygon([(x, Y - r), (x - r, Y + r), (x + r, Y + r)], closed=True,
                                 fc="#ede9fe", ec="#6d28d9", lw=1.8, zorder=3))
    xs = [p[0] for p in pos.values()]; ys = [p[1] * VS for p in pos.values()]
    ax.set_xlim(min(xs) - 0.7, max(xs) + 0.7); ax.set_ylim(min(ys) - 0.7, max(ys) + 1.1)
    ax.text(min(xs) - 0.5, max(ys) + 0.7, "△ MAX   ▽ MIN   □ leaf value",
            fontsize=9, color="#475569")
    ax.set_aspect("equal"); ax.axis("off")
    return fig_to_b64(fig)

def render_scatter(s):
    pts = s["points"]; xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    clusters = s.get("clusters"); centroids = s.get("centroids"); line = s.get("line")
    cols = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c"]
    fig, ax = plt.subplots(figsize=(5.3, 4.0))
    if clusters:
        for i, (x, y) in enumerate(pts):
            ax.scatter(x, y, color=cols[clusters[i] % len(cols)], s=70, zorder=3, edgecolor="white", lw=0.8)
    else:
        ax.scatter(xs, ys, color="#2563eb", s=70, zorder=3, edgecolor="white", lw=0.8)
    if centroids:
        for j, (cx, cy) in enumerate(centroids):
            ax.scatter(cx, cy, marker="X", s=240, color=cols[j % len(cols)], edgecolor="black", lw=1.5, zorder=4)
    if line:
        m, b = line["slope"], line["intercept"]
        xr = np.linspace(min(xs), max(xs), 100)
        ax.plot(xr, m * xr + b, color="#0f172a", lw=2, zorder=2, label=f"y = {m}x + {b}")
        ax.legend(fontsize=9)
    ax.set_xlabel(s.get("xlabel", "x")); ax.set_ylabel(s.get("ylabel", "y"))
    ax.grid(True, alpha=0.3)
    return fig_to_b64(fig)

def render_curve(s):
    pts = s["points"]; xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.plot(xs, ys, color="#2563eb", lw=2.3, zorder=2)
    for m in s.get("markers", []):
        ax.scatter(m["x"], m["y"], s=90, color="#dc2626", zorder=4, edgecolor="white")
        ax.annotate(m.get("label", ""), (m["x"], m["y"]), textcoords="offset points", xytext=(0, 11),
                    ha="center", fontsize=9, fontweight="bold", color=ACCENT)
    ax.set_xlabel(s.get("xlabel", "x")); ax.set_ylabel(s.get("ylabel", "y"))
    ax.grid(True, alpha=0.3)
    return fig_to_b64(fig)

RENDER = {"graph": render_graph, "tree": render_tree, "game_tree": render_game_tree,
          "scatter": render_scatter, "curve": render_curve}

# ---------- load ----------
def qsort_key(q):
    m = re.search(r"Q(\d+)$", q["id"]); return int(m.group(1)) if m else 0

lectures = []
for lid in ORDER:
    data = json.load(open(os.path.join(DATA, lid + ".json"), encoding="utf-8"))
    data.sort(key=qsort_key)
    lectures.append((lid, data))

# ---------- html helpers ----------
def esc(s): return html.escape(str(s))
def stem_html(s):
    mono = ("|" in s) or bool(re.search(r"\S {2,}\S", s))
    return f'<div class="stem{" mono" if mono else ""}">{esc(s)}</div>'

def fig_html(fig):
    if not fig: return ""
    b64 = RENDER[fig["type"]](fig)
    cap = esc(fig.get("caption", ""))
    return (f'<div class="figwrap"><img src="data:image/png;base64,{b64}"/>'
            f'<div class="cap">{cap}</div></div>')

# ---------- assemble ----------
parts = []
parts.append("""<!doctype html><html><head><meta charset="utf-8"><style>
* { box-sizing: border-box; }
@page { size: A4; margin: 15mm 15mm 17mm; }
body { font-family: "Segoe UI", system-ui, Arial, sans-serif; color:#0f172a; font-size:11pt; line-height:1.45; margin:0; }
h1 { font-size:26pt; margin:0 0 4px; letter-spacing:-0.5px; }
.sub { color:#475569; font-size:11pt; margin-bottom:18px; }
.box { background:#f1f5f9; border:1px solid #e2e8f0; border-radius:10px; padding:14px 16px; margin:14px 0; }
.box h3 { margin:0 0 6px; font-size:12pt; }
.box ul { margin:6px 0 0; padding-left:20px; } .box li { margin:3px 0; }
.lec { break-before: page; }
.lec-head { background:#0f172a; color:#fff; padding:9px 14px; border-radius:8px; font-size:14pt; font-weight:700; margin:0 0 14px; }
.q { break-inside: avoid; margin:0 0 15px; padding:11px 13px; border:1px solid #e5e7eb; border-radius:9px; }
.qhead { display:flex; justify-content:space-between; align-items:baseline; gap:10px; margin-bottom:5px; }
.qnum { font-weight:800; font-size:11.5pt; color:#0f172a; }
.topic { font-size:8.5pt; color:#475569; background:#eef2ff; border-radius:20px; padding:2px 9px; white-space:nowrap; }
.stem { white-space:pre-wrap; margin:2px 0 7px; }
.stem.mono { font-family: ui-monospace, Consolas, monospace; font-size:10pt; background:#f8fafc; padding:8px 10px; border-radius:6px; }
.opt { margin:3px 0 3px 6px; padding:2px 0; } .opt b { display:inline-block; width:1.4em; color:#1d4ed8; }
.figwrap { text-align:center; margin:8px 0; }
.figwrap img { max-width:78%; border:1px solid #e5e7eb; border-radius:8px; padding:4px; background:#fff; }
.cap { font-size:8.5pt; color:#64748b; margin-top:3px; font-style:italic; }
.sheet { display:grid; grid-template-columns: repeat(5, 1fr); gap:5px 14px; margin-top:8px; }
.cell { font-size:9.5pt; border-bottom:1px solid #cbd5e1; padding:3px 2px; }
.cell b { color:#1d4ed8; }
.ak { break-before: page; }
.ak-item { break-inside: avoid; margin:0 0 9px; padding:8px 11px; border:1px solid #e5e7eb; border-radius:8px; }
.ak-item .num { font-weight:800; }
.ans { color:#15803d; font-weight:800; }
.expl { color:#334155; font-size:10pt; margin-top:3px; }
.akhead { background:#15803d; }
</style></head><body>""")

# Title + instructions + answer sheet
total = sum(len(d) for _, d in lectures)
parts.append(f"""<h1>AI Exam &mdash; Self-Test</h1>
<div class="sub">{total} exam-level applied multiple-choice questions &middot; 10 lectures (L02&ndash;L12) &middot; with diagrams</div>
<div class="box"><h3>How to use this test</h3>
<ul>
<li>Work through all {total} questions and record your letter answers on the sheet below (or on paper).</li>
<li>Each question has exactly <b>one</b> correct option. These are <b>applied</b> questions &mdash; expect to trace algorithms, compute values, and classify scenarios, not just recall definitions.</li>
<li>When done, check the <b>Answer Key</b> at the end (it starts on its own page so you won't see answers while solving). Each answer includes a short explanation.</li>
<li>Tally your score <i>per lecture</i> to see exactly which topics to review.</li>
</ul></div>""")

# answer sheet grid
gnum = 0; cells = []
for lid, data in lectures:
    for q in data:
        gnum += 1; cells.append(f'<div class="cell"><b>Q{gnum}</b> ({lid}): ____</div>')
parts.append('<div class="box"><h3>Answer sheet</h3><div class="sheet">' + "".join(cells) + "</div></div>")

# Questions
gnum = 0; keymap = []
for lid, data in lectures:
    parts.append(f'<div class="lec"><div class="lec-head">{esc(TITLES[lid])}</div>')
    for q in data:
        gnum += 1
        keymap.append((gnum, lid, q))
        opts = q["options"]
        ohtml = "".join(f'<div class="opt"><b>{k})</b> {esc(opts[k])}</div>' for k in ["A", "B", "C", "D"])
        parts.append(f"""<div class="q"><div class="qhead"><span class="qnum">Q{gnum}</span>
<span class="topic">{esc(q.get("topic",""))}</span></div>
{stem_html(q["stem"])}{fig_html(q.get("figure"))}{ohtml}</div>""")
    parts.append("</div>")

# Answer key
parts.append('<div class="ak"><div class="lec-head akhead">Answer Key &amp; Explanations</div>')
cur = None
for gn, lid, q in keymap:
    if lid != cur:
        cur = lid
        parts.append(f'<div style="font-weight:800;margin:12px 0 6px;color:#0f172a;">{esc(TITLES[lid])}</div>')
    parts.append(f"""<div class="ak-item"><span class="num">Q{gn}.</span>
<span class="ans">{esc(q["answer"])}</span> &mdash; {esc(q["explanation"])}</div>""")
parts.append("</div>")

parts.append("</body></html>")
open(OUT_HTML, "w", encoding="utf-8").write("".join(parts))
print("Wrote HTML:", OUT_HTML, "| questions:", total)
