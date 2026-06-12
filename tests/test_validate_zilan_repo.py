from pathlib import Path

from validate_zilan_repo import _check_platform_validation_doc, run_checks

ROOT = Path(__file__).resolve().parents[1]


def test_repository_invariants_pass_without_rebuilding_generated_files() -> None:
    failures, _warnings = run_checks(ROOT, check_generated=False, strict_yaml=False)

    assert failures == []


def test_repository_invariants_pass_with_strict_yaml() -> None:
    failures, warnings = run_checks(ROOT, check_generated=False, strict_yaml=True)

    assert failures == []
    assert warnings == []


def test_platform_validation_doc_status_mismatch_is_reported(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "platform-validation.md").write_text(
        """# Platform Validation Status

| Status | Meaning |
|---|---|
| `tested` | Runtime validation exists. |
| `definition-versioned` | Prompt is versioned. |
| `metadata-only` | Metadata exists. |
| `config-only` | Configuration exists. |
| `blocked` | Validation is blocked. |

| Platform route | Status | Last validated | Evidence | Boundary |
|---|---|---|---|---|
| Codex | `config-only` | 2026-06-10 | evidence | boundary |
""",
        encoding="utf-8",
    )
    validation = {
        "codex": {
            "status": "tested",
            "date": "2026-06-10",
            "scope": "ZC-01 through ZC-06 passed.",
        }
    }
    failures: list[str] = []

    _check_platform_validation_doc(tmp_path, validation, failures)

    assert any("status mismatch for Codex" in failure for failure in failures)
