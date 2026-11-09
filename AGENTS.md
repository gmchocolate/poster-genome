# 给维护 Poster Genome 仓库的 Agent

本仓库有两层：根目录是项目介绍、安装与治理；**实际可分发的 Skill 在 `skills/poster-genome/`**。不要重新创建根目录 `SKILL.md`，避免 CLI 只安装入口文件、漏掉依赖。

修改前先确定目标读者、目的、编辑范围与明确授权。对中文文档使用 [deep 改写原则](docs/EDITORIAL_POLICY.md)：优先理顺阅读路径，不编造能力、不改变命令、条件和版本；原文已经清楚时可以不改。

权威来源：
- `skills/poster-genome/SKILL.md`：Agent 行为与边界。
- `skills/poster-genome/references/`：按需读取的具体设计方法。
- `skills/poster-genome/schemas/`：数据契约。
- `docs/INSTALLATION.md`：安装路径及命令。
- `docs/EVALUATION.md`：什么叫验证通过。

新增基因前必须比较现有内容、获得用户对写入仓库的授权，并诚实记录来源和版权。不得提交私人照片、未经授权的第三方海报和付费字体。

更新后检查文档链接、例子和测试：`python skills/poster-genome/scripts/validate_library.py` 与 `python -m unittest discover -s tests -v`。能力测试和视觉效果没有完成时，不写“已验证”。


## v0.3 私人参考图与实际创作

Poster Genome 现在是 Reference-First Skill。用户可将喜欢的参考海报存于执行环境本机 ~/.poster-genome/；这些图片**严禁**提交到公共仓库或内置 genomes/。不要将云端运行空间称为用户自己电脑的本地文件。

维护时必须检查：references/personal-taste-library.md、references/reference-first-workflow.md、scripts/taste_library.py。JSON 文件仍只负责抽象规则；实际创作应真实检索、读取并经宿主接口附加视觉参考图。文件路径、文本摘要不等于图像输入。

涉及用户真实照片时，用户源图与风格参考图角色严格分开；两张人物照片不能漏掉其中一张。相机参数、日期、气温等必须核实。

测试：安装 skills/poster-genome/requirements-dev.txt 并运行 python -m unittest discover -s tests -v。参考图在临时测试目录内生成；不要向 GitHub 提交用户上传的真实海报。
