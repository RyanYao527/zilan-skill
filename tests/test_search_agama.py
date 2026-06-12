from pathlib import Path

from search_agama import iter_agama_markdown_files, search_agama

ROOT = Path(__file__).resolve().parents[1]


def test_agama_file_iterator_excludes_index_and_xml_sources() -> None:
    files = list(iter_agama_markdown_files(ROOT))
    names = {path.name for path in files}

    assert "agama-index.md" not in names
    assert "T0099-za-agama.md" in names
    assert all("_source" not in path.parts for path in files)


def test_search_returns_auditable_markdown_locations() -> None:
    matches = search_agama("無我", root=ROOT, limit=5)

    assert matches
    assert all(match.file.startswith("context/agama/") for match in matches)
    assert all(match.line > 0 for match in matches)
    assert any(match.juan for match in matches)


def test_search_filters_known_false_positive_phrases() -> None:
    matches = search_agama("非我", root=ROOT, limit=100)

    assert matches
    assert all("非我宜" not in match.text for match in matches)
    assert all("非我所說" not in match.text for match in matches)


def test_search_can_include_context_lines() -> None:
    matches = search_agama("緣起", root=ROOT, limit=1, context_lines=5)

    assert matches
    assert matches[0].context_before or matches[0].context_after
