from app.chunker import chunk_markdown, chunk_source


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
