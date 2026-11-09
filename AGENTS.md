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
