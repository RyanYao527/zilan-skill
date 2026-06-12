# Maintenance Roadmap

> Last updated: 2026-06-12

This roadmap records engineering maintenance state and next priorities for zilan-agent. It is not platform validation evidence. Platform status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## Current Baseline

| Area | Current state |
|---|---|
| CI | GitHub Actions runs repository invariants, generated Agama idempotency checks, pytest, ruff, and Agama search smoke tests. |
| Repository invariants | `scripts/validate_zilan_repo.py` checks required files, context files, YAML shape, regression inventory, platform status consistency, agent prompt contracts, and Agama search behavior. |
| Regression inventory | `CODEX_REGRESSION_TESTS.md` is mirrored by `tests/regression_cases.yaml`; CI validates structure, resources, and case IDs. |
| Platform status | `agents/openai.yaml` is the machine-readable source; `docs/platform-validation.md` is the human-readable validation record. |
| Runtime validation | `docs/runtime-validation-log.md` records manual runtime validation sessions and transcript availability. |
| Agama search | `scripts/search_agama.py` searches Markdown only by default, filters known false positives, supports passage grouping, emits JSON, and provides stable `citation` / `passage_citation` fields. |
| Agent prompts | Codex and Claude agent prompts are checked for the Agama citation contract and must prefer `search_agama.py --json` citation fields when available. |

## Operating Rules

- Run `python scripts/validate_zilan_repo.py --check-generated --strict-yaml`, `python -m pytest`, and `python -m ruff check scripts tests` before merging prompt, context, script, or platform metadata changes.
- Keep platform claims conservative. Do not mark a route `tested` without dated validation evidence in `docs/platform-validation.md`.
- Use local Agama Markdown as a searchable working corpus. Use `_source/` XML only for collation, source verification, or CBETA-specific checks.
- Preserve stable citation output in `search_agama.py`; downstream prompts and regression expectations depend on `citation` and `passage_citation`.
- Prefer small PRs with one maintenance theme each, and keep unrelated content or wording refactors out of engineering PRs.

## Near-Term Priorities

| Priority | Track | Work | Done when |
|---|---|---|---|
| P0 | Runtime validation | Re-run ZC-01 through ZC-06 after prompt or routing changes and append to `docs/runtime-validation-log.md`. | A dated manual validation note records prompts, observed behavior, failures, transcript status, and checks run. |
| P1 | Validation evidence | Replace summarized baselines with transcript-backed Codex and Claude Code sessions where practical. | Runtime results are auditable without relying on chat history. |
| P1 | Claude Code route | Run the Claude Code agent definition against the same lightweight, concept, Agama, and long-report scenarios. | `docs/platform-validation.md` can move Claude Code beyond `definition-versioned` only if evidence supports it. |
| P1 | OpenAI API route | Build a small API harness that loads the portable metadata and runs a bounded prompt suite. | OpenAI API status has runnable evidence, not just YAML metadata. |
| P1 | Provider routes | Validate or explicitly block DeepSeek, GLM, and Qwen route assumptions. | Each route has a dated tested or blocked entry with provider/model details and failure modes. |
| P1 | Agama citations | Extract or preserve finer-grained sutra or section markers when present in the Markdown. | Search output can cite representative passages beyond file, line, and fascicle where the source supports it. |
| P2 | Scholarly collation | Add a stricter collation path from Markdown hits back to CBETA XML-P5 and relevant parallels. | Publication-level work has a documented verification route. |
| P2 | Installation docs | Clarify install paths and activation expectations for Codex, Claude Code, and portable API use. | New users can install the skill or agent without reading implementation history. |
| P2 | Release hygiene | Add version or changelog conventions once the repository stabilizes. | Changes can be summarized for users without reading merged PRs. |

## Manual Validation Checklist

Use this checklist before changing a platform route from metadata/config status to tested:

1. Record the exact date, provider, model, tool/runtime version, and repository commit.
2. Run the relevant ZC prompts from `CODEX_REGRESSION_TESTS.md` or a documented equivalent.
3. Confirm context loading, citation behavior, boundary statements, and sub-agent routing where applicable.
4. Record failures and follow-up fixes, not only successful final answers.
5. Run the repository checks listed in this document.
6. Update `agents/openai.yaml` and `docs/platform-validation.md` in the same PR.

## Backlog Guardrails

- Do not add broad abstractions unless they protect a real contract already used by prompts, scripts, tests, or documentation.
- Do not treat smoke tests as answer-quality grading. Manual runtime review remains required for agent behavior.
- Do not upgrade scholarly claims beyond the evidence in the local corpus and documented collation route.
