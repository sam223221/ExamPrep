"""Lecture identity helpers, curated metadata maps, and the closed taxonomy.

This module is the single source of truth for the canonical lecture id (`L01`..`L12`),
the *numeric* lecture sort (folders are non-zero-padded — `Lecture 1`..`Lecture 12` —
so a lexical sort mis-orders them), the curated deck-title map (PDF basename -> human
title), the lecture -> topic map, and the closed `topic`/`difficulty` vocabularies.

Every downstream module (extract, chunker, ingest, quiz, main) threads the `L01`..`L12`
id derived here so guides, MCQs, and Chroma metadata share one stable join key.
"""

from __future__ import annotations

import re

# --- canonical lecture id ---------------------------------------------------

#: Matches a ``Lecture N`` folder segment and captures the integer N.
_LECTURE_DIR_RE = re.compile(r"Lecture\s+(\d+)\b", re.IGNORECASE)


def lecture_num_of(path: str) -> int | None:
    """Parse the integer lecture number out of a path containing ``Lecture N``.

    ``'.../Lecture 10/Refactoring1.pdf'`` -> ``10``. Returns ``None`` when no
    ``Lecture N`` segment is present so callers can skip non-lecture files.
    """
    norm = path.replace("\\", "/")
    last: int | None = None
    # Scan every segment; the deepest ``Lecture N`` wins (handles nested mounts).
    for seg in norm.split("/"):
        m = _LECTURE_DIR_RE.fullmatch(seg.strip())
        if m:
            last = int(m.group(1))
    if last is not None:
        return last
    # Fallback: a ``Lecture N`` substring anywhere in the path.
    m = _LECTURE_DIR_RE.search(norm)
    return int(m.group(1)) if m else None


def lecture_id_of(path_or_num: str | int) -> str | None:
    """Derive the canonical zero-padded id ``L01``..``L12`` from a path or int.

    Returns ``None`` if no lecture number can be determined.
    """
    num = path_or_num if isinstance(path_or_num, int) else lecture_num_of(str(path_or_num))
    if num is None:
        return None
    return lecture_id_from_num(num)


def lecture_id_from_num(num: int) -> str:
    """``4`` -> ``'L04'``. Zero-padded to two digits."""
    return f"L{num:02d}"


def num_from_lecture_id(lecture_id: str) -> int | None:
    """``'L04'`` -> ``4``. Returns ``None`` for malformed ids."""
    m = re.fullmatch(r"L(\d{2})", lecture_id)
    return int(m.group(1)) if m else None


def numeric_lecture_sort(paths: list[str]) -> list[str]:
    """Sort paths by integer lecture number, then by basename within a lecture.

    This is the project-critical replacement for cyper's lexical ``sorted()``:
    files with no resolvable lecture number sort *after* lectured ones (stable,
    by path) so discovery never crashes on a stray file.
    """

    def key(p: str) -> tuple[int, int, str]:
        num = lecture_num_of(p)
        norm = p.replace("\\", "/")
        base = norm.rsplit("/", 1)[-1].lower()
        # (has-no-number flag, lecture number, basename) — None sorts last.
        return (0 if num is not None else 1, num if num is not None else 0, base)

    return sorted(paths, key=key)


# --- curated deck-title map -------------------------------------------------

#: PDF basename -> human-readable deck/guide title. Filenames are PascalCase or
#: terse, and a few titles differ from the filename, so a curated map is required.
#: Adding Lecture 8/12 decks later is a one-line edit here.
DECK_TITLES: dict[str, str] = {
    # Lecture 1 — Intro & Version Control
    "IntroductionSB5MAI.pdf": "Introduction to Software Maintenance",
    "Lab - GIT.pdf": "Version Control Lab",
    "IntroLab.pdf": "Intro Lab — Maven & GitHub",
    "[Litt] Literature List.pdf": "Literature List",
    # Lecture 2 — Software Change, Concept Location, JHotDraw
    "ChangeLec.pdf": "Introduction to Software Change",
    "ChangeReqLec.pdf": "Change Initiation",
    "ConceptLocation.pdf": "Concept Location",
    "JHotDraw.pdf": "Introduction to JHotDraw Framework",
    "ChangeReqLab.pdf": "Change Request Lab",
    "CLLab1.pdf": "Concept Location Lab",
    # Lecture 3 — Impact Analysis, Processes, CI
    "ImpactAnalysis.pdf": "Impact and Feature Analysis",
    "IntroSwProcesses.pdf": "Introduction to Software Processes",
    "TeamProcesses.pdf": "Team Iterative Processes",
    "ContinuesIntegration.pdf": "Continuous Integration",
    "AnalysisLab1.pdf": "Impact Analysis Lab",
    "CILab.pdf": "Continuous Integration Lab",
    # Lecture 4 — Refactoring & Maintainable Code
    "Refactoring1.pdf": "Refactoring",
    "BetterCode.pdf": "Building Maintainable Software",
    "HighLevelRefactoring.pdf": "High Level Refactoring Patterns",
    "RefactoringLab1.pdf": "Refactoring Lab",
    # Lecture 5 — Actualization, Clean Architecture, OO Principles
    "Actualization.pdf": "Actualization",
    "Clean Architecture.pdf": "Clean Architecture",
    "OOPrinciples.pdf": "Object-Oriented Principles",
    "ActualizationLab.pdf": "Actualization Lab",
    # Lecture 6 — Clean Code & Design Patterns
    "CleanCode.pdf": "Clean Code",
    "DesignPrinciplesAndPatterns.pdf": "Design Principles and Patterns",
    # Lecture 7 — Software Testing
    "Software Testing.pdf": "Software Testing",
    "TestLab1.pdf": "Unit Testing Lab",
    # Lecture 9 — Verification / BDD
    "BDD.pdf": "Pragmatic BDD for Java",
    "BDDLab.pdf": "Behavior-Driven Testing Lab",
    # Lecture 10 — Conclusion & Worked Example
    "Conclusion of software change.pdf": "Conclusion of Software Change",
    "Example of software change.pptx.pdf": "Worked Example — Drawlets Framework",
    # Lecture 11 — Technical Debt
    "BeyondTechnicalDebt.pdf": "Beyond Technical Debt",
}


def deck_title_of(file: str) -> str:
    """Resolve a PDF basename to its curated human title.

    Falls back to a de-camel-cased, de-extension'd version of the filename so a
    newly added (unmapped) deck still gets a readable label rather than crashing.
    """
    base = file.replace("\\", "/").rsplit("/", 1)[-1]
    if base in DECK_TITLES:
        return DECK_TITLES[base]
    stem = base.rsplit(".", 1)[0]
    # Insert spaces at camelCase boundaries: 'HighLevelRefactoring' -> 'High Level Refactoring'.
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", stem)
    return spaced.replace("-", " ").replace("_", " ").strip() or stem


# --- document-kind classification ------------------------------------------


def doc_kind_of(file: str) -> str:
    """Classify a source PDF as ``deck`` | ``lab`` | ``meta``.

    - ``meta``: the literature/reading list (bracket-tagged ``[Litt]...``).
    - ``lab``: filenames containing ``lab`` (case-insensitive) — lab/exercise sheets.
    - ``deck``: everything else (the teaching content).
    """
    base = file.replace("\\", "/").rsplit("/", 1)[-1]
    low = base.lower()
    if low.startswith("[litt") or "literature" in low:
        return "meta"
    if "lab" in low:
        return "lab"
    return "deck"


# --- closed topic taxonomy (architecture §4.5) ------------------------------

#: The 16 controlled-vocabulary topics. Used identically for guide chunks and
#: MCQs so a quiz topic filter and a search topic filter agree. Closed list:
#: new lectures append topics rather than mint ad-hoc ones.
TOPICS: tuple[str, ...] = (
    "Software Change Process",
    "Concept Location",
    "Impact Analysis",
    "Refactoring",
    "Prefactoring",
    "Actualization",
    "Clean Architecture",
    "OO Principles",
    "Clean Code",
    "Design Patterns",
    "Software Testing",
    "BDD / Verification",
    "Technical Debt",
    "Software Processes / CI",
    "Version Control / Git",
    "JHotDraw Case Study",
)

#: Set form for O(1) membership checks at the API boundary.
TOPIC_SET: frozenset[str] = frozenset(TOPICS)

#: The closed difficulty vocabulary (architecture §4.4).
DIFFICULTIES: tuple[str, ...] = ("easy", "medium", "hard", "very-hard")
DIFFICULTY_SET: frozenset[str] = frozenset(DIFFICULTIES)


# --- lecture -> primary topics map ------------------------------------------

#: Each lecture maps to 1–3 primary topics from ``TOPICS``. Drives the website's
#: filter chips and documents the intended grounding for each guide/MCQ set.
#: Lecture 8 (empty) and Lecture 12 (no PDFs) are intentionally absent — they
#: slot in by adding a row here plus their data files, with zero other edits.
LECTURE_TOPICS: dict[str, list[str]] = {
    "L01": ["Version Control / Git", "Software Change Process"],
    "L02": ["Software Change Process", "Concept Location", "JHotDraw Case Study"],
    "L03": ["Impact Analysis", "Software Processes / CI"],
    "L04": ["Refactoring", "Prefactoring"],
    "L05": ["Actualization", "Clean Architecture", "OO Principles"],
    "L06": ["Clean Code", "Design Patterns"],
    "L07": ["Software Testing"],
    "L09": ["BDD / Verification"],
    "L10": ["Software Change Process", "JHotDraw Case Study"],
    "L11": ["Technical Debt"],
}

#: Curated human title per lecture, keyed by canonical id. Used by ``/api/lectures``
#: and as a fallback guide/MCQ title when the data files are absent.
LECTURE_TITLES: dict[str, str] = {
    "L01": "Introduction & Version Control",
    "L02": "Software Change, Concept Location & JHotDraw",
    "L03": "Impact Analysis, Software Processes & CI",
    "L04": "Refactoring & Maintainable Code",
    "L05": "Actualization, Clean Architecture & OO Principles",
    "L06": "Clean Code & Design Patterns",
    "L07": "Software Testing",
    "L09": "Software Verification & BDD",
    "L10": "Conclusion of Software Change",
    "L11": "Technical Debt",
}


def topics_for_lecture(lecture_id: str) -> list[str]:
    """Primary topics for a lecture id, or ``[]`` if unknown."""
    return list(LECTURE_TOPICS.get(lecture_id, []))


def lecture_title_of(lecture_id: str) -> str:
    """Human title for a lecture id, with a generic fallback for unknown ids."""
    num = num_from_lecture_id(lecture_id)
    fallback = f"Lecture {num}" if num is not None else lecture_id
    return LECTURE_TITLES.get(lecture_id, fallback)
