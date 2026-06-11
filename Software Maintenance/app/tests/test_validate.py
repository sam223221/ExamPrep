"""validate_mcqs gate: every §4 violation is caught; valid bank passes."""

import copy
import json

from app.validate_mcqs import main, validate_bank, validate_question


def _q(**over):
    base = {
        "id": "L04-Q001",
        "lecture_id": "L04",
        "topic": "Refactoring",
        "difficulty": "easy",
        "stem": "What does Extract Method improve?",
        "options": [
            {"key": "A", "text": "Readability"},
            {"key": "B", "text": "Compile time"},
            {"key": "C", "text": "Binary size"},
            {"key": "D", "text": "Network latency"},
        ],
        "answer": "A",
        "explanation": "Extract Method names a block, aiding readability (Refactoring1 p.14).",
        "source": {"deck": "Refactoring1.pdf", "page": 14},
    }
    base.update(over)
    return base


def _errs(q):
    return validate_question(q, where="t#0")


def test_valid_question_passes():
    assert _errs(_q()) == []


def test_catches_bad_id():
    assert _errs(_q(id="Q1")) != []
    assert _errs(_q(id="L4-Q001")) != []  # not zero-padded


def test_catches_id_lecture_mismatch():
    assert _errs(_q(id="L05-Q001", lecture_id="L04")) != []


def test_catches_wrong_option_count():
    q = _q()
    q["options"] = q["options"][:3]
    assert _errs(q) != []


def test_catches_bad_option_keys():
    q = _q()
    q["options"][3]["key"] = "E"
    assert _errs(q) != []


def test_catches_duplicate_option_keys():
    q = _q()
    q["options"][1]["key"] = "A"  # two A's
    assert _errs(q) != []


def test_catches_answer_not_in_ad():
    assert _errs(_q(answer="E")) != []


def test_catches_answer_not_matching_option():
    q = _q()
    # All keys A..D present but make answer reference a removed key by corrupting keys
    q["options"][0]["key"] = "B"  # now keys are B,B,C,D -> answer A matches none
    assert _errs(q) != []


def test_catches_empty_explanation():
    assert _errs(_q(explanation="   ")) != []


def test_catches_missing_source_fields():
    assert _errs(_q(source={"page": 14})) != []
    assert _errs(_q(source={"deck": "x.pdf"})) != []
    assert _errs(_q(source={"deck": "x.pdf", "page": -1})) != []


def test_catches_out_of_vocab_topic_and_difficulty():
    assert _errs(_q(topic="Made Up Topic")) != []
    assert _errs(_q(difficulty="trivial")) != []


def test_bank_catches_duplicate_id_across_files(tmp_path):
    f1 = tmp_path / "lecture-04-refactoring.json"
    f2 = tmp_path / "lecture-05-actualization.json"
    f1.write_text(json.dumps({"lecture_id": "L04", "questions": [_q()]}), encoding="utf-8")
    dup = copy.deepcopy(_q())  # same id L04-Q001 in a different file
    f2.write_text(json.dumps({"lecture_id": "L05", "questions": [dup]}), encoding="utf-8")
    errors = validate_bank([str(tmp_path)])
    assert any("duplicate id" in e for e in errors)


def test_bank_catches_duplicate_stem_across_files(tmp_path):
    f1 = tmp_path / "a.json"
    f2 = tmp_path / "b.json"
    f1.write_text(json.dumps({"lecture_id": "L04", "questions": [_q()]}), encoding="utf-8")
    q2 = _q(id="L05-Q001", lecture_id="L05")  # different id, SAME stem
    f2.write_text(json.dumps({"lecture_id": "L05", "questions": [q2]}), encoding="utf-8")
    errors = validate_bank([str(tmp_path)])
    assert any("duplicate stem" in e for e in errors)


def test_main_exit_codes(tmp_path, capsys):
    good = tmp_path / "lecture-04-refactoring.json"
    good.write_text(json.dumps({"lecture_id": "L04", "questions": [_q()]}), encoding="utf-8")
    assert main([str(tmp_path)]) == 0

    bad = tmp_path / "lecture-05-bad.json"
    bad.write_text(json.dumps({"lecture_id": "L05", "questions": [_q(id="bad")]}), encoding="utf-8")
    assert main([str(tmp_path)]) == 1


def test_main_empty_dir_is_ok(tmp_path):
    assert main([str(tmp_path)]) == 0  # no files -> nothing to validate, exit 0
