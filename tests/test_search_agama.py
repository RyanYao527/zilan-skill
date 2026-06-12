import json
import subprocess
import sys
from pathlib import Path

from search_agama import iter_agama_markdown_files, search_agama, search_agama_passages

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "search_agama.py"


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


def test_search_can_extend_false_positive_filter() -> None:
    matches = search_agama("無我", root=ROOT, limit=10, false_positive_phrases=("無我；",))

    assert matches
    assert all("無我；" not in match.text for match in matches)


def test_search_can_aggregate_by_passage() -> None:
    passages = search_agama_passages("非我", root=ROOT, limit=5)

    assert passages
    assert all(passage.start_line <= passage.end_line for passage in passages)
    assert all(passage.matched_lines for passage in passages)
    assert len({(passage.file, passage.start_line, passage.end_line) for passage in passages}) == len(passages)


def test_search_json_cli_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--terms", "緣起", "--limit", "2", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert len(data) == 2
    assert {"file", "line", "juan", "text"}.issubset(data[0])


def test_search_text_cli_can_group_by_juan() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--terms", "緣起", "--limit", "2", "--group-by", "juan"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )

    assert "## context/agama/" in result.stdout
    assert "卷" in result.stdout
