from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

from search_agama import search_agama

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "README.zh.md",
    "README.en.md",
    "SKILL.md",
    "SKILL-en.md",
    "CODEX_REGRESSION_TESTS.md",
    "AGENT_UPGRADE_PORTABLE.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CONTRIBUTING-en.md",
    "agents/openai.yaml",
    "agents/zilan-claude-code.md",
    "agents/zilan-codex.md",
    "scripts/build_agama_context.py",
    "scripts/search_agama.py",
)

REQUIRED_CONTEXT_FILES = (
    "context/摄类学工具箱.md",
    "context/因明推理引擎.md",
    "context/心类学认知分析.md",
    "context/中观应成精要.md",
    "context/南传观禅指南.md",
    "context/模因机器视角下的佛教结集与传播.md",
    "context/agama/agama-index.md",
    "context/agama/T0001-chang-agama.md",
    "context/agama/T0026-zhong-agama.md",
    "context/agama/T0099-za-agama.md",
    "context/agama/T0125-ekottarika-agama.md",
    "context/agama/_source/T01n0001.xml",
    "context/agama/_source/T01n0026.xml",
    "context/agama/_source/T02n0099.xml",
    "context/agama/_source/T02n0125.xml",
)

GENERATED_AGAMA_FILES = (
    "context/agama/agama-index.md",
    "context/agama/T0001-chang-agama.md",
    "context/agama/T0026-zhong-agama.md",
    "context/agama/T0099-za-agama.md",
    "context/agama/T0125-ekottarika-agama.md",
)

REGRESSION_CASES = ("ZC-01", "ZC-02", "ZC-03", "ZC-04", "ZC-05", "ZC-06")


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_paths(root: Path, failures: list[str]) -> None:
    for rel_path in REQUIRED_FILES + REQUIRED_CONTEXT_FILES:
        if not (root / rel_path).exists():
            failures.append(f"Missing required path: {rel_path}")


def _check_regression_matrix(root: Path, failures: list[str]) -> None:
    text = (root / "CODEX_REGRESSION_TESTS.md").read_text(encoding="utf-8")
    for case in REGRESSION_CASES:
        if case not in text:
            failures.append(f"Missing regression case in CODEX_REGRESSION_TESTS.md: {case}")


def _check_agent_prompts(root: Path, failures: list[str]) -> None:
    codex_agent = (root / "agents/zilan-codex.md").read_text(encoding="utf-8")
    required_fragments = (
        "runtime: codex-sub-agent",
        "Codex 阿含检索规范",
        "引用阿含经时必须注明",
        "边界与限制",
    )
    for fragment in required_fragments:
        if fragment not in codex_agent:
            failures.append(f"agents/zilan-codex.md missing required fragment: {fragment}")


def _check_yaml(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    yaml_path = root / "agents/openai.yaml"
    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        message = "PyYAML is not installed; skipped agents/openai.yaml parse check."
        if strict_yaml:
            failures.append(message)
        else:
            warnings.append(message)
        return

    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - surface parser details to maintainers.
        failures.append(f"Failed to parse agents/openai.yaml: {exc}")
        return

    validation = data.get("validation", {}) if isinstance(data, dict) else {}
    if validation.get("codex", {}).get("status") != "tested":
        failures.append("agents/openai.yaml should mark validation.codex.status as tested.")
    for provider in ("openai_api", "deepseek", "glm", "qwen"):
        if provider not in validation:
            failures.append(f"agents/openai.yaml missing validation entry: {provider}")


def _check_agama_search(root: Path, failures: list[str]) -> None:
    matches = search_agama("無我|非我|緣起", root=root, limit=30)
    if not matches:
        failures.append("Agama smoke search returned no matches.")
        return
    if any("_source" in match.file for match in matches):
        failures.append("Agama smoke search should not return _source XML matches.")

    false_positive_check = search_agama("非我", root=root, limit=100)
    if any("非我宜" in match.text or "非我所說" in match.text for match in false_positive_check):
        failures.append("Agama search did not filter known false positives.")


def _run_build_agama(root: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(root / "scripts" / "build_agama_context.py")],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result


def _check_generated_agama(root: Path, failures: list[str]) -> None:
    result = _run_build_agama(root)
    if result.returncode != 0:
        failures.append(
            "build_agama_context.py failed:\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
        return
    after_first_run = {rel_path: _hash_file(root / rel_path) for rel_path in GENERATED_AGAMA_FILES}

    result = _run_build_agama(root)
    if result.returncode != 0:
        failures.append(
            "Second build_agama_context.py run failed:\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
        return
    after_second_run = {rel_path: _hash_file(root / rel_path) for rel_path in GENERATED_AGAMA_FILES}

    changed = [
        rel_path
        for rel_path in GENERATED_AGAMA_FILES
        if after_first_run[rel_path] != after_second_run[rel_path]
    ]
    if changed:
        failures.append("Agama Markdown generation is not idempotent: " + ", ".join(changed))
        return

    diff_result = subprocess.run(
        ["git", "diff", "--quiet", "--", *GENERATED_AGAMA_FILES],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if diff_result.returncode != 0:
        failures.append(
            "Generated Agama Markdown differs from committed content. "
            "Run scripts/build_agama_context.py and review the diff."
        )


def run_checks(
    root: Path = ROOT,
    *,
    check_generated: bool = False,
    strict_yaml: bool = False,
) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    root = root.resolve()

    _check_paths(root, failures)
    _check_regression_matrix(root, failures)
    _check_agent_prompts(root, failures)
    _check_yaml(root, failures, warnings, strict_yaml)
    _check_agama_search(root, failures)
    if check_generated:
        _check_generated_agama(root, failures)
    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate zilan-agent repository invariants.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument(
        "--check-generated",
        action="store_true",
        help="Rebuild Agama Markdown and fail if generated files change.",
    )
    parser.add_argument(
        "--strict-yaml",
        action="store_true",
        help="Fail when PyYAML is unavailable instead of warning.",
    )
    args = parser.parse_args()

    failures, warnings = run_checks(
        args.root,
        check_generated=args.check_generated,
        strict_yaml=args.strict_yaml,
    )
    for warning in warnings:
        print(f"WARN: {warning}")
    if failures:
        print("zilan-agent validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("zilan-agent validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
