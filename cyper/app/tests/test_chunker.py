from app.chunker import chunk_markdown, chunk_source, chunk_qna, chunk_commands


def test_chunk_source_attaches_page():
    text = "<!-- page:1 -->\nIntro about firewalls.\n<!-- page:2 -->\nIDS detail here."
    chunks = chunk_source(text, file="L04.pdf", topic="Firewalls & IDS", max_chars=200)
    assert any(c["page"] == 1 for c in chunks)
    assert any(c["page"] == 2 for c in chunks)
    assert all(c["type"] == "source" for c in chunks)
    assert all(c["topic"] == "Firewalls & IDS" for c in chunks)


def test_chunk_markdown_splits_by_heading():
    md = "# T\n## Key Concepts\nA.\n## Glossary\nB."
    chunks = chunk_markdown(md, file="04-firewalls.md", topic="Firewalls & IDS")
    titles = {c["title"] for c in chunks}
    assert "Key Concepts" in titles and "Glossary" in titles
    assert all(c["type"] == "guide" for c in chunks)
    assert all(c["difficulty"] == "" for c in chunks)


def test_chunk_qna_parses_questions_and_difficulty():
    md = (
        "# 06. Denial of Service — Simulated Open-Book Questions\n"
        "### [EASY] What is a SYN flood?\n"
        "**Answer:** It exhausts the TCP backlog.\n"
        "### [VERY HARD] Given a capture, identify the attack and mitigation.\n"
        "**Answer:** Analyze the half-open connections, then enable SYN cookies.\n"
    )
    chunks = chunk_qna(md, file="06-denial-of-service.md", topic="Denial Of Service")
    assert len(chunks) == 2
    assert all(c["type"] == "qna" for c in chunks)
    assert chunks[0]["difficulty"] == "easy"
    assert chunks[1]["difficulty"] == "very-hard"
    # question goes into the title; both Q and A end up in the embedded text
    assert chunks[0]["title"] == "What is a SYN flood?"
    assert "SYN flood" in chunks[0]["text"]
    assert "TCP backlog" in chunks[0]["text"]
    # the "**Answer:**" label is stripped from the stored body
    assert "**Answer:**" not in chunks[0]["text"]


def test_chunk_commands_splits_examples_and_is_fence_aware():
    md = (
        "# 02. Vulnerability Assessment — Commands & Code Examples\n"
        "### Full TCP SYN scan\n"
        "**What:** stealthy port scan.\n"
        "```bash\n"
        "nmap -sS -p- 10.0.0.5\n"
        "### this is a comment-like line inside a fence, NOT a new example\n"
        "```\n"
        "**Notes:** needs root.\n"
        "### Service/version detection\n"
        "**What:** identify services.\n"
        "```bash\n"
        "nmap -sV 10.0.0.5\n"
        "```\n"
    )
    chunks = chunk_commands(md, file="02-vulnerability-assessment.md", topic="Vulnerability Assessment")
    # fence-aware: the '###' inside the code block must NOT create a 3rd example
    assert len(chunks) == 2
    assert all(c["type"] == "cmd" for c in chunks)
    assert chunks[0]["title"] == "Full TCP SYN scan"
    assert chunks[1]["title"] == "Service/version detection"
    # the command text is preserved in the chunk for embedding
    assert "nmap -sS -p- 10.0.0.5" in chunks[0]["text"]
    assert "comment-like line inside a fence" in chunks[0]["text"]
