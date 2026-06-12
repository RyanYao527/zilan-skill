# 孜澜 · Zilan

> **Independent Buddhist practitioner** · **独立修行者**
>
> AI 大语言模型佛学 Agent / Skill 双轨框架 · Buddhist Agent / Skill framework for AI LLMs
>
> 基于优婆塞姚磊佛学体系 · Based on Upāsaka Yao Lei's Buddhist study system

---

## 🌐 Choose your language · 选择语言

| | 语言 | Language | 入口 Entry |
|---|---|---|---|
| 🇨🇳 | **中文** | Chinese | **[`README.zh.md`](README.zh.md)** |
| 🇺🇸 | **English** | English | **[`README.en.md`](README.en.md)** |

> 💡 *Tip: GitHub 会根据你的浏览器语言自动显示对应版本。如果你想切换,点击上表中的入口即可。*
> *GitHub auto-detects your browser language. Click an entry above to switch.*

---

## ⚡ 30 秒快速上手 · Quick start in 30 seconds

```bash
# 1. Clone
git clone https://github.com/RyanYao527/zilan-agent.git

# 2. Copy into your Claude Code skills directory
cp -r zilan-agent ~/.claude/skills/

# 3. Optional: install the Claude Code Agent definition
mkdir -p ~/.claude/agents
cp zilan-agent/agents/zilan-claude-code.md ~/.claude/agents/zilan.md

# 4. In any Claude session, mention 孜澜 / Zilan / 因明 / 摄类学 to activate
```

---

## 📦 What's inside · 仓库内容

| 文件 File | 用途 Purpose |
|---|---|
| `SKILL.md` | 完整 skill 定义(中文) · Full skill definition (Chinese) |
| `SKILL-en.md` | 完整 skill 定义(英文) · Full skill definition (English) |
| `README.zh.md` | 完整文档 · Full documentation (Chinese) |
| `README.en.md` | 完整文档 · Full documentation (English) |
| `CONTRIBUTING.md` / `CONTRIBUTING-en.md` | 贡献指南 · How to contribute |
| `LICENSE` | MIT 开源许可 · MIT license |
| `agents/zilan-claude-code.md` | Claude Code Agent 定义 · Claude Code Agent definition |
| `agents/zilan-codex.md` | Codex sub-agent prompt · Codex sub-agent prompt |
| `agents/openai.yaml` | 跨平台 Agent 配置 · Cross-platform Agent metadata |
| `CODEX_REGRESSION_TESTS.md` | Codex 回归测试矩阵 · Codex regression matrix |
| `docs/platform-validation.md` | 平台验证状态 · Platform validation status |
| `scripts/validate_zilan_repo.py` | 仓库结构与语料 smoke 校验 · Repository invariant checks |
| `scripts/search_agama.py` | 阿含 Markdown 检索工具 · Agama Markdown search helper |
| `.github/workflows/ci.yml` | 自动化校验 · Automated CI checks |
| `context/摄类学工具箱.md` | 摄类学推理工具链 · Collected Topics reasoning toolkit |
| `context/因明推理引擎.md` | 因明逻辑引擎 · Buddhist logic engine |
| `沟通过程.md` | 沟通进化轨迹 · Communication evolution log |
| `上传步骤.md` | 上传指南 · Upload guide |

---

## 🧭 Skill / Agent dual track · 双轨模式

- **Skill mode**: lightweight dialogue, daily practice reflection, and simple concept explanation.
- **Agent mode**: explicit deep research for Agama retrieval, Buddhist logic chains, cross-domain analysis, and long reports.
- **Codex**: use explicit prompts such as `spawn a zilan agent` / `让孜澜独立深入研究一下`; regression cases live in `CODEX_REGRESSION_TESTS.md`.

---

## ✅ Compatibility status · 兼容性状态

- **Platform status**: `agents/openai.yaml` is the machine-readable metadata source; `docs/platform-validation.md` records status definitions, validation evidence, and update rules.
- **Runtime boundary**: Codex, Claude Code, OpenAI API, DeepSeek, GLM, and Qwen routes must not be described as tested unless the platform validation document says so.
- **Scholarly collation**: local Agama Markdown is a searchable working corpus; publication-level work should verify against CBETA XML and parallel texts.

---

## 🧪 Engineering checks · 工程校验

```bash
python scripts/validate_zilan_repo.py --check-generated
python -m pytest
python scripts/search_agama.py --terms "無我|非我|緣起" --limit 10
python scripts/search_agama.py --terms "非我" --passages --group-by juan --limit 10
python scripts/search_agama.py --terms "緣起" --json --limit 5
```

GitHub Actions runs the same invariant checks, tests, and Agama search smoke test on push and pull request.

---

## 🔑 唤醒关键字 · Activation keywords

**主关键字 Primary**: `孜澜` · `Zilan`
**身份 Identity**: `姚磊` · `优婆塞` · `Upāsaka` · `Yao Lei`
**经典 Scriptural**: `阿含经` · `Agama`
**逻辑 Logical**: `因明` · `摄类学` · `应成论式` · `因三相` · `四句逻辑`
**场景 Contextual**: `数字人佛学` · `数字人修学` · `Buddhist digital persona`

---

*寻遍十方谁是我,波心圆月本无澜* · *遍了十方谁是吾,波心圆月本无澜*
