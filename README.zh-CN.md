# Poster Genome｜海报基因 🧬

**喜欢一张海报，不只要学它长什么样，更要学会它为什么这样设计。**

Poster Genome 是一套开源的 **Agent Skill（供 AI 助手执行的技能说明）**。你给它一张喜欢的海报，它会分析素材、布局、色彩、字体、文案和阅读顺序，并把其中能复用的方法整理成“设计基因”。之后，你上传自己的照片，它会挑选适合的基因、问少量必要问题，再指导具有生图能力的 AI 创作原创海报。

它不是一个独立的网站，也不自带生图模型。实际看图、生图和修图能力取决于使用它的 AI 客户端。

[English](README.md) · [Skill 本体](skills/poster-genome/SKILL.md) · [贡献指南](CONTRIBUTING.md)

## 一分钟安装

在项目目录中运行：

```bash
npx skills add gmchocolate/poster-genome
```

安装器会发现名为 **`poster-genome`** 的技能，并让你选择要安装到哪个 AI Agent。想在所有项目里使用，可加 `-g`：

```bash
npx skills add gmchocolate/poster-genome -g
```

只想先检查能找到哪些技能，不安装：

```bash
npx skills add gmchocolate/poster-genome --list
```

安装器需要符合其版本要求的 Node.js（当前官方说明为 **22.20 或以上**）。不同客户端是否会自动载入技能，要以其实际行为为准。完整步骤、检查方法和常见问题见 [安装指南](docs/INSTALLATION.md)。

## 我可以用它做什么？

### 1. 学习一张优秀海报

上传一张你喜欢的海报，然后说：

> 用 poster-genome 学习这张海报。先告诉我主要元素有哪些、观众会先看哪里、颜色和字体为什么这样搭配。请把真正可复用的设计方法整理成候选基因，不要直接照搬，也先不要保存到仓库。

它会按这个顺序回答：

1. **看到什么：** 人物、物品、背景、装饰、文字的数量与位置；看不清的地方明确标注。
2. **怎样组织：** 主体和文字的主次、观看顺序、构图、留白、配色和画面质感。
3. **为什么可能有效：** 用具体画面证据解释设计判断，不只说“高级”或“有冲击力”。
4. **能学走什么：** 总结 3–8 条可迁移规则，说明什么素材适合、什么情况会失效。
5. **要不要保存：** 显示候选名称和差异，得到你批准才加入基因库。

例如，看到“亮色商品 + 安静深色背景”，它会提炼“用明暗差别突出单一主角”，而不是把商品、标题与背景位置全部原样复制。

### 2. 用自己的照片创作海报

上传照片后说：

> 用 poster-genome 给这张照片做生日海报。祝福语是「祝奶奶生日快乐」，发朋友圈用。其他你来决定，只问我真正缺少的信息。

它会先检查照片里的主体和可裁切空间，再选择合适的设计基因。如果缺少的信息会影响作品，通常只问“做给谁、必须写什么、用在哪里”这类问题。

选好风格后，先规划主体位置、文字区、颜色和层次，然后使用客户端真实可用的生图或修图工具制作。生成后检查文字、人物、裁切和画面质量。

**如果客户端没有生图工具：** 它会给你清晰的制作方案和提示词，不会假装已经生成了图片。

### 3. 修改一张已经做好的海报

> 保留人物、标题和颜色方向，只修复排版拥挤、文字不清楚的问题。

Skill 会先区分**硬错误**（错字、主体变形、内容漏写）和**审美偏好**（更简约、更明亮），再针对问题修改，不为了“显得专业”随意重做。

## 为什么要有“设计基因库”？

每次只模仿一张参考图，换了主体、用途或文案就容易失效。设计基因保存的是**可调整的规则**，不是固定模板。

例如，`cinematic-editorial` 记录人物电影感海报的主体对比、光线、留白和短文案安排；`bold-type-minimal` 则强调强烈的标题、简洁形状和严格的对齐。两者只是演示数据，均为原创示例，尚不代表对真实用户偏好的验证。

每份基因都记录适用的主体、用途、比例，以及什么情况下可能不合适。你后续上传参考海报，可以不断增添或改进基因，但要**先看差异、再决定是否保存**。

## 项目结构：从哪里开始看？

```text
poster-genome/
├── README.md / README.zh-CN.md    # 介绍与使用方法
├── CONTRIBUTING.md                # 贡献和评审要求
├── docs/                          # 安装、改写方法与评估边界
├── skills/
│   └── poster-genome/             # 实际被 npx skills 安装的完整技能
│       ├── SKILL.md               # Agent 的执行入口
│       ├── references/            # 六份按需阅读的设计方法
│       ├── genomes/               # 可积累、可选择的设计基因
│       ├── schemas/               # JSON 数据格式
│       ├── scripts/               # 匹配、校验、新建与文字合成
│       └── examples/              # 不含第三方版权图片的示例
├── tests/                         # 本地静态测试
└── .github/workflows/             # GitHub 自动检查
```

想知道 AI **必须如何做**，读 [SKILL.md](skills/poster-genome/SKILL.md)；想知道某条分析为什么合理，读对应的 `references/`；想参与开源，读 [贡献指南](CONTRIBUTING.md)。

## 需要维护基因库时

本地脚本需要 Python 3.10+。在仓库根目录执行：

```bash
python -m pip install -r requirements-dev.txt
python skills/poster-genome/scripts/validate_library.py
python -m unittest discover -s tests -v
```

查询适合人像、编辑叙事、电影感、4:5 竖版的基因：

```bash
python skills/poster-genome/scripts/match_genomes.py --subject person --intent editorial --mood cinematic --ratio 4:5
```

已有构思也可以用 [示例简报](skills/poster-genome/examples/brief-example.json) 直接检索：

```bash
python skills/poster-genome/scripts/match_genomes.py --input skills/poster-genome/examples/brief-example.json --top 3
```

如果已经有照片和合法字体，只需要一个准确写中文的简单合成步骤，可以单独安装 Pillow 使用 `overlay_text.py`。这只是固定的文字叠加，不是 AI 原创海报生成器。命令见 [示例说明](skills/poster-genome/examples/README.md)。

## 目前能验证什么，不能验证什么？

- **仓库检查：** Python 脚本、基因格式、文档路径和安装打包可以通过自动化流程检查。
- **还不能证明：** 用户上传的每张图片都能正确理解、每种设计基因都好看、所有客户端都具备生图工具、真实用户的理解率或审美偏好得到提升。
- **版权与隐私：** 分析参考图不等于可以公开分发参考图。私人照片、商标素材和字体不得在未获授权时提交公开仓库。

关于怎样做可靠的测试，见 [评估方法](docs/EVALUATION.md)。关于为什么这样重写说明文档，见 [中文表达原则](docs/EDITORIAL_POLICY.md)。

## 参与贡献

欢迎提交可复用的原创设计基因、明确的失败案例、对中文海报排版的改进，或某种 AI 客户端实际安装与运行记录。请按 [贡献指南](CONTRIBUTING.md) 提供问题、理由、需要保留的要求、反例和验证方法。

项目代码与原创文档采用 [MIT License](LICENSE)。第三方素材的权利不因本仓库的许可证而自动改变。
