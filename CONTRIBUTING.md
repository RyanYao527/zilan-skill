# 贡献指南

感谢对孜澜 skill 的关注。

## 如何贡献

### 方式一：提交 Issue
- 发现 bug 或有改善建议，欢迎提交 GitHub Issue
- 请使用清晰的问题描述

### 方式二：Fork & Pull Request
1. Fork 本仓库
2. 创建分支（`git checkout -b feature/你的功能名`）
3. 提交更改（`git commit -m '你的提交信息'`）
4. Push（`git push origin feature/你的功能名`）
5. 提交 Pull Request

### 提交规范
- Commit 信息使用中文或英文，简洁描述
- 涉及核心定义修改的，请同时更新 `沟通过程.md` 中的对应章节
- 大幅修改请先提 Issue 讨论

## 本地验证

修改 `SKILL.md`、`agents/`、`context/`、阿含语料或脚本后，请至少运行：

```bash
python scripts/validate_zilan_repo.py --check-generated
python -m pytest
python scripts/search_agama.py --terms "無我|非我|緣起" --limit 10
```

`validate_zilan_repo.py` 会检查必要文件、Codex 回归矩阵、Agent prompt 关键片段、阿含检索 smoke test，并可验证 CBETA XML 生成的 Markdown 是否稳定。

## 知识共建说明

本 skill 是活的学习系统，会随修学进展持续更新。核心知识沉淀在：
- `SKILL.md` — 主定义文件
- `context/摄类学工具箱.md` — 概念分析与逻辑推理工具链
- `context/因明推理引擎.md` — 因明逻辑引擎
- `沟通过程.md` — 进化轨迹记录

欢迎通过 PR 共建。

---

*寻遍十方谁是我，波心圆月本无澜*
