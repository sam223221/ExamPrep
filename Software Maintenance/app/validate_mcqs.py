"""Build-time validation gate for the MCQ bank (architecture §4, §7 Phase-B gate).

Validates every ``data/mcqs/*.json`` file against the §4 schema and the cross-file
de-duplication rule, then exits non-zero on any violation so it is usable in CI:

    python -m app.validate_mcqs            # validate $MCQ_ROOT (or /data/mcqs)
    python -m app.validate_mcqs path/...   # validate explicit files/dirs

Checks per question:
  * schema-valid object with the required keys present and correctly typed
  * exactly 4 options keyed ``A``..``D`` (unique keys, non-empty text)
  * exactly one ``answer`` in ``A``..``D`` matching an option key
  * non-empty ``explanation``
  * ``source.deck`` (non-empty) and ``source.page`` (int >= 0) present
  * ``topic`` in the closed taxonomy; ``difficulty`` in the closed vocabulary
  * ``id`` matching ``L\\d\\d-Q\\d+`` and globally unique
  * ``lecture_id`` matching ``L\\d\\d`` and consistent with the ``id`` prefix
  * no duplicate question stems within OR across lectures (normalized compare)

The functions return structured error lists so the test-suite can assert each
violation is caught; ``main`` prints a human report and sets the exit code.
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys
from typing import Any

from app.lectures import DIFFICULTY_SET, TOPIC_SET

ID_RE = re.compile(r"^L\d{2}-Q\d+$")
LECTURE_ID_RE = re.compile(r"^L\d{2}$")
OPTION_KEYS = ("A", "B", "C", "D")
_REQUIRED_KEYS = (
    "id",
    "lecture_id",
    "topic",
    "difficulty",
    "stem",
    "options",
    "answer",
    "explanation",
    "source",
)


def normalize_stem(stem: str) -> str:
    """Lower-case, collapse whitespace, strip trailing punctuation for de-dup compare."""
    return re.sub(r"\s+", " ", str(stem).strip().lower()).rstrip("?.! ")


def validate_question(q: Any, *, where: str) -> list[str]:
    """Validate a single MCQ object. Returns a list of human-readable error strings."""
    errors: list[str] = []
    qid = q.get("id", "<no-id>") if isinstance(q, dict) else "<not-an-object>"
    tag = f"{where} [{qid}]"

    if not isinstance(q, dict):
        return [f"{tag}: question is not a JSON object"]

    for key in _REQUIRED_KEYS:
        if key not in q:
            errors.append(f"{tag}: missing required field '{key}'")

    # id
    qid_val = q.get("id")
    if not isinstance(qid_val, str) or not ID_RE.match(qid_val):
        errors.append(f"{tag}: 'id' must match L\\d\\d-Q\\d+ (got {qid_val!r})")

    # lecture_id + consistency with id prefix
    lec = q.get("lecture_id")
    if not isinstance(lec, str) or not LECTURE_ID_RE.match(lec):
        errors.append(f"{tag}: 'lecture_id' must match L\\d\\d (got {lec!r})")
    elif isinstance(qid_val, str) and ID_RE.match(qid_val) and not qid_val.startswith(lec + "-"):
        errors.append(f"{tag}: 'id' prefix does not match 'lecture_id' {lec!r}")

    # topic / difficulty against closed vocab
    topic = q.get("topic")
    if topic not in TOPIC_SET:
        errors.append(f"{tag}: 'topic' not in the closed taxonomy (got {topic!r})")
    difficulty = q.get("difficulty")
    if difficulty not in DIFFICULTY_SET:
        errors.append(f"{tag}: 'difficulty' not in {sorted(DIFFICULTY_SET)} (got {difficulty!r})")

    # stem
    stem = q.get("stem")
    if not isinstance(stem, str) or not stem.strip():
        errors.append(f"{tag}: 'stem' must be a non-empty string")

    # options: exactly 4, keyed A..D, unique, non-empty text
    options = q.get("options")
    keys_seen: list[str] = []
    if not isinstance(options, list) or len(options) != 4:
        errors.append(f"{tag}: 'options' must be a list of exactly 4 objects")
    else:
        for idx, opt in enumerate(options):
            if not isinstance(opt, dict):
                errors.append(f"{tag}: option {idx} is not an object")
                continue
            key = opt.get("key")
            text = opt.get("text")
            if key not in OPTION_KEYS:
                errors.append(f"{tag}: option {idx} 'key' must be one of A..D (got {key!r})")
            else:
                keys_seen.append(key)
            if not isinstance(text, str) or not text.strip():
                errors.append(f"{tag}: option {key!r} 'text' must be a non-empty string")
        if sorted(keys_seen) != list(OPTION_KEYS):
            errors.append(f"{tag}: option keys must be exactly A,B,C,D with no duplicates")

    # answer: exactly one, in A..D, matching an existing option key
    answer = q.get("answer")
    if answer not in OPTION_KEYS:
        errors.append(f"{tag}: 'answer' must be one of A..D (got {answer!r})")
    elif keys_seen and answer not in keys_seen:
        errors.append(f"{tag}: 'answer' {answer!r} does not match any option key")

    # explanation
    explanation = q.get("explanation")
    if not isinstance(explanation, str) or not explanation.strip():
        errors.append(f"{tag}: 'explanation' must be a non-empty string")

    # source.deck + source.page
    source = q.get("source")
    if not isinstance(source, dict):
        errors.append(f"{tag}: 'source' must be an object with 'deck' and 'page'")
    else:
        deck = source.get("deck")
        page = source.get("page")
        if not isinstance(deck, str) or not deck.strip():
            errors.append(f"{tag}: 'source.deck' must be a non-empty string")
        if not isinstance(page, int) or isinstance(page, bool) or page < 0:
            errors.append(f"{tag}: 'source.page' must be an int >= 0 (got {page!r})")

    return errors


def validate_file(path: str) -> tuple[list[dict], list[str]]:
    """Validate one MCQ JSON file's structure and its questions.

    Returns ``(questions, errors)``. File-level structural problems short-circuit
    with an empty question list.
    """
    errors: list[str] = []
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"{path}: cannot read/parse JSON — {exc}"]

    if not isinstance(data, dict):
        return [], [f"{path}: top-level JSON must be an object"]

    lec_id = data.get("lecture_id")
    if not isinstance(lec_id, str) or not LECTURE_ID_RE.match(lec_id):
        errors.append(f"{path}: file 'lecture_id' must match L\\d\\d (got {lec_id!r})")

    questions = data.get("questions")
    if not isinstance(questions, list):
        errors.append(f"{path}: 'questions' must be a list")
        return [], errors

    valid_questions: list[dict] = []
    for i, q in enumerate(questions):
        qerrors = validate_question(q, where=f"{os.path.basename(path)}#{i}")
        errors.extend(qerrors)
        if isinstance(q, dict):
            valid_questions.append(q)
    return valid_questions, errors


def _discover_json(paths: list[str]) -> list[str]:
    """Expand dirs to ``*.json`` and keep explicit files, numerically/lexically sorted."""
    out: list[str] = []
    for p in paths:
        if os.path.isdir(p):
            out.extend(glob.glob(os.path.join(p, "*.json")))
        elif p.endswith(".json"):
            out.append(p)
    return sorted(set(out))


def validate_bank(paths: list[str]) -> list[str]:
    """Validate every MCQ file under ``paths`` plus cross-file uniqueness rules.

    Returns the full list of errors (empty == valid). Cross-file checks: globally
    unique ``id`` and no duplicate normalized stems anywhere in the bank.
    """
    errors: list[str] = []
    seen_ids: dict[str, str] = {}
    seen_stems: dict[str, str] = {}

    for path in _discover_json(paths):
        questions, file_errors = validate_file(path)
        errors.extend(file_errors)
        for q in questions:
            qid = q.get("id")
            base = os.path.basename(path)
            if isinstance(qid, str):
                if qid in seen_ids:
                    errors.append(f"{base} [{qid}]: duplicate id (also in {seen_ids[qid]})")
                else:
                    seen_ids[qid] = base
            stem = q.get("stem")
            if isinstance(stem, str) and stem.strip():
                norm = normalize_stem(stem)
                if norm in seen_stems:
                    errors.append(f"{base} [{qid}]: duplicate stem (also in {seen_stems[norm]})")
                else:
                    seen_stems[norm] = f"{base} [{qid}]"
    return errors


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns a process exit code (0 = valid, 1 = violations)."""
    argv = list(sys.argv[1:] if argv is None else argv)
    targets = argv or [os.environ.get("MCQ_ROOT", "/data/mcqs")]
    files = _discover_json(targets)
    if not files:
        print(f"No MCQ JSON files found under {targets}. Nothing to validate.")
        return 0

    errors = validate_bank(targets)
    if errors:
        print(f"MCQ validation FAILED — {len(errors)} problem(s) across {len(files)} file(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"MCQ validation OK — {len(files)} file(s) valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
