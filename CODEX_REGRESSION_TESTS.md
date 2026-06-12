# Zilan Codex Regression Tests

> Purpose: keep the Codex version of zilan-agent stable after prompt, context, or routing changes.
> Date: 2026-06-10

## How To Run

Run these manually in a Codex chat after any meaningful change to `SKILL.md`, `agents/zilan-codex.md`, `agents/openai.yaml`, or `context/`.

For sub-agent cases, use an explicit trigger such as "spawn a zilan agent" so Codex may delegate according to the current sub-agent policy.

## Pass Criteria

- The answer uses Zilan's precise, de-mystified Buddhist analysis style.
- The answer loads or cites the relevant local context instead of guessing.
- Agama citations include sutra name, CBETA id,卷 or 经/品 information when available, and local file line references for audit.
- Agama text searches prefer Markdown files and avoid `_source/` XML unless explicitly checking source text.
- The answer states boundaries for practice guidance, textual inference, or non-exhaustive search.
- Lightweight dialogue stays in Skill mode; deep research uses sub-agent only after explicit trigger or user confirmation.

## Test Matrix

| ID | Mode | Prompt | Expected Behavior |
|----|------|--------|-------------------|
| ZC-01 | Skill lightweight dialogue | `孜澜，我今天职场又被否定了，心里很难受。` | Direct response without sub-agent; uses daily-practice support,心类学/观禅 framing, and no scripture overreach. |
| ZC-02 | Skill concept lookup | `孜澜，什么是因三相？` | Reads or follows `context/因明推理引擎.md`; explains遍是宗法性、同品定有性、异品遍无性; mentions relation to摄类学. |
| ZC-03 | Skill cross-domain explanation | `孜澜，用摄类学和心类学解释“我被否定了”的认知过程。` | Uses `摄类学工具箱.md` + `心类学认知分析.md`; distinguishes fact, concept label,受/想/瞋心所, and practice boundary. |
| ZC-04 | Explicit sub-agent Agama search | `请 spawn 一个 zilan agent，查四阿含中关于无我的经文，并做初步归类分析。` | Spawns sub-agent; searches Markdown Agama files with traditional terms; excludes `_source/`; returns categories, representative citations, and boundary statement. |
| ZC-05 | Explicit sub-agent cross-domain research | `请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。` | Spawns sub-agent; loads Agama index plus摄类学、因明、中观、观禅 context; outputs conclusion, reasoning chain, practice boundary. |
| ZC-06 | Long report output | `请 spawn 一个 zilan agent，生成一份“阿含无我观法门”研究报告并写入文件。` | Spawns sub-agent; writes a report only because file output is requested; includes search strategy, classification table, representative passages, analysis, and boundary statement. |

## Spot-Check Commands

Use these from PowerShell when validating the local knowledge base. Run them from the repository root, also called `<zilan-agent-root>` in the prompt files.

```powershell
python scripts/validate_zilan_repo.py --check-generated
python scripts/search_agama.py --terms "無我|非我|無我所|五陰|五受陰|緣起" --limit 10
python scripts/search_agama.py --terms "非我" --passages --group-by juan --limit 10
python scripts/search_agama.py --terms "緣起" --json --limit 5
rg -n --glob '!**/_source/**' --max-count 10 "無我|非我|無我所|五陰|五受陰|緣起" "context\agama"
rg -n --glob '!**/_source/**' --max-count 10 "因三相|性相|心所|應成|十六觀智" "context"
```

`scripts/search_agama.py` excludes `_source/` XML by default, filters known keyword collisions such as `非我宜` and `非我所說`, supports `--group-by file|juan`, and can aggregate paragraph-like passages with `--passages`.

## Known Boundaries

- These tests are smoke/regression tests, not exhaustive scholarly validation.
- Codex sub-agent spawning is a runtime capability, not a persistent user-level `~/.codex/agents` directory contract.

## Scholarly Collation Roadmap

For publication-level Agama work, treat the local Markdown files as a searchable working corpus rather than the final critical source. A stricter route should:

- Verify quoted Markdown passages against the corresponding CBETA XML-P5 source.
- De-duplicate hits by sutra, fascicle, and passage rather than by raw keyword match.
- Compare relevant parallel translations and, when useful, Pali parallels.
- Standardize citations at sutra / fascicle / passage or line level before external publication.
