# Runtime Validation Log

> Last updated: 2026-06-12

This log records manual runtime validation evidence for zilan-agent. It complements CI and repository invariant checks; it does not replace `python scripts/validate_zilan_repo.py --check-generated --strict-yaml`, pytest, ruff, or platform status maintenance in `agents/openai.yaml` and `docs/platform-validation.md`.

## Evidence Rules

Every runtime validation entry should record:

- exact date
- runtime or provider
- model or tool version when known
- repository commit or branch
- prompt set used
- case-level result
- observed failures or limitations
- repository checks run after the session
- whether full transcripts are committed, summarized, or unavailable

Use conservative status labels:

| Status | Meaning |
|---|---|
| `pass` | The case met its documented expected behavior in the observed runtime. |
| `partial` | The case mostly worked but had a material gap that should be tracked. |
| `fail` | The case did not meet expected behavior. |
| `blocked` | The case could not be executed because of missing access, tooling, or provider failure. |
| `not-run` | The case remains in scope but was not executed in this session. |

## 2026-06-10 Codex Baseline

| Field | Value |
|---|---|
| Runtime | Codex |
| Scope | ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` |
| Evidence source | Existing project validation notes in `agents/openai.yaml` and `docs/platform-validation.md` |
| Repository context | Local Markdown context and explicit sub-agent triggers for ZC-04 through ZC-06 |
| Transcript status | Full transcripts are not committed in this repository. Treat this entry as a summarized baseline, not a transcript archive. |
| Follow-up | Re-run and append a transcript-backed entry after meaningful prompt, routing, or context changes. |

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Lightweight daily-practice support; no sub-agent expected. |
| ZC-02 | Skill concept lookup | `pass` | Expected to use or follow `context/因明推理引擎.md`. |
| ZC-03 | Skill cross-domain explanation | `pass` | Expected to combine `context/摄类学工具箱.md` and `context/心类学认知分析.md`. |
| ZC-04 | Explicit sub-agent Agama search | `pass` | Explicit sub-agent trigger; Agama Markdown search expected, with `_source/` excluded. |
| ZC-05 | Explicit sub-agent cross-domain research | `pass` | Explicit sub-agent trigger; expected to connect Agama, Collected Topics, Buddhist logic, Madhyamaka, and vipassana. |
| ZC-06 | Long report output | `pass` | Explicit sub-agent trigger; file output expected only because the prompt requested it. |

### Known Limits

- This entry is a summarized baseline. It does not contain full model transcripts.
- CI validates case inventory, prompt contracts, search behavior, and repository invariants; it does not grade answer quality.
- Future prompt or routing changes should append a new entry rather than editing this historical baseline in place.

## Next Validation Entries

Use this template for future manual sessions:

```markdown
## YYYY-MM-DD Runtime Name

| Field | Value |
|---|---|
| Runtime |  |
| Provider / model |  |
| Tool version |  |
| Repository commit |  |
| Prompt set |  |
| Transcript status | committed / summarized / unavailable |
| Repository checks |  |

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `not-run` |  |
| ZC-02 | Skill concept lookup | `not-run` |  |
| ZC-03 | Skill cross-domain explanation | `not-run` |  |
| ZC-04 | Explicit sub-agent Agama search | `not-run` |  |
| ZC-05 | Explicit sub-agent cross-domain research | `not-run` |  |
| ZC-06 | Long report output | `not-run` |  |
```
