# Platform Validation Status

> Last updated: 2026-06-12

This document is the source of truth for Zilan's platform validation status. It keeps engineering checks, manual runtime validation, provider metadata, and scholarly collation boundaries separate so the project does not overclaim platform support.

## Status Vocabulary

| Status | Meaning |
|---|---|
| `tested` | A documented runtime or manual regression pass exists for the route, with date, scope, and known limits. |
| `definition-versioned` | The prompt or agent definition is versioned in this repository, but runtime behavior depends on a local tool or provider setup not validated by CI. |
| `harness-ready` | A runnable harness exists and is covered by repository checks, but live end-to-end provider execution has not been recorded. |
| `metadata-only` | Portable metadata exists, but there is no runnable end-to-end harness in this repository yet. |
| `config-only` | Provider configuration exists, but the route has not been end-to-end tested. |
| `blocked` | Validation is intentionally blocked by missing access, provider behavior, or an unresolved integration issue. |

## Current Matrix

| Platform route | Status | Last validated | Evidence | Boundary |
|---|---|---|---|---|
| Codex | `tested` | 2026-06-12 | `docs/runtime-validation-log.md`, `CODEX_REGRESSION_TESTS.md`, `tests/regression_cases.yaml`, `agents/zilan-codex.md` | ZC-01 through ZC-06 passed in Codex on 2026-06-12 with local Markdown context. ZC-04 through ZC-06 used parent-observed sub-agent spawns. CI validates the regression inventory and tooling; it does not grade answer quality. |
| Claude Code | `tested` | 2026-06-12 | `docs/runtime-validation-log.md`, `CODEX_REGRESSION_TESTS.md`, `tests/regression_cases.yaml`, `agents/zilan-claude-code.md` | ZC-01 through ZC-06 passed through Claude Code CLI 2.1.169 with the repository agent prompt loaded. The noninteractive direct prompt-file route is tested; background auto-spawn behavior is not separately audited. |
| OpenAI API | `harness-ready` | Dry-run harness: 2026-06-12 | `scripts/openai_api_harness.py`, `tests/test_openai_api_harness.py`, `docs/openai-api-harness.md`, `agents/openai.yaml` | The harness builds OpenAI Responses API requests and is covered by pytest. Live `--live` execution is not yet recorded and requires `OPENAI_API_KEY`. |
| DeepSeek | `config-only` | Not end-to-end tested | `agents/openai.yaml`, `AGENT_UPGRADE_PORTABLE.md` | The Anthropic-compatible endpoint issue is documented in `AGENT_UPGRADE_PORTABLE.md`; do not mark this route tested until that integration is verified. |
| GLM | `config-only` | Not end-to-end tested | `agents/openai.yaml` | Provider metadata exists, but no runtime transcript or harness is committed. |
| Qwen | `config-only` | Not end-to-end tested | `agents/openai.yaml` | Provider metadata exists, but no runtime transcript or harness is committed. |

## Validation Layers

### Repository CI

Repository checks prove that required files, regression case metadata, YAML structure, generated Agama Markdown, and search tooling are coherent.

Recommended release check:

```powershell
python scripts/validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest
python -m ruff check scripts tests
```

These checks should pass before merging prompt, context, script, or platform metadata changes.

### Codex Runtime

Codex answer quality is validated manually with ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml`. Runtime evidence and transcript availability are tracked in `docs/runtime-validation-log.md`.

Minimum runtime protocol:

1. Run each prompt in a fresh or clearly controlled Codex session.
2. For ZC-04 through ZC-06, use explicit wording such as "spawn a zilan agent" so sub-agent routing is tested.
3. Confirm local context is used instead of unsupported guessing.
4. Confirm Agama citations include sutra name, CBETA ID when available, fascicle or passage information, and local file references when possible.
5. Confirm the answer states boundaries for practice guidance, textual inference, or non-exhaustive search.

### Agama Search Smoke

Use the search helper to verify the local Markdown corpus and false-positive filters:

```powershell
python scripts/search_agama.py --terms "無我|非我|無我所|五陰|五受陰|緣起" --limit 10
python scripts/search_agama.py --terms "非我" --passages --group-by juan --limit 10
python scripts/search_agama.py --terms "緣起" --json --limit 5
```

The helper excludes `_source/` XML by default and filters known collisions such as `非我宜`, `非我所說`, and `無我活為`.

### Claude Code Runtime

Claude Code answer quality is validated manually with the same ZC prompt family where practical. The 2026-06-12 run used `claude -p` noninteractive mode with `agents/zilan-claude-code.md` appended as the agent prompt and local repository tools enabled per case. Treat this as validation of the Claude Code CLI plus repository prompt route, not as proof that every user's installed `~/.claude/skills` path is current.

### OpenAI API Harness

The OpenAI API route has a minimal harness at `scripts/openai_api_harness.py`. Dry-run mode builds a Responses API request from `agents/openai.yaml`, `tests/regression_cases.yaml`, and bounded local context. Live mode requires `OPENAI_API_KEY` and `--live`; do not mark OpenAI API `tested` until a dated live run is recorded.

### Provider Routes

Before changing a route from `metadata-only`, `harness-ready`, or `config-only` to `tested`, commit or document:

- date of validation
- provider and model ID
- prompt set used
- whether local context was supplied and how
- transcript or summarized evidence
- failure modes observed
- exact repository checks run

## Scholarly Collation Boundary

The local Agama Markdown files are a searchable working corpus, not a critical edition. Publication-level citation should verify quoted passages against CBETA XML-P5 and, when relevant, compare parallel Chinese translations or Pali parallels. Keyword search results should be deduplicated by sutra, fascicle, and passage before being treated as evidence.

## Update Rule

Do not describe a platform as "supported", "validated", or "tested" unless it meets the status definition above. When in doubt, keep the status conservative and record the next validation step instead.
