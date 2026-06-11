"""In-memory MCQ bank: load, filter+sample, serve (answers stripped), and grade.

Architecture §5.3/§5.5: Quiz mode reads the per-lecture MCQ JSON bank directly —
exact metadata filtering, no vectors. The bank is loaded once at startup into an
index (``{lecture_id -> [questions]}`` plus a flat list) and pre-bucketed by
``lecture_id`` and ``difficulty`` so candidate selection is O(1).

Answer hygiene (the one app-specific security item, §9): the served quiz payload
NEVER includes ``answer``, ``explanation`` or ``source`` — options are reshuffled
server-side (deterministic when a ``seed`` is given) and grading happens only in
``grade()`` (which reveals answer/explanation/source for citations after grading).

The bank loader is defensive: a missing/empty ``data/mcqs/`` or an individual
malformed file must NOT crash the app — invalid questions are skipped and surfaced
in ``load_errors`` for the build gate / logs.
"""

from __future__ import annotations

import glob
import os
import random
from collections import defaultdict
from typing import Any

from app.lectures import (
    DIFFICULTIES,
    TOPIC_SET,
    lecture_title_of,
    num_from_lecture_id,
)
from app.validate_mcqs import OPTION_KEYS, validate_file, validate_question

#: Fields stripped from any payload that ships to the browser before grading.
#: ``source`` (deck + page) is withheld pre-grade too: it points at the exact slide,
#: so leaking it would let a curious user open ``/slide`` and read the answer before
#: submitting. ``/api/quiz/check`` still returns ``source`` so citations appear after
#: grading (architecture §9 answer-hygiene; FIX 2 security hardening).
_SECRET_FIELDS = ("answer", "explanation", "source")


def _question_topics(q: dict) -> set[str]:
    """Distinct closed-taxonomy topics a question covers: its ``topic`` plus any of
    its ``tags`` that are valid taxonomy topics.

    The MCQ bank was authored by parallel agents that tagged topics inconsistently —
    some put a cross-cutting topic only in ``tags`` rather than ``topic``, and ``tags``
    also holds many granular non-taxonomy labels (e.g. ``grep``, ``gof``). Restricting
    to ``TOPIC_SET`` keeps the offered chips and the filter on the closed taxonomy.
    """
    topics: set[str] = set()
    primary = q.get("topic")
    if primary in TOPIC_SET:
        topics.add(primary)
    tags = q.get("tags")
    if isinstance(tags, list):
        topics.update(t for t in tags if t in TOPIC_SET)
    return topics


def _topic_matches(q: dict, topic: str) -> bool:
    """True when a question matches the requested ``topic`` via its ``topic`` field OR
    its ``tags`` array (FIX 1 — cross-cutting tagged questions stay reachable)."""
    if q.get("topic") == topic:
        return True
    tags = q.get("tags")
    return isinstance(tags, list) and topic in tags


class QuizBank:
    """Loaded, validated, pre-bucketed MCQ bank with sampling and grading."""

    def __init__(self) -> None:
        self.questions: list[dict] = []  # flat list (valid questions only)
        self.by_id: dict[str, dict] = {}
        self.by_lecture: dict[str, list[dict]] = defaultdict(list)
        # (lecture_id, difficulty) -> [questions]; difficulty-only via _by_difficulty.
        self.by_lecture_difficulty: dict[tuple[str, str], list[dict]] = defaultdict(list)
        self.by_difficulty: dict[str, list[dict]] = defaultdict(list)
        self.load_errors: list[str] = []

    # --- loading ------------------------------------------------------------

    @classmethod
    def load(cls, mcq_root: str) -> QuizBank:
        """Build a bank from every ``*.json`` under ``mcq_root``. Never raises.

        Files are processed in sorted order. Within a file, only questions that
        pass ``validate_file`` structural checks are admitted; the rest are recorded
        in ``load_errors``. A duplicate id (across files) keeps the first occurrence.
        """
        bank = cls()
        if not mcq_root or not os.path.isdir(mcq_root):
            bank.load_errors.append(f"MCQ root {mcq_root!r} not found; bank is empty.")
            return bank

        for path in sorted(glob.glob(os.path.join(mcq_root, "*.json"))):
            questions, errors = validate_file(path)
            bank.load_errors.extend(errors)
            # ``validate_file`` aggregates errors across the file but still returns
            # every dict question; re-check each in isolation so one malformed
            # question never admits its (otherwise valid) siblings with bad data.
            for i, q in enumerate(questions):
                if validate_question(q, where=f"{os.path.basename(path)}#{i}"):
                    continue
                bank._add(q)
        return bank

    def _add(self, q: dict) -> None:
        qid = q["id"]
        if qid in self.by_id:
            self.load_errors.append(f"duplicate id {qid!r} ignored")
            return
        self.by_id[qid] = q
        self.questions.append(q)
        lec = q["lecture_id"]
        diff = q["difficulty"]
        self.by_lecture[lec].append(q)
        self.by_difficulty[diff].append(q)
        self.by_lecture_difficulty[(lec, diff)].append(q)

    # --- introspection for /api/lectures ------------------------------------

    def lectures_metadata(self) -> list[dict]:
        """One row per lecture present in the bank: id, num, title, topics, counts.

        ``topics`` is the sorted, distinct set of taxonomy topics that actually occur
        among the lecture's questions — derived from the loaded bank (each question's
        ``topic`` plus any taxonomy topics in its ``tags``), NOT the static
        lecture→topic map. This guarantees every chip the UI offers has at least one
        matching question and surfaces cross-cutting tagged topics (FIX 1).

        ``counts.by_difficulty`` is computed from the loaded bank so the UI shows
        only difficulties that actually have questions. Sorted numerically.
        """
        rows: list[dict] = []
        for lec in sorted(self.by_lecture, key=lambda x: (num_from_lecture_id(x) or 0, x)):
            qs = self.by_lecture[lec]
            counts = dict.fromkeys(DIFFICULTIES, 0)
            topics: set[str] = set()
            for q in qs:
                counts[q["difficulty"]] = counts.get(q["difficulty"], 0) + 1
                topics |= _question_topics(q)
            rows.append(
                {
                    "lecture_id": lec,
                    "lecture_num": num_from_lecture_id(lec),
                    "title": lecture_title_of(lec),
                    "topics": sorted(topics),
                    "counts": {"total": len(qs), "by_difficulty": counts},
                }
            )
        return rows

    # --- candidate selection ------------------------------------------------

    def _candidates(
        self,
        lecture: str | None,
        topic: str | None,
        difficulty: str | None,
    ) -> list[dict]:
        """Resolve a filtered candidate pool using the pre-built buckets.

        ``lecture`` is a canonical id (``L04``) or ``None``/``all``. ``topic`` and
        ``difficulty`` are optional exact filters. A question matches ``topic`` when
        its primary ``topic`` equals it OR the topic appears in its ``tags`` array —
        so cross-cutting questions whose topic lives only in ``tags`` stay reachable
        by the filter (FIX 1; the MCQ bank tags topics inconsistently).
        """
        lec = None if lecture in (None, "", "all") else lecture
        if lec and difficulty:
            pool = list(self.by_lecture_difficulty.get((lec, difficulty), []))
        elif lec:
            pool = list(self.by_lecture.get(lec, []))
        elif difficulty:
            pool = list(self.by_difficulty.get(difficulty, []))
        else:
            pool = list(self.questions)
        if topic:
            pool = [q for q in pool if _topic_matches(q, topic)]
        return pool

    # --- sampling + serving -------------------------------------------------

    def sample(
        self,
        *,
        lecture: str | None = None,
        topic: str | None = None,
        difficulty: str | None = None,
        n: int = 20,
        seed: int | None = None,
    ) -> list[dict]:
        """Return up to ``n`` SERVE-SAFE questions matching the filters.

        Deterministic when ``seed`` is given (same seed + filters -> same set and
        option order). Each returned question has ``answer``/``explanation`` removed
        and its options reshuffled so option position is never a tell.
        """
        pool = self._candidates(lecture, topic, difficulty)
        rng = random.Random(seed)
        picked = pool if len(pool) <= n else rng.sample(pool, n)
        # Stable, seed-driven order for the served set itself.
        ordered = list(picked)
        rng.shuffle(ordered)
        return [self._serve(q, rng) for q in ordered]

    @staticmethod
    def _serve(q: dict, rng: random.Random) -> dict:
        """Project a question to its public payload: no secrets, options reshuffled.

        Options keep their authored ``key`` (A..D) but are re-ordered, so the visual
        position carries no signal while the correct key the client submits still
        resolves against ``grade()``. ``answer``, ``explanation`` and ``source`` are
        dropped entirely (``_SECRET_FIELDS``) so neither the correct answer nor the
        slide that reveals it ever ships before grading.
        """
        opts = [{"key": o["key"], "text": o["text"]} for o in q["options"]]
        rng.shuffle(opts)
        served = {k: v for k, v in q.items() if k not in _SECRET_FIELDS and k != "options"}
        served["options"] = opts
        return served

    # --- grading ------------------------------------------------------------

    def grade(self, answers: list[dict[str, Any]]) -> dict:
        """Grade ``[{id, chosen}]`` against the bank.

        Returns ``{score, total, results:[{id, correct, answer, explanation, source}]}``.
        Unknown ids and malformed entries are flagged ``correct: false`` rather than
        raising, so a tampered/garbage body cannot 500 the endpoint (§8 edge cases).
        """
        results: list[dict] = []
        score = 0
        for entry in answers:
            qid = entry.get("id") if isinstance(entry, dict) else None
            chosen = entry.get("chosen") if isinstance(entry, dict) else None
            q = self.by_id.get(qid) if isinstance(qid, str) else None
            if q is None:
                results.append(
                    {
                        "id": qid,
                        "correct": False,
                        "answer": None,
                        "explanation": None,
                        "source": None,
                        "unknown": True,
                    }
                )
                continue
            correct = isinstance(chosen, str) and chosen in OPTION_KEYS and chosen == q["answer"]
            if correct:
                score += 1
            results.append(
                {
                    "id": q["id"],
                    "correct": correct,
                    "chosen": chosen,
                    "answer": q["answer"],
                    "explanation": q["explanation"],
                    "source": q["source"],
                }
            )
        return {"score": score, "total": len(answers), "results": results}
