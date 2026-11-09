# Poster Genome 🧬｜让 AI 学会你喜欢的海报

**不是让 AI 凭一句“高级感”自由发挥，而是先存下你真正喜欢的参考海报，再带着这些真实图片去创作。**

Poster Genome 是开源 [Agent Skill](https://agentskills.io/specification)。你可以上传喜欢的海报，让 AI 看图分析它为什么好看，经你同意后将**原始参考图和你的审美偏好保存在运行环境本地**。之后你上传自己的照片，Agent 会选出适合的参考原图和设计基因，把它们一起提供给具有图像输入能力的创作工具。

**本项目不自带视觉模型、生图模型或云端同步服务。** 视觉学习与生成质量依赖宿主 Agent 的实际工具。

[English](README.md) · [Skill 主指令](skills/poster-genome/SKILL.md) · [个人图库使用指南](skills/poster-genome/references/personal-taste-library.md) · [贡献指南](CONTRIBUTING.md)

## 一、安装技能

~~~bash
npx skills add gmchocolate/poster-genome
~~~

全局使用：

~~~bash
npx skills add gmchocolate/poster-genome -g
~~~

查看能发现什么：

~~~bash
npx skills add gmchocolate/poster-genome --list
~~~

安装后，在支持该 Skill 的 Agent 对话中说：“用 poster-genome 学习这张海报”。详细环境要求见 [安装指南](docs/INSTALLATION.md)。

## 二、第一次使用：添加你喜欢的真实参考海报

把一张喜欢的海报交给有看图能力的 Agent，并说：

> 深入分析这张海报的构图、字体、图片、留白和细节。尤其告诉我哪些设计方法值得复用。**学习完把这张图片和我的喜好一起保存到我的本地 Taste Library。** 不要把它上传 GitHub。

Agent 在能访问图片和本地文件、获得你明确授权的前提下，可以调用私人图库 CLI。先在**安装后的技能目录**安装图片处理依赖：

~~~bash
python -m pip install -r requirements-library.txt
~~~

然后添加图片：

~~~bash
python scripts/taste_library.py add \
  --image "/path/to/reference.jpg" \
  --title "摄影手账风" \
  --genome playful-sky-editorial \
  --tag editorial \
  --like "粗体标题与小手写字错落穿插" \
  --like "主图之外大面积米色留白" \
  --avoid "原设计师独特LOGO及完整版面复制" \
  --rating 5
~~~

每个安装者都拥有**独立的本地图库**：

~~~text
~/.poster-genome/
├── index.json              # 每张图的名字、标签、审美偏好与评分
└── images/                 # 保存下来的真实参考图片（移除 EXIF 元信息）
~~~

这不是远程服务；不会自动把图片发到 GitHub。图库不会随着重新安装 Skill 而被覆盖。

**注意：** “本地”指 Agent 的 CLI 实际运行位置。如果你在没有电脑文件访问权限的云端 Grok Bot 中使用，Bot 无法仅靠这条指令把图直接保存到你的电脑。需要能够访问你本机的 Agent，或你明确授权的私有持久化环境。

## 三、下次创作时，真的使用参考图片

比如你上传两张宝宝照片，说：

> 用我风格库里收藏的摄影手账海报，做一张双宝出行日记。**两张照片都必须用上，宝宝面容保持真实。** 不要编造拍摄时间和相机参数。

新版执行路径是：

<escape>用户源照片 → 匹配设计基因 → 找到个人图库中的 1–3 张真实参考海报 → 实际将两类图像送入支持多图的创作工具 → 核对成品 → 收集用户反馈</escape>

Agent 可调用本地脚本生成**输入清单**：

~~~bash
python scripts/taste_library.py prepare \
  --source "/path/to/baby-blue.jpg" \
  --source "/path/to/baby-pink.jpg" \
  --genome playful-sky-editorial \
  --tag portrait \
  --headline "双宝出行日记" \
  --top 2
~~~

清单严格区分：

- **content_images**：用户本次的真实照片。负责人物、数量、服装、商品、原始内容的保真。
- **style_reference_images**：你收藏的参考海报。负责字体、色彩、版式节奏和装饰语言，不能取代真实主体。
- **genome_id**：文字化的设计方法及适用边界。
- **constraints**：重要事实、文字和素材不能乱改。
- **attachment_required**：要求 Agent **真正读取/附加**参考图片，而不只是把文件路径写进 Prompt。

CLI 只准备清单，不是生图引擎。**能否实际使用多张图，仍取决于宿主是否支持图像输入和文件访问**。如果它只能处理文字，就不能声称已经根据参考原图生成。

完整执行标准见 [Reference-First 创作流程](skills/poster-genome/references/reference-first-workflow.md)。

## 四、越用越懂你的 Taste

保存的参考图可以按风格或标签找：

~~~bash
python scripts/taste_library.py list
python scripts/taste_library.py select --genome playful-sky-editorial --top 2
~~~

如果做出一张图，你觉得“大字和黄色手写字很有感觉，但是虚构相机参数很差”，在用户同意后，Agent 可以将这条反馈写入相关参考记录：

~~~bash
python scripts/taste_library.py feedback \
  --id ref-xxxxxxxxxxxxxxxxxxxx \
  --rating 5 \
  --like "大字与黄色手写字的错落节奏" \
  --avoid "未经核实的摄影参数"
~~~

这是一套**个人审美记忆**，不是“点赞一次就能微调模型权重”。初版检索使用标签、风格关联和用户评分进行排序；要让图片真正被参考，仍必须在创作时读取、附加图片。

## 五、公开基因库与个人图库有什么区别？

| 内容 | 保存在哪里 | 能做什么 |
| --- | --- | --- |
| **公开设计基因** | 安装技能内的 genomes/，代码仓库中也有 | 保存通用设计原理、限制和适配方式 |
| **个人真实参考海报** | 用户自己的 ~/.poster-genome/images/ | 让 AI 实际参考你喜欢的图片审美 |
| **个人审美反馈** | 用户自己的 ~/.poster-genome/index.json | 记录喜欢什么、不喜欢什么，决定优先选哪张参考 |
| **本次源照片** | 用户上传或自行指定的位置 | 保持照片里的真实内容和数量，不自动进参考库 |

例如，公开基因的正确名称是 **playful-sky-editorial**；它保存的是单图记录卡、手绘线、字体反差等设计原理。每个用户可以给它关联不同的私人海报，让同一个基因产生不同的个人审美方向。

仓库现有 cinematic-editorial、bold-type-minimal、playful-sky-editorial、quiet-urban-editorial 等基因，不需要人人把真实图片提交公共仓库。第三方海报的原图权利仍属于其权利人。

## 六、开发和测试

Python 3.10+，在仓库根目录运行：

~~~bash
python -m pip install -r skills/poster-genome/requirements-dev.txt
python skills/poster-genome/scripts/validate_library.py
python -m unittest discover -s tests -v
python skills/poster-genome/scripts/match_genomes.py --input skills/poster-genome/examples/brief-example.json --top 2
~~~

这些测试可以检查 JSON Schema、脚本、私人图库去除 EXIF、选择规则、安装文件完整性等；**不会调用图像大模型，也不会证明任意一张参考图一定带来更好的审美结果**。

## 七、隐私、版权和能力边界

- 未得到“保存到本地”的明确授权，不永久保存任何参考图。
- 用户图库与用户照片不进入公共 GitHub 仓库，也不默认上传云端生图服务。
- 保存到用户本机前会重编码参考图并剥除 EXIF；这不删除画面本身可见的私人信息。
- 参考图可以用来学习通用设计方法，不应复制第三方作品完整而独特的表达。
- 两张真实人物照片中的两个人都必须被保留；保真是硬门槛，审美好看不能抵消主体遗漏。
- 你实际使用的 Agent 如果不支持多图输入、本地文件读取或图像生成，必须明确指出而不能假装做到了。

想参与开源，见 [贡献指南](CONTRIBUTING.md)。更多质量与工具限制见 [评估方法](docs/EVALUATION.md)。原创代码与文档采用 [MIT License](LICENSE)。
