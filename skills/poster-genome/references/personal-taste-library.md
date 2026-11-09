# 个人 Taste Library：把喜欢的海报保留在自己本地

## 为什么要有本地参考图库？

设计基因 JSON 告诉 Agent **应该怎么设计**，但只靠规则通常会丢失真实作品的精微节奏、字体比例、图片与标题的关系和设计趣味。

因此每位安装者应该有一套**独立的私人视觉参考库**，而不是只能复用仓库公开的文字规则。每条参考记录包含：

- **真实参考图**（保存本机副本）；
- 用户给的名字、风格标签、关联的设计基因；
- **liked_for**：真正喜欢哪些设计细节，如“不规则大标题与手写黄字的关系”；
- **avoid_copying**：不要模仿哪些内容，如“原作品的 LOGO、确切字句和相同位置”；
- 用户主观打分 rating（1–5），用于本地优先排序，而非客观审美评分。

同一种风格可以有多张参考；不同用户有不同的喜好，**不会汇总进仓库或自动向 GitHub 同步**。

## 本地在哪里？

默认是执行 Agent 的那台机器上的：

~~~text
~/.poster-genome/
├── index.json               # 用户的私人审美记录
└── images/
    └── <content-sha256>.jpg # 去除图片元信息后的参考图
~~~

可用环境变量 POSTER_GENOME_HOME=/absolute/private/path 或 CLI 的 --home 改变位置。默认不放进安装后的 Skill、当前项目或 Git 仓库，不因 npx skills add 重装而丢失。

**注意远程 Agent：** “本地”是指 CLI 实际运行的环境。如果 Grok 或其他 Agent 在云端、没有访问用户电脑文件的权限，它无法凭空读写用户电脑的 ~/.poster-genome。必须将图片安全地提供给可访问该目录的本地 Agent，或自行配置持久化的私有存储；本项目没有云端同步服务。

## 第一次使用

找到已安装的 poster-genome 技能目录：

~~~bash
python -m pip install -r requirements-library.txt
python scripts/taste_library.py list
~~~

首次 list 返回空列表，不会自动建立目录、收集或上传任何图片。

**用户明确同意添加后**，例如：

~~~bash
python scripts/taste_library.py add \
  --image "/path/to/liked-poster.jpg" \
  --title "日常摄影手账" \
  --genome playful-sky-editorial \
  --tag everyday --tag editorial \
  --like "粗体主标题与细手写字自然穿插" \
  --like "留白和小型涂鸦的节奏" \
  --avoid "原海报LOGO和准确字句" \
  --rating 5
~~~

本操作会把参考图去除 EXIF 等内嵌元信息（包括可能的地理位置信息），保存本地副本，并记录条目 ID。同一个图重复添加会合并标签和偏好，不复制多份。

它不会自动分析图片；**学习分析必须由具备视觉能力的 Agent 实际查看用户图片后进行**，再由 Agent 在获授权后写入 --like / --avoid。CLI 仅提供可靠的本地保存与检索。

## 检索用户真正喜欢的参考图片

~~~bash
python scripts/taste_library.py select \
  --genome playful-sky-editorial --tag everyday --top 2
~~~

返回图像在本机的真实绝对路径，以及用户记录的喜欢/避免内容。初版按基因标签、用户标签和喜好分数排序，是**可解释的元数据检索**，不是 CLIP、图像向量或自动视觉相似度检索。Agent 应实际查看候选图，再判断最终选哪张；找不到合适的参考，不要硬选。

不填 --genome 可以浏览整个个人参考库：

~~~bash
python scripts/taste_library.py list
python scripts/taste_library.py select --tag portrait
~~~

## 根据成品反馈积累 Taste

用户完成一次创作后，可表达：

> 我喜欢第一版黄色手写字叠加在粗体标题上的感觉，但不喜欢虚构相机参数。保存这条偏好。

Agent 在确认用户要更新哪条本地参考时可执行：

~~~bash
python scripts/taste_library.py feedback \
  --id ref-xxxxxxxxxxxxxxxxxxxx \
  --rating 5 \
  --like "黄色手写字和粗体标题穿插" \
  --avoid "没有依据的相机参数"
~~~

删除本地参考记录（也删除其私人图片副本）：

~~~bash
python scripts/taste_library.py remove --id ref-xxxxxxxxxxxxxxxxxxxx
~~~

所有保存和删除必须由用户明确要求或同意。**上传参考图用于本次分析，不自动等于授权持久存储**。

## 权利与隐私

- 用户保留本地图片，不代表获得第三方商业海报的公开转载或重新分发权限。
- 不要将用户的图库放到 skills/poster-genome/、Git 仓库、自动化 CI、Issue 或 PR 中。
- 对用户的本地库进行“引用”不等于可以自动将图上传到外部生成服务；调用云端生图工具前应尊重用户授权和服务本身的隐私规则。
- 素材里的隐藏 EXIF 会被重编码移除；但**画面可见的姓名、脸、地址、车牌、二维码**仍然留在照片中，需要用户自己判断能否交给云端工具。
- CLI 只有本地文件读写，不会主动访问网络。未提供图像输入权限的 Agent 不能声称已经读取了参考图。
