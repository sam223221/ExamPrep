"""
Generate TTS audio (MP3) for every lecture and the master index of the
AI Exam Prep study package, optimized for a dyslexic listener.

- Voice:   en-US-JennyNeural   (clear, natural, widely recommended for accessibility)
- Rate:    -10%                 (slightly slower than default)
- Format:  MP3, 24 kHz, mono, ~48 kbps (edge-tts default for Jenny)

Strategy
--------
Markdown -> "spoken-English" plain text via a deterministic cleaner that:
  * strips code blocks, mermaid diagrams, image refs, anchors, HTML
  * rewrites LaTeX math into natural English (alpha, sum over i, f of n, etc.)
  * rewrites unicode math symbols (in, to, less-than-or-equal, ...)
  * unrolls Markdown tables row-by-row
  * preserves heading hierarchy with extra pauses for clarity

Long lectures (~12k words) would push edge-tts close to its practical
per-request ceiling, so the cleaned text is split on top-level H2 headings
(`## ...`) into section chunks. Each chunk is synthesized to a temp file,
then the temp MP3s are concatenated by raw byte append (works for the
streamable MP3 frames edge-tts emits; pydub fallback is available if the
result ever looks malformed).

Usage:
    py -3.12 study\\audio\\generate_audio.py
"""

from __future__ import annotations

import asyncio
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Iterable

import edge_tts


# -------------------------- configuration ----------------------------------

VOICE_PRIMARY = "en-US-JennyNeural"
VOICE_BACKUP = "en-US-AriaNeural"
RATE = "-10%"
PITCH = "+0Hz"

ROOT = Path(__file__).resolve().parent.parent          # .../AI/study
AUDIO_DIR = ROOT / "audio"
LECTURES_DIR = ROOT / "lectures"

SOURCES: list[Path] = [
    ROOT / "00-master-index.md",
    LECTURES_DIR / "L02-Agents.md",
    LECTURES_DIR / "L03-Uninformed-Search.md",
    LECTURES_DIR / "L05-Local-Search.md",
    LECTURES_DIR / "L06-Adversarial-Search.md",
    LECTURES_DIR / "L07-CSP.md",
    LECTURES_DIR / "L09a-Bayesian-Networks.md",
    LECTURES_DIR / "L09b-HMM.md",
    LECTURES_DIR / "L10-Intro-to-ML.md",
    LECTURES_DIR / "L11-Regression.md",
    LECTURES_DIR / "L12-Clustering.md",
]

# Approx max characters of cleaned text per TTS request. edge-tts handles
# much more, but smaller chunks recover faster from transient network errors
# and let us stream progress per section.
MAX_CHARS_PER_CHUNK = 6000


# -------------------------- math / symbol tables ---------------------------

GREEK = {
    r"\\alpha": "alpha", r"\\beta": "beta", r"\\gamma": "gamma",
    r"\\delta": "delta", r"\\epsilon": "epsilon", r"\\varepsilon": "epsilon",
    r"\\zeta": "zeta", r"\\eta": "eta", r"\\theta": "theta",
    r"\\vartheta": "theta", r"\\iota": "iota", r"\\kappa": "kappa",
    r"\\lambda": "lambda", r"\\mu": "mu", r"\\nu": "nu",
    r"\\xi": "ksi", r"\\pi": "pi", r"\\rho": "rho",
    r"\\sigma": "sigma", r"\\tau": "tau", r"\\upsilon": "upsilon",
    r"\\phi": "phi", r"\\varphi": "phi", r"\\chi": "chi",
    r"\\psi": "psi", r"\\omega": "omega",
    r"\\Gamma": "capital gamma", r"\\Delta": "capital delta",
    r"\\Theta": "capital theta", r"\\Lambda": "capital lambda",
    r"\\Xi": "capital ksi", r"\\Pi": "capital pi",
    r"\\Sigma": "capital sigma", r"\\Phi": "capital phi",
    r"\\Psi": "capital psi", r"\\Omega": "capital omega",
}

LATEX_OPS = {
    r"\\times": " times ",
    r"\\cdot": " dot ",        # placeholder dot; binary use is rare in these notes
    r"\\langle": " ",
    r"\\rangle": " ",
    r"\\div": " divided by ",
    r"\\pm": " plus or minus ",
    r"\\mp": " minus or plus ",
    r"\\leq": " less than or equal to ",
    r"\\geq": " greater than or equal to ",
    r"\\le": " less than or equal to ",
    r"\\ge": " greater than or equal to ",
    r"\\neq": " not equal to ",
    r"\\ne": " not equal to ",
    r"\\approx": " approximately equals ",
    r"\\sim": " is distributed as ",
    r"\\equiv": " is equivalent to ",
    r"\\propto": " is proportional to ",
    r"\\to": " to ",
    r"\\rightarrow": " to ",
    r"\\Rightarrow": " implies ",
    r"\\leftarrow": " from ",
    r"\\Leftarrow": " is implied by ",
    r"\\leftrightarrow": " if and only if ",
    r"\\Leftrightarrow": " if and only if ",
    r"\\iff": " if and only if ",
    r"\\implies": " implies ",
    r"\\forall": " for all ",
    r"\\exists": " there exists ",
    r"\\in": " in ",
    r"\\notin": " not in ",
    r"\\subset": " is a subset of ",
    r"\\subseteq": " is a subset of or equal to ",
    r"\\supset": " is a superset of ",
    r"\\cup": " union ",
    r"\\cap": " intersect ",
    r"\\emptyset": " the empty set ",
    r"\\varnothing": " the empty set ",
    r"\\infty": " infinity ",
    r"\\partial": " partial ",
    r"\\nabla": " gradient ",
    r"\\circ": " composed with ",
    r"\\land": " and ",
    r"\\lor": " or ",
    r"\\lnot": " not ",
    r"\\neg": " not ",
    r"\\mid": " given ",
    r"\\colon": ": ",
    r"\\ldots": ", and so on, ",
    r"\\dots": ", and so on, ",
    r"\\cdots": ", and so on, ",
    r"\\ast": " star ",
    r"\\star": " star ",
    r"\\bullet": " ",
    r"\\quad": " ",
    r"\\qquad": " ",
    r"\\,": " ",
    r"\\;": " ",
    r"\\:": " ",
    r"\\!": "",
    r"\\\\": ". ",
    r"\\%": " percent ",
    r"\\&": " and ",
    r"\\#": " ",
    r"\\$": " dollar ",
    r"\\_": " ",
    r"\\{": " ",
    r"\\}": " ",
    r"\\left": "",
    r"\\right": "",
    r"\\big": "", r"\\Big": "", r"\\bigg": "", r"\\Bigg": "",
    r"\\displaystyle": "",
    r"\\textstyle": "",
    r"\\,$": "",
}

# blackboard / cal / mathbf — just drop the wrapper
LATEX_FONT_WRAPPERS = [
    r"\\mathbb",
    r"\\mathcal",
    r"\\mathbf",
    r"\\mathrm",
    r"\\mathsf",
    r"\\mathit",
    r"\\text",
    r"\\textbf",
    r"\\textit",
    r"\\boldsymbol",
    r"\\bm",
    r"\\operatorname",
    r"\\overline",
    r"\\underline",
    r"\\widehat",
    r"\\hat",
    r"\\widetilde",
    r"\\tilde",
    r"\\bar",
    r"\\vec",
    r"\\dot",
    r"\\ddot",
]

# Common probability/stat operator names (read literally).
LATEX_NAMED_FUNCS = {
    r"\\Pr": "probability",
    r"\\Prob": "probability",
    r"\\Var": "variance",
    r"\\Cov": "covariance",
    r"\\Corr": "correlation",
    r"\\argmax": "arg max",
    r"\\argmin": "arg min",
    r"\\arg\\max": "arg max",
    r"\\arg\\min": "arg min",
    r"\\max": "max",
    r"\\min": "min",
    r"\\log": "log",
    r"\\ln": "natural log",
    r"\\exp": "exp",
    r"\\sin": "sine",
    r"\\cos": "cosine",
    r"\\tan": "tangent",
    r"\\sqrt": "square root of",
    r"\\sum": "sum",
    r"\\prod": "product",
    r"\\int": "integral",
}

UNICODE_MATH = {
    "→": " to ",
    "←": " from ",
    "↔": " if and only if ",
    "⇒": " implies ",
    "⇐": " is implied by ",
    "⇔": " if and only if ",
    "≤": " less than or equal to ",
    "≥": " greater than or equal to ",
    "≠": " not equal to ",
    "≈": " approximately equals ",
    "≡": " is equivalent to ",
    "∝": " is proportional to ",
    "∈": " in ",
    "∉": " not in ",
    "⊂": " is a subset of ",
    "⊆": " is a subset of or equal to ",
    "⊃": " is a superset of ",
    "∪": " union ",
    "∩": " intersect ",
    "∅": " the empty set ",
    "∞": " infinity ",
    "∂": " partial ",
    "∇": " gradient ",
    "∀": " for all ",
    "∃": " there exists ",
    "∑": " sum ",
    "∏": " product ",
    "∫": " integral ",
    "√": " square root of ",
    "±": " plus or minus ",
    "×": " times ",
    "·": " times ",
    "÷": " divided by ",
    "°": " degrees ",
    "α": " alpha ", "β": " beta ", "γ": " gamma ", "δ": " delta ",
    "ε": " epsilon ", "ζ": " zeta ", "η": " eta ", "θ": " theta ",
    "ι": " iota ", "κ": " kappa ", "λ": " lambda ", "μ": " mu ",
    "ν": " nu ", "ξ": " ksi ", "π": " pi ", "ρ": " rho ",
    "σ": " sigma ", "τ": " tau ", "υ": " upsilon ", "φ": " phi ",
    "χ": " chi ", "ψ": " psi ", "ω": " omega ",
    "Γ": " capital gamma ", "Δ": " capital delta ", "Θ": " capital theta ",
    "Λ": " capital lambda ", "Ξ": " capital ksi ", "Π": " capital pi ",
    "Σ": " capital sigma ", "Φ": " capital phi ", "Ψ": " capital psi ",
    "Ω": " capital omega ",
    "ℝ": " the real numbers ",
    "ℕ": " the natural numbers ",
    "ℤ": " the integers ",
    "ℚ": " the rationals ",
    "ℂ": " the complex numbers ",
    "²": " squared ",
    "³": " cubed ",
    "—": ", ",
    "–": ", ",
    "…": ", and so on, ",
    "•": ". ",
    "·": " ",
    "“": '"', "”": '"', "‘": "'", "’": "'",
    " ": " ",   # nbsp
    "​": "",    # zero-width space
}

# Pronunciation overrides — applied to plain English text after math is gone.
# Order matters: longer/qualified patterns first.
PRONUNCIATION = [
    (re.compile(r"\bA\*\b"),                          "A-star"),
    (re.compile(r"\bA\s*-\s*star\b"),                 "A-star"),
    (re.compile(r"\bK\s*-\s*means\b", re.I),          "K means"),
    (re.compile(r"\bK\s*-\s*medoids\b", re.I),        "K medoids"),
    (re.compile(r"\bK\s*-\s*NN\b"),                   "K nearest neighbours"),
    (re.compile(r"\bk\s*-\s*nn\b"),                   "k nearest neighbours"),
    (re.compile(r"\bDBSCAN\b"),                       "D B SCAN"),
    (re.compile(r"\bBFS\b"),                          "B F S"),
    (re.compile(r"\bDFS\b"),                          "D F S"),
    (re.compile(r"\bUCS\b"),                          "U C S"),
    (re.compile(r"\bIDS\b"),                          "I D S"),
    (re.compile(r"\bDLS\b"),                          "D L S"),
    (re.compile(r"\bCSP\b"),                          "C S P"),
    (re.compile(r"\bCSPs\b"),                         "C S Ps"),
    (re.compile(r"\bMRV\b"),                          "M R V"),
    (re.compile(r"\bLCV\b"),                          "L C V"),
    (re.compile(r"\bAC-?3\b"),                        "A C 3"),
    (re.compile(r"\bPEAS\b"),                         "PEAS"),  # acronym read as a word
    (re.compile(r"\bBN\b"),                           "Bayes net"),
    (re.compile(r"\bBNs\b"),                          "Bayes nets"),
    (re.compile(r"\bHMM\b"),                          "H M M"),
    (re.compile(r"\bHMMs\b"),                         "H M Ms"),
    (re.compile(r"\bMDP\b"),                          "M D P"),
    (re.compile(r"\bMLE\b"),                          "M L E"),
    (re.compile(r"\bMAP\b"),                          "M A P"),
    (re.compile(r"\bOLS\b"),                          "O L S"),
    (re.compile(r"\bSSE\b"),                          "S S E"),
    (re.compile(r"\bSSR\b"),                          "S S R"),
    (re.compile(r"\bSST\b"),                          "S S T"),
    (re.compile(r"\bR\^?2\b"),                        "R squared"),
    (re.compile(r"\bR-?squared\b", re.I),             "R squared"),
    (re.compile(r"\bp-?value(s)?\b", re.I),
                                                       lambda m: "p values" if m.group(1) else "p value"),
    (re.compile(r"\bGA\b"),                           "G A"),
    (re.compile(r"\bGAs\b"),                          "G As"),
    (re.compile(r"\bML\b"),                           "M L"),
    (re.compile(r"\bAI\b"),                           "A I"),
    (re.compile(r"\bRL\b"),                           "reinforcement learning"),
    (re.compile(r"\bL1\b"),                           "L one"),
    (re.compile(r"\bL2\b"),                           "L two"),
    (re.compile(r"\bSection\s+§\s*(\d+(?:\.\d+)*)"),  r"Section \1"),
    (re.compile(r"§\s*(\d+(?:\.\d+)*)"),              r"section \1"),
]


# -------------------------- markdown / latex cleaner -----------------------

_RE_CODE_FENCE = re.compile(r"^```[^\n]*\n.*?^```", re.MULTILINE | re.DOTALL)
_RE_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_RE_HTML_TAG = re.compile(r"</?[a-zA-Z][^>]*>")
_RE_IMG = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_RE_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_RE_REF_LINK = re.compile(r"\[([^\]]+)\]\[[^\]]*\]")
_RE_ANCHOR = re.compile(r"\s*\{#[a-zA-Z0-9\-_.:]+\}")
_RE_HRULE = re.compile(r"^\s*(?:-\s*){3,}\s*$", re.MULTILINE)
_RE_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}.*$", re.MULTILINE)
_RE_BACKTICK_INLINE = re.compile(r"`([^`\n]+)`")
_RE_BLOCKQUOTE = re.compile(r"^>\s?", re.MULTILINE)
_RE_LIST_MARKER = re.compile(r"^(\s*)([-*+]|\d+\.)\s+", re.MULTILINE)
_RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
_RE_MULTI_BLANK = re.compile(r"\n{3,}")
_RE_BOLD = re.compile(r"\*\*([^*]+?)\*\*", re.DOTALL)
_RE_ITAL_UNDER = re.compile(r"(?<!\w)_([^_\n]+)_(?!\w)")
_RE_ITAL_STAR = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)", re.DOTALL)
_RE_INLINE_MATH = re.compile(r"\$([^$]+?)\$", re.DOTALL)
_RE_BLOCK_MATH = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_RE_BRACES = re.compile(r"\{([^{}]*)\}")

# subscript and superscript: identifier or {block}
_RE_SUB = re.compile(r"_(\{[^{}]+\}|[A-Za-z0-9]+)")
_RE_SUP = re.compile(r"\^(\{[^{}]+\}|[A-Za-z0-9+\-*]+)")
_RE_FRAC = re.compile(r"\\d?frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}")
_RE_FRAC2 = re.compile(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}")


def _strip_code_blocks(md: str) -> str:
    # Replace fenced code (including ```mermaid) with a brief spoken stand-in.
    def _replace(match: re.Match[str]) -> str:
        block = match.group(0)
        first_line = block.split("\n", 1)[0].strip("` ").lower()
        if "mermaid" in first_line:
            return "\n\n[diagram — see the PDF]\n\n"
        return "\n\n[code example — see the PDF]\n\n"
    return _RE_CODE_FENCE.sub(_replace, md)


def _strip_images(md: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        caption = match.group(1).strip()
        if not caption:
            return ""
        return f"Figure: {caption}."
    return _RE_IMG.sub(_replace, md)


def _flatten_links(md: str) -> str:
    md = _RE_LINK.sub(r"\1", md)
    md = _RE_REF_LINK.sub(r"\1", md)
    return md


def _table_to_prose(md: str) -> str:
    """Convert pipe tables into row-by-row prose.

    A table block is: header row | separator row (---) | data rows.
    We detect a separator and treat the immediately preceding line as the
    header.  Each data row becomes "Row N: <col header> is <value>, ...".
    """
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if (i + 1 < len(lines)
                and "|" in line
                and _RE_TABLE_SEP.match(lines[i + 1])):
            # Found a table.  Parse header.
            header_cells = [c.strip() for c in _split_table_row(line)]
            i += 2  # skip header + separator
            row_n = 0
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                cells = [c.strip() for c in _split_table_row(lines[i])]
                row_n += 1
                pieces: list[str] = []
                for h, c in zip(header_cells, cells):
                    if not c:
                        continue
                    if h:
                        pieces.append(f"{h} is {c}")
                    else:
                        pieces.append(c)
                if pieces:
                    out.append(f"Row {row_n}: " + "; ".join(pieces) + ".")
                i += 1
            out.append("")  # blank line after table
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def _split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return line.split("|")


# ---- LaTeX → English -------------------------------------------------------

def _expand_fractions(s: str) -> str:
    # \dfrac / \tfrac / \frac{a}{b} → "a over b"
    prev = None
    while prev != s:
        prev = s
        s = _RE_FRAC2.sub(lambda m: f"({m.group(1)}) over ({m.group(2)})", s)
        s = re.sub(r"\\[dt]frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}",
                   lambda m: f"({m.group(1)}) over ({m.group(2)})", s)
    return s


def _strip_font_wrappers(s: str) -> str:
    # \mathbb{R} → R ;  \text{stuff} → stuff
    for cmd in LATEX_FONT_WRAPPERS:
        pattern = re.compile(cmd + r"\s*\{([^{}]*)\}")
        prev = None
        while prev != s:
            prev = s
            s = pattern.sub(r"\1", s)
    return s


def _latex_to_english(s: str) -> str:
    """Convert a LaTeX math fragment into spoken English.

    Heuristic — not a real LaTeX parser. Good enough for the textbook-style
    expressions used in the lecture notes (no nested macros, no \\begin{}).
    """
    s = s.strip()

    # \frac and friends first (must run before brace stripping).
    s = _expand_fractions(s)

    # Sum/prod/integral with bounds: \sum_{i=1}^{n}  →  "sum from i=1 to n"
    s = re.sub(
        r"\\(sum|prod|int)_\{([^{}]+)\}\^\{([^{}]+)\}",
        lambda m: f" {_named(m.group(1))} from {m.group(2)} to {m.group(3)} ",
        s,
    )
    s = re.sub(
        r"\\(sum|prod|int)_\{([^{}]+)\}",
        lambda m: f" {_named(m.group(1))} over {m.group(2)} ",
        s,
    )
    s = re.sub(
        r"\\(sum|prod|int)\^\{([^{}]+)\}_\{([^{}]+)\}",
        lambda m: f" {_named(m.group(1))} from {m.group(3)} to {m.group(2)} ",
        s,
    )

    # argmin/argmax/max/min with subscript: \max_{a} → "max over a"
    s = re.sub(
        r"\\(arg\\max|arg\\min|argmax|argmin|max|min)_\{([^{}]+)\}",
        lambda m: f" {_named(m.group(1))} over {m.group(2)} ",
        s,
    )

    # \sqrt{...} → square root of (...)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r" square root of (\1) ", s)

    # \mathbb{E}[X|Y] / \mathbb{E}_{p}[...] etc. — drop the wrappers first
    s = _strip_font_wrappers(s)

    # Named functions (must come AFTER font stripping so \mathrm{Var} -> Var).
    for cmd, repl in LATEX_NAMED_FUNCS.items():
        s = re.sub(cmd + r"\b", " " + repl + " ", s)

    # Greek letters.
    for cmd, repl in GREEK.items():
        s = re.sub(cmd + r"\b", " " + repl + " ", s)

    # Generic operators / symbols.
    for cmd, repl in LATEX_OPS.items():
        s = re.sub(cmd, repl, s)

    # "P(\cdot)" / "U[\cdot]" placeholder notation — strip the dot-only arg
    # so we read "P" instead of "P of dot".
    s = re.sub(r"\(\s*(?:dot|\.)\s*\)", "", s)
    s = re.sub(r"\[\s*(?:dot|\.)\s*\]", "", s)

    # Subscripts and superscripts.
    # x_{i,j} → "x sub i comma j" ;  x^2 → "x squared" ;  x^n → "x to the n"
    def _sub_repl(m: re.Match[str]) -> str:
        body = m.group(1)
        if body.startswith("{"):
            body = body[1:-1]
        body = body.replace(",", " comma ")
        return f" sub {body} "
    s = _RE_SUB.sub(_sub_repl, s)

    def _sup_repl(m: re.Match[str]) -> str:
        body = m.group(1)
        if body.startswith("{"):
            body = body[1:-1]
        if body == "2":
            return " squared "
        if body == "3":
            return " cubed "
        if body == "T":
            return " transpose "
        if body == "-1":
            return " inverse "
        if body == "*":
            return " star "
        body = body.replace(",", " comma ")
        return f" to the {body} "
    s = _RE_SUP.sub(_sup_repl, s)

    # Equality, arithmetic — basic symbol pass.
    s = s.replace("=", " equals ")
    s = s.replace("+", " plus ")
    s = re.sub(r"(?<![a-zA-Z0-9])-(?![a-zA-Z0-9])", " minus ", s)  # standalone -
    s = s.replace("/", " over ")

    # Function-call style: f(n)  →  "f of n"
    s = re.sub(
        r"\b([A-Za-z][A-Za-z0-9]*)\s*\(\s*([A-Za-z0-9 ,]+?)\s*\)",
        lambda m: f"{m.group(1)} of {m.group(2).replace(',', ' comma ')}",
        s,
    )

    # Remaining braces → bare words.
    s = _RE_BRACES.sub(r"\1", s)

    # Apply unicode symbol pass for anything left.
    for k, v in UNICODE_MATH.items():
        s = s.replace(k, v)

    # Collapse stray backslashes / whitespace.
    s = re.sub(r"\\([A-Za-z]+)", r"\1", s)   # drop unknown TeX macros
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _named(token: str) -> str:
    return {
        "sum": "sum",
        "prod": "product",
        "int": "integral",
        "max": "max",
        "min": "min",
        "argmax": "arg max",
        "argmin": "arg min",
        "arg\\max": "arg max",
        "arg\\min": "arg min",
    }.get(token, token)


def _replace_inline_math(text: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        body = match.group(1)
        # strip blockquote markers / list bullets that the math span crossed
        body = re.sub(r"\n\s*>\s?", " ", body)
        body = re.sub(r"\n\s*[-*+]\s+", " ", body)
        # collapse any soft wraps inside the math span before parsing
        body = re.sub(r"\s+", " ", body).strip()
        # collapse "x _i" → "x_i" so subscript regex matches the joined form
        body = re.sub(r"\s+_", "_", body)
        body = re.sub(r"\s+\^", "^", body)
        english = _latex_to_english(body)
        # If the result is still gnarly (long, lots of unparsed macros),
        # fall back to a generic stand-in so the listener isn't bombarded.
        if english.count("\\") > 0 or len(english) > 220:
            return " [math expression] "
        return f" {english} "
    return _RE_INLINE_MATH.sub(_replace, text)


def _replace_block_math(text: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        body = match.group(1).strip()
        # Strip alignment characters that aren't pronounceable.
        body = body.replace("&", " ").replace(r"\\", " . ")
        body = re.sub(r"\s+", " ", body)
        body = re.sub(r"\s+_", "_", body)
        body = re.sub(r"\s+\^", "^", body)
        english = _latex_to_english(body)
        if english.count("\\") > 0 or len(english) > 320:
            return "\n\n[math expression — see the PDF]\n\n"
        return f"\n\n{english}.\n\n"
    return _RE_BLOCK_MATH.sub(_replace, text)


# ---- final markdown pass ---------------------------------------------------

def _apply_pronunciation(text: str) -> str:
    for rgx, repl in PRONUNCIATION:
        text = rgx.sub(repl, text)
    return text


def clean_markdown_for_tts(md: str) -> str:
    """Return spoken-English plain text for TTS."""
    # 0. Normalize a few unicode forms BEFORE other passes so en-dash ranges
    #    like "60–75 min" read as "60 to 75 min" instead of "60, 75 min".
    md = re.sub(r"(\d)\s*[–—]\s*(\d)", r"\1 to \2", md)

    # 1. Front-matter, html comments.
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.DOTALL)
    md = _RE_HTML_COMMENT.sub("", md)

    # 2. Code blocks (and mermaid) FIRST so we don't try to LaTeX-parse them.
    md = _strip_code_blocks(md)

    # 3. Block-level math BEFORE inline math.
    md = _replace_block_math(md)

    # 4. Tables → prose.
    md = _table_to_prose(md)

    # 5. Images → "Figure: caption."
    md = _strip_images(md)

    # 6. Links → just the visible text.
    md = _flatten_links(md)

    # 7. Anchors {#some-id}.
    md = _RE_ANCHOR.sub("", md)

    # 8. Inline math.
    md = _replace_inline_math(md)

    # 9. Headings → add a clear vocal cue + extra pause.
    def _heading(match: re.Match[str]) -> str:
        level = len(match.group(1))
        title = match.group(2).strip()
        title = _RE_ANCHOR.sub("", title)
        if level == 1:
            return f"\n\n\n{title}.\n\n"
        if level == 2:
            return f"\n\n\nSection: {title}.\n\n"
        return f"\n\n{title}.\n\n"
    md = _RE_HEADING.sub(_heading, md)

    # 10. Inline backticks → bare text.
    md = _RE_BACKTICK_INLINE.sub(r"\1", md)

    # 11. Bold / italics.
    md = _RE_BOLD.sub(r"\1", md)
    md = _RE_ITAL_STAR.sub(r"\1", md)
    md = _RE_ITAL_UNDER.sub(r"\1", md)

    # 12. Blockquote markers, list markers.
    md = _RE_BLOCKQUOTE.sub("", md)
    md = _RE_LIST_MARKER.sub(r"\1", md)

    # 13. Horizontal rules → paragraph break.
    md = _RE_HRULE.sub("", md)

    # 14. HTML tags.
    md = _RE_HTML_TAG.sub("", md)

    # 15. Unicode math symbols still lingering.
    for k, v in UNICODE_MATH.items():
        md = md.replace(k, v)

    # 16. Pronunciation overrides.
    md = _apply_pronunciation(md)

    # 17. Whitespace + punctuation normalisation.
    md = _RE_MULTI_BLANK.sub("\n\n", md)
    md = re.sub(r"[ \t]+", " ", md)
    md = re.sub(r" *\n *", "\n", md)
    # collapse cascaded commas/periods produced by dash → comma rewrites
    md = re.sub(r",(\s*,)+", ",", md)
    md = re.sub(r"\.(\s*\.)+", ".", md)
    md = re.sub(r"\s+([,.;:!?])", r"\1", md)
    md = re.sub(r"^\s*Figure:\s*\.\s*$", "", md, flags=re.MULTILINE)
    md = md.strip() + "\n"
    return md


# -------------------------- chunking + TTS ---------------------------------

def chunk_text(text: str, max_chars: int = MAX_CHARS_PER_CHUNK) -> list[str]:
    """Split cleaned text into chunks at paragraph boundaries.

    We prefer to break at blank lines (paragraph) so prosody isn't cut in the
    middle of a sentence.  If a single paragraph already exceeds the limit
    (rare — only really long block-quote callouts), it is further split at
    sentence boundaries.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0
    for para in paragraphs:
        if len(para) > max_chars:
            # split this long paragraph on sentence boundaries
            sentences = re.split(r"(?<=[.!?])\s+", para)
            for sent in sentences:
                if buf_len + len(sent) + 1 > max_chars and buf:
                    chunks.append("\n\n".join(buf))
                    buf, buf_len = [], 0
                buf.append(sent)
                buf_len += len(sent) + 1
            continue
        if buf_len + len(para) + 2 > max_chars and buf:
            chunks.append("\n\n".join(buf))
            buf, buf_len = [], 0
        buf.append(para)
        buf_len += len(para) + 2
    if buf:
        chunks.append("\n\n".join(buf))
    return chunks


async def synth_chunk(
    text: str,
    output_path: Path,
    voice: str,
    rate: str,
    pitch: str,
) -> None:
    """Synthesize a single chunk with edge-tts; raise on failure."""
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
    )
    await communicate.save(str(output_path))


async def synth_with_retry(
    text: str,
    output_path: Path,
    voice: str,
    rate: str,
    pitch: str,
    attempts: int = 3,
) -> None:
    last_err: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            await synth_chunk(text, output_path, voice, rate, pitch)
            if output_path.exists() and output_path.stat().st_size > 0:
                return
            raise RuntimeError("edge-tts produced an empty file")
        except Exception as exc:                                  # noqa: BLE001
            last_err = exc
            wait = 2 ** attempt
            print(f"    chunk attempt {attempt}/{attempts} failed: {exc}; "
                  f"sleeping {wait}s")
            await asyncio.sleep(wait)
    raise RuntimeError(f"edge-tts failed after {attempts} attempts: {last_err}")


def concat_mp3(parts: Iterable[Path], output: Path) -> None:
    """Concatenate MP3 part files by raw byte append.

    edge-tts emits streamable MP3 frames (no ID3 trailer / no file-level
    container), so naive byte concatenation produces a valid combined MP3
    that every player handles. We also strip a leading ID3v2 tag on parts
    after the first if any are present, just to be safe.
    """
    parts = list(parts)
    with output.open("wb") as out:
        for i, part in enumerate(parts):
            data = part.read_bytes()
            if i > 0 and data[:3] == b"ID3":
                # Strip ID3v2 header (10 bytes header + size field).
                size = ((data[6] & 0x7F) << 21) | ((data[7] & 0x7F) << 14) \
                       | ((data[8] & 0x7F) << 7) | (data[9] & 0x7F)
                data = data[10 + size:]
            out.write(data)


# -------------------------- duration / sizing ------------------------------

def mp3_duration_seconds(path: Path) -> float | None:
    """Best-effort MP3 duration via pydub (ffmpeg) or mutagen, else None."""
    try:
        from pydub.utils import mediainfo
        info = mediainfo(str(path))
        if info and info.get("duration"):
            return float(info["duration"])
    except Exception:
        pass
    try:
        from mutagen.mp3 import MP3
        return float(MP3(str(path)).info.length)
    except Exception:
        pass
    # Fallback: estimate from file size + nominal 48 kbps bitrate.
    bytes_ = path.stat().st_size
    return bytes_ * 8 / 48000.0


def fmt_duration(seconds: float | None) -> str:
    if seconds is None:
        return "?"
    m, s = divmod(int(round(seconds)), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def fmt_size(bytes_: int) -> str:
    mb = bytes_ / (1024 * 1024)
    if mb >= 1:
        return f"{mb:.2f} MB"
    return f"{bytes_ / 1024:.1f} KB"


# -------------------------- top-level driver -------------------------------

async def process_file(
    src: Path,
    out_dir: Path,
    voice: str,
    rate: str,
    pitch: str,
) -> dict:
    """Clean, chunk, synthesize, concatenate, and report on one source file."""
    basename = src.stem
    print(f"Generating {basename}.mp3 ...", flush=True)
    t0 = time.time()

    md = src.read_text(encoding="utf-8")
    cleaned = clean_markdown_for_tts(md)
    chunks = chunk_text(cleaned)
    final_path = out_dir / f"{basename}.mp3"

    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix=f"tts_{basename}_") as tmp:
        tmp_dir = Path(tmp)
        part_paths: list[Path] = []
        for i, chunk in enumerate(chunks, 1):
            part = tmp_dir / f"part_{i:03d}.mp3"
            try:
                await synth_with_retry(chunk, part, voice, rate, pitch)
                part_paths.append(part)
            except Exception as exc:                              # noqa: BLE001
                print(f"    [WARN] chunk {i}/{len(chunks)} failed: {exc}")
                failures.append(f"{basename} chunk {i}/{len(chunks)}")
        if not part_paths:
            raise RuntimeError(f"no chunks succeeded for {basename}")
        if len(part_paths) == 1:
            shutil.copyfile(part_paths[0], final_path)
        else:
            concat_mp3(part_paths, final_path)

    elapsed = time.time() - t0
    size_b = final_path.stat().st_size
    dur = mp3_duration_seconds(final_path)
    print(f"  done in {elapsed:.1f}s — wrote {final_path.name} "
          f"({fmt_size(size_b)}, {fmt_duration(dur)}, "
          f"{len(chunks)} chunks)", flush=True)

    return {
        "src": src,
        "out": final_path,
        "size_bytes": size_b,
        "duration_seconds": dur,
        "elapsed_seconds": elapsed,
        "chunks": len(chunks),
        "failures": failures,
    }


async def main() -> int:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    missing = [p for p in SOURCES if not p.exists()]
    if missing:
        for m in missing:
            print(f"[ERROR] source not found: {m}")
        return 2

    voice = VOICE_PRIMARY
    print(f"Voice: {voice}    Rate: {RATE}    Output: {AUDIO_DIR}\n")

    results: list[dict] = []
    total_failures: list[str] = []
    for src in SOURCES:
        try:
            res = await process_file(src, AUDIO_DIR, voice, RATE, PITCH)
            results.append(res)
            total_failures.extend(res["failures"])
        except Exception as exc:                                  # noqa: BLE001
            print(f"[ERROR] {src.name} failed: {exc}")
            total_failures.append(f"{src.name} (whole file)")

    print("\n=== Summary ===")
    total_bytes = 0
    total_seconds = 0.0
    for r in results:
        total_bytes += r["size_bytes"]
        if r["duration_seconds"]:
            total_seconds += r["duration_seconds"]
        print(f"  {r['out'].name:35s}  {fmt_size(r['size_bytes']):>10s}  "
              f"{fmt_duration(r['duration_seconds']):>12s}  "
              f"({r['chunks']} chunks)")
    print(f"\nFiles: {len(results)}  Total size: {fmt_size(total_bytes)}  "
          f"Total duration: {fmt_duration(total_seconds)}")
    if total_failures:
        print("\nFailures:")
        for f in total_failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
