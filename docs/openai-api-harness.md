# OpenAI API Harness

> Last updated: 2026-06-12

This repository includes a minimal OpenAI Responses API harness for Zilan. It loads `agents/openai.yaml`, selects a regression case from `tests/regression_cases.yaml`, bundles the expected local context files, and builds a Responses API request.

The harness is dry-run by default so CI does not require secrets:

```powershell
python scripts/openai_api_harness.py --case ZC-02 --json
```

To run a live request, set `OPENAI_API_KEY` and opt in explicitly:

```powershell
$env:OPENAI_API_KEY = "..."
python scripts/openai_api_harness.py --case ZC-02 --live --json
```

Optional knobs:

```powershell
python scripts/openai_api_harness.py --case ZC-03 --model gpt-5.5 --json
python scripts/openai_api_harness.py --prompt "孜澜，什么是因三相？" --json
```

## Status

- Default mode: dry-run request construction, covered by pytest.
- Live mode: implemented, but not run by CI and not marked end-to-end tested until a dated live transcript or summarized evidence is recorded.
- API surface: Responses API request with developer and user messages, `model`, `input`, and low reasoning effort.
- Credential boundary: `OPENAI_API_KEY` is required only with `--live` and must be supplied from the environment.

## Documentation Basis

The implementation follows OpenAI's current Responses API guidance:

- Latest model guidance names GPT-5.5 as the current latest model family: <https://developers.openai.com/api/docs/guides/latest-model.md>
- The text generation guide shows `responses.create` with `model`, `reasoning`, message-style `input`, and `response.output_text`: <https://developers.openai.com/api/docs/guides/text>
- The Responses API reference documents text `input` accepted by the create response endpoint: <https://developers.openai.com/api/docs/api-reference/responses/create.md>
- The API overview requires Bearer authentication and recommends loading API keys from server-side environment variables or key management: <https://developers.openai.com/api/docs/overview>
