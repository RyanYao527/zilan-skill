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

## 2026-06-12 Codex Rerun

| Field | Value |
|---|---|
| Runtime | Codex |
| Provider / model | Codex current session; exact model ID not recorded in repository evidence |
| Tool version | Codex session with `multi_agent_v1.spawn_agent` and `multi_agent_v1.wait_agent` available |
| Repository commit | `8079c1b7a455cb60e2c6560577c45d452f53b6f4` |
| Branch | `codex/runtime-validation-rerun-20260612` |
| Prompt set | ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml` |
| Transcript status | Summarized here; full transcripts are not committed. Parent session recorded sub-agent IDs for ZC-04 through ZC-06. ZC-06 also wrote a report to `C:\tmp\zilan-validation-20260612-ZC06.md`, outside the repository. |
| Repository checks | `python -m ruff check scripts tests` pass; `python -m pytest` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass |
| Overall result | `pass` with the limitations below |

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Main Codex session, no sub-agent. Covered daily-practice support with psychology / vipassana framing, avoided scripture overreach, and stated practice boundaries. |
| ZC-02 | Skill concept lookup | `pass` | Main Codex session, no sub-agent. Explained the three characteristics of a valid reason: `遍是宗法性`, `同品定有性`, and `异品遍无性`, with the expected Collected Topics relation. |
| ZC-03 | Skill cross-domain explanation | `pass` | Main Codex session, no sub-agent. Combined Collected Topics and Buddhist psychology, distinguishing fact, concept label, feeling / perception, and anger, with a practice boundary. |
| ZC-04 | Explicit sub-agent Agama search | `pass` | Spawned sub-agent `019eba77-1d09-79e1-b853-ada7ab3ff31c` (`Popper`). It searched local Agama Markdown, excluded `_source/` XML, reported 282 script matches, grouped the evidence into six doctrinal categories, supplied CBETA / fascicle / local-line citations, and stated search limits. |
| ZC-05 | Explicit sub-agent cross-domain research | `pass` | Spawned sub-agent `019eba77-5d1a-7032-9bec-2d71c2715f9b` (`Russell`). It connected Agama, Collected Topics, Buddhist logic, Madhyamaka, and vipassana, supplied local citations, and stated practice and textual inference boundaries. |
| ZC-06 | Long report output | `pass` | Spawned sub-agent `019eba77-7e15-7992-886b-4a9b9b866a25` (`Raman`). It wrote `C:\tmp\zilan-validation-20260612-ZC06.md`, searched local Agama Markdown with `_source/` excluded, reported passage counts by corpus, produced a long report with citations, and stated non-exhaustive / non-practice-certification boundaries. |

### Sub-Agent Evidence

| Case | Parent-observed agent ID | Evidence |
|---|---|---|
| ZC-04 | `019eba77-1d09-79e1-b853-ada7ab3ff31c` | Completion notification returned the Agama search summary, search commands, match counts, representative citations, and boundary statement. |
| ZC-05 | `019eba77-5d1a-7032-9bec-2d71c2715f9b` | Completion notification returned the cross-domain doctrinal answer, representative citations, and boundary statement. |
| ZC-06 | `019eba77-7e15-7992-886b-4a9b9b866a25` | Completion notification confirmed file output at `C:\tmp\zilan-validation-20260612-ZC06.md`; the file was read and summarized for this log. |

### Known Limits

- Full prompts and answer transcripts are summarized, not committed verbatim.
- Sub-agents cannot self-observe the parent session's spawn handle, so their self-reports mark sub-agent verification as partial. Parent-observed agent IDs are the runtime evidence for ZC-04 through ZC-06.
- ZC-04 surfaced residual false positives such as non-doctrinal `無我` contexts that require manual screening after keyword search.
- One shell attempt to read a local installed skill path failed under the Windows sandbox. The rerun used the repository-local `SKILL.md`, agent prompt, and context files successfully.

## 2026-06-12 Claude Code Rerun

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code 2.1.169; JSON model usage reported `deepseek-v4-pro[1m]` under the local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` appended as the agent prompt |
| Repository commit | `1cae652fec50132e69c526113ba644dfeba21cbf` |
| Branch | `codex/claude-openai-validation` |
| Prompt set | ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml` |
| Transcript status | Summarized here; full JSON outputs are not committed. ZC-06 also wrote a report to `C:\tmp\zilan-claude-validation-20260612-ZC06.md`, outside the repository. |
| Repository checks | `python -m ruff check scripts tests` pass; `python -m pytest` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass |
| Overall result | `pass` with the limitations below |

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Claude Code session `edbefc6f-5344-48f8-b4c8-8e47c9f25ab4`; used `Read` for `摄类学工具箱.md`, `心类学认知分析.md`, and `南传观禅指南.md`; no `Bash` or `Write`; boundary statement present. |
| ZC-02 | Skill concept lookup | `pass` | Session `c5e3599d-d54d-4666-b27f-4f62fc8aa285`; used `Read` for `因明推理引擎.md` and `摄类学工具箱.md`; explained `遍是宗法性`, `同品定有性`, and `异品遍无性`; boundary statement present. |
| ZC-03 | Skill cross-domain explanation | `pass` | Session `a51d0a1c-fb53-4600-872e-201821b02461`; used `Read` for `摄类学工具箱.md` and `心类学认知分析.md`; distinguished fact, concept label, `受`, `想`, and `瞋`; boundary statement present. |
| ZC-04 | Explicit agent Agama search | `pass` | Initial session `2e25ea9e-761c-4371-b658-e10c29f47b6f` completed classification but looked for `~/.claude/skills/zilan-agent/scripts/search_agama.py`, which was not installed locally. Rerun session `6a7da561-6c7a-4ba0-8e8d-1e2f66c43629` used the explicit repository root and `scripts/search_agama.py --json`; local Markdown only; boundary statement present. |
| ZC-05 | Explicit agent cross-domain research | `pass` | Session `13d6aac6-0594-4277-8431-ccaf4bfa057d`; used `Read` and `Bash`; connected Agama, Collected Topics, Buddhist logic, Madhyamaka, and vipassana; supplied local citations and practice / textual boundaries. |
| ZC-06 | Long report output | `pass` | Session `7e4c7b98-e351-4abd-ae8e-03ac3b3455bb`; used `Read`, `Bash`, and `Write`; wrote `C:\tmp\zilan-claude-validation-20260612-ZC06.md`; independent file check found 352 lines; repository worktree remained clean. |

### Known Limits

- This validates Claude Code CLI noninteractive execution with the repository agent prompt loaded directly. It does not independently prove every user's installed `~/.claude/skills/zilan-agent` path is current.
- Background auto-spawn behavior was not separately audited; explicit ZC-04 through ZC-06 prompts were executed through the loaded agent prompt in `claude -p`.
- Full JSON transcripts are summarized, not committed verbatim.
- The first ZC-04 run exposed an installation-path gap: `~/.claude/agents/zilan.md` existed locally, but `~/.claude/skills/zilan-agent/scripts/search_agama.py` did not. The repository prompt now prefers current-repo `scripts/` when available.

## 2026-06-12 OpenAI API Harness Dry Run

| Field | Value |
|---|---|
| Runtime | OpenAI API harness |
| Provider / model | OpenAI Responses API request model `gpt-5.5` |
| Tool version | `scripts/openai_api_harness.py` dry-run mode |
| Repository branch | `codex/claude-openai-validation` |
| Prompt set | Harness dry-run for ZC-02 / ZC-03 request construction from `tests/regression_cases.yaml` |
| Transcript status | Dry-run request construction only; no live OpenAI response transcript is recorded. |
| Repository checks | `python -m ruff check scripts tests` pass; `python -m pytest` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass |
| Overall result | `partial`: harness-ready, live provider execution not yet tested |

### Observations

- The harness loads `agents/openai.yaml`, regression case prompts, and bounded local context files.
- Dry-run mode does not require `OPENAI_API_KEY` and is covered by `tests/test_openai_api_harness.py`.
- Live mode is implemented behind `--live` and fails fast unless `OPENAI_API_KEY` is present.
- OpenAI API should remain `harness-ready`, not `tested`, until a dated live run is recorded.

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
