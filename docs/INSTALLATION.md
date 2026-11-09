# 安装与验证：让 AI Agent 找到完整的 Poster Genome

## 先确认环境

- 需要一个支持 [Agent Skills](https://agentskills.io/specification) 的 AI Agent，例如使用 Skills CLI 的兼容客户端。
- 安装命令使用 [Vercel Skills CLI](https://github.com/vercel-labs/skills)。截至本次核对，其文档要求 **Node.js 22.20+**。用 `node --version` 检查。
- 需要能访问 GitHub 和 npm 的网络环境。
- **使用图片创作功能**还取决于所选 Agent 有没有实际看图、生图或修图工具；“成功安装 Skill”不等于“具备生图模型”。

## 安装（在你自己的项目目录）

```bash
npx skills add gmchocolate/poster-genome
```

安装器显示找到的技能 `poster-genome`，然后选择需要的 Agent 和安装方式。默认是**当前项目**安装；希望所有项目使用：

```bash
npx skills add gmchocolate/poster-genome -g
```

只检查发现结果，不写入：

```bash
npx skills add gmchocolate/poster-genome --list
```

已有安装时，按客户端的加载机制重启或刷新，再在对话里明确说“使用 poster-genome 分析这张海报”。

## 为什么代码放在 skills/poster-genome/？

这是技能的**完整可安装目录**：

```text
skills/poster-genome/
├── SKILL.md
├── references/
├── genomes/
├── schemas/
├── scripts/
└── examples/
```

根目录没有另一个 `SKILL.md`。这样安装器发现的是**一套完整技能**，不是只拿到一个入口文件、却找不到引用的规则或脚本。格式遵循 [Agent Skills 规范](https://agentskills.io/specification)；命令行行为以 [Skills CLI 文档](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) 为准。

## 安装后怎样检查？

1. 运行 `npx skills list`，或在已选 Agent 对应的技能目录中检查是否存在 `poster-genome`。
2. 检查安装目录中有没有 `SKILL.md` 和 `references/analysis-framework.md`、`genomes/cinematic-editorial.json`、`scripts/match_genomes.py`。
3. 在能运行 Python 的 Agent 工作区中调用基因匹配脚本，或让 Agent 读取示例 JSON 并说明它选择哪一种基因。
4. 再试一张已获授权的参考图：让 Agent 区分“观察、推断、未知”。若没有看图能力，这一步不能算通过。

安装路径随客户端、全局/项目安装和工具版本变化，不应保证所有客户端完全相同。

## 常见问题

**提示找不到技能：** 检查网络、Node.js 版本、命令是否在可写项目目录执行，随后用 `--list` 看发现结果。

**只装了 SKILL.md：** 检查是否安装了旧版本或直接拿根目录文件。请重新从该 GitHub 仓库安装最新版，确认 `references/` 等文件存在。

**安装成功但不会生成图片：** 这不属于安装失败。Skill 提供的是设计分析与执行流程，需要宿主 Agent 自己具有图像工具；否则只能输出可实施的创作说明。

**需要固定版本：** Skills CLI 支持将 Git 源固定到 tag 或 commit，但应先确认目标版本已发布及其内容完整，不要随意编造 tag。

## 验证范围

GitHub Actions 使用 Skills CLI 检查仓库发现与本地安装目录中关键文件是否齐全；这属于**安装与文件结构测试**，不代表所有客户端的真实运行体验已通过，更不代表海报审美质量得到验证。
