from pathlib import Path

from openai_api_harness import OPENAI_RESPONSES_URL, build_request, run_harness
from openai_api_harness import _load_regression_case as load_regression_case

ROOT = Path(__file__).resolve().parents[1]


def test_openai_harness_builds_responses_api_request() -> None:
    case = load_regression_case(ROOT, "ZC-02")
    request = build_request(ROOT, case, "gpt-5.5")

    assert request["model"] == "gpt-5.5"
    assert request["input"][0]["role"] == "developer"
    assert request["input"][1]["role"] == "user"
    assert request["input"][1]["content"][0]["text"] == case.prompt
    assert "context/因明推理引擎.md" in request["input"][0]["content"][0]["text"]
    assert request["reasoning"]["effort"] == "low"


def test_openai_harness_dry_run_does_not_require_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = run_harness(root=ROOT, case_id="ZC-03", model="gpt-5.5", prompt_override=None, live=False)

    assert result.mode == "dry-run"
    assert result.endpoint == OPENAI_RESPONSES_URL
    assert result.output_text is None
    assert "context/摄类学工具箱.md" in result.reference_files


def test_openai_harness_live_requires_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    try:
        run_harness(root=ROOT, case_id="ZC-02", model="gpt-5.5", prompt_override=None, live=True)
    except RuntimeError as exc:
        assert "OPENAI_API_KEY" in str(exc)
    else:
        raise AssertionError("live OpenAI API harness should require OPENAI_API_KEY")
