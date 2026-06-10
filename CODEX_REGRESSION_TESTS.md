# Zilan Codex Regression Tests

> Purpose: keep the Codex version of zilan-skill stable after prompt, context, or routing changes.
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

Use these from PowerShell when validating the local knowledge base.

```powershell
rg -n --glob '!**/_source/**' --max-count 10 "無我|非我|無我所|五陰|五受陰|緣起" "C:\Users\rori9\.codex\skills\zilan-skill\context\agama"
rg -n --max-count 10 "因三相|性相|心所|應成|十六觀智" "C:\Users\rori9\.codex\skills\zilan-skill\context"
```

## Known Boundaries

- These tests are smoke/regression tests, not exhaustive scholarly validation.
- For publication-level work, verify local Markdown passages against CBETA XML and relevant parallel texts.
- Codex sub-agent spawning is a runtime capability, not a persistent user-level `~/.codex/agents` directory contract.
