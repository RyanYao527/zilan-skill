from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5.5"
CONTEXT_CHAR_LIMIT = 5000


@dataclass(frozen=True)
class HarnessCase:
    case_id: str
    prompt: str
    reference_files: list[str]
    keywords: list[str]


@dataclass(frozen=True)
class HarnessResult:
    mode: str
    model: str
    case_id: str
    endpoint: str
    prompt: str
    reference_files: list[str]
    request: dict[str, Any]
    output_text: str | None = None
    response_id: str | None = None


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping.")
    return data


def _load_regression_case(root: Path, case_id: str) -> HarnessCase:
    data = _load_yaml(root / "tests" / "regression_cases.yaml")
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise ValueError("tests/regression_cases.yaml missing cases list.")

    for item in cases:
        if not isinstance(item, dict) or item.get("id") != case_id:
            continue
        expected = item.get("expected")
        if not isinstance(expected, dict):
            raise ValueError(f"{case_id} missing expected mapping.")
        return HarnessCase(
            case_id=case_id,
            prompt=str(item.get("prompt", "")),
            reference_files=[str(path) for path in expected.get("reference_files", [])],
            keywords=[str(keyword) for keyword in expected.get("keywords", [])],
        )

    raise ValueError(f"Unknown regression case: {case_id}")


def _default_model(root: Path) -> str:
    data = _load_yaml(root / "agents" / "openai.yaml")
    models = data.get("models", {})
    if isinstance(models, dict):
        openai_model = models.get("openai_api")
        if isinstance(openai_model, dict) and isinstance(openai_model.get("model_id"), str):
            return openai_model["model_id"]
    return DEFAULT_MODEL


def _default_prompt(root: Path) -> str:
    data = _load_yaml(root / "agents" / "openai.yaml")
    interface = data.get("interface")
    if isinstance(interface, dict) and isinstance(interface.get("default_prompt"), str):
        return interface["default_prompt"].strip()
    return "You are Zilan. Answer with precise Buddhist analysis and clear boundaries."


def _read_context_bundle(root: Path, reference_files: list[str]) -> str:
    parts: list[str] = []
    for rel_path in reference_files:
        path = root / rel_path
        if not path.exists() or not path.is_file():
            parts.append(f"## {rel_path}\n[missing]")
            continue

        text = path.read_text(encoding="utf-8")
        if len(text) > CONTEXT_CHAR_LIMIT:
            text = text[:CONTEXT_CHAR_LIMIT] + "\n[truncated for harness request]"
        parts.append(f"## {rel_path}\n{text}")
    return "\n\n".join(parts)


def build_request(root: Path, case: HarnessCase, model: str, prompt_override: str | None = None) -> dict[str, Any]:
    prompt = prompt_override or case.prompt
    developer_prompt = "\n\n".join(
        [
            _default_prompt(root),
            "Use only the supplied local repository context when making repository-specific claims.",
            "Cite local context filenames when relevant. State boundaries for practice guidance or textual inference.",
            "Local context bundle:",
            _read_context_bundle(root, case.reference_files),
        ]
    )

    return {
        "model": model,
        "reasoning": {"effort": "low"},
        "input": [
            {
                "role": "developer",
                "content": [{"type": "input_text", "text": developer_prompt}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}],
            },
        ],
    }


def _extract_output_text(response: dict[str, Any]) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"]

    chunks: list[str] = []
    output = response.get("output")
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    chunks.append(part["text"])
    return "\n".join(chunks)


def call_openai(request_body: dict[str, Any], api_key: str) -> dict[str, Any]:
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API request failed with HTTP {exc.code}: {body}") from exc


def run_harness(
    *,
    root: Path,
    case_id: str,
    model: str | None,
    prompt_override: str | None,
    live: bool,
) -> HarnessResult:
    case = _load_regression_case(root, case_id)
    selected_model = model or os.environ.get("OPENAI_MODEL") or _default_model(root)
    request_body = build_request(root, case, selected_model, prompt_override)

    if not live:
        return HarnessResult(
            mode="dry-run",
            model=selected_model,
            case_id=case.case_id,
            endpoint=OPENAI_RESPONSES_URL,
            prompt=prompt_override or case.prompt,
            reference_files=case.reference_files,
            request=request_body,
        )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required when --live is set.")

    response = call_openai(request_body, api_key)
    return HarnessResult(
        mode="live",
        model=selected_model,
        case_id=case.case_id,
        endpoint=OPENAI_RESPONSES_URL,
        prompt=prompt_override or case.prompt,
        reference_files=case.reference_files,
        request=request_body,
        output_text=_extract_output_text(response),
        response_id=response.get("id") if isinstance(response.get("id"), str) else None,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or run a minimal Zilan OpenAI Responses API harness.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--case", default="ZC-02", help="Regression case ID from tests/regression_cases.yaml.")
    parser.add_argument("--model", help="OpenAI model ID. Defaults to OPENAI_MODEL, agents/openai.yaml, or gpt-5.5.")
    parser.add_argument("--prompt", help="Override the regression case prompt.")
    parser.add_argument("--live", action="store_true", help="Call the OpenAI Responses API. Requires OPENAI_API_KEY.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    try:
        result = run_harness(
            root=args.root.resolve(),
            case_id=args.case,
            model=args.model,
            prompt_override=args.prompt,
            live=args.live,
        )
    except (OSError, RuntimeError, ValueError, yaml.YAMLError) as exc:
        print(f"openai-api-harness failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(f"mode: {result.mode}")
        print(f"model: {result.model}")
        print(f"case: {result.case_id}")
        print(f"endpoint: {result.endpoint}")
        print("reference_files:")
        for path in result.reference_files:
            print(f"  - {path}")
        if result.output_text is not None:
            print("\noutput_text:")
            print(result.output_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
