# 示例：从了解格式到真正运行

这个目录里放的是**合成示例**，不是已经观察过的真实商业海报。

- `brief-example.json`：给匹配脚本使用的示例创作要求。
- `analysis-example.json`：演示怎样区分观察、推断、未知。里面的海报是假设场景，**不代表实际看过图片**。

## 从技能目录运行

下面的命令以当前目录是 `skills/poster-genome/`（或安装后的技能根目录）为前提：

```bash
python scripts/match_genomes.py --input examples/brief-example.json --top 2
```

如果从 GitHub 仓库根目录运行：

```bash
python skills/poster-genome/scripts/match_genomes.py --input skills/poster-genome/examples/brief-example.json --top 2
```

## 给已有图片叠加准确中文

这是一个**简单的文字合成工具**，不是 AI 生图器。你需要自己的照片，以及可以合法使用、包含所需中文字形的字体文件。先在仓库根目录安装可选依赖：

```bash
python -m pip install -r requirements-render.txt
python skills/poster-genome/scripts/overlay_text.py \
  --image ./photo.jpg \
  --font /path/to/your/CJK-font.ttf \
  --headline "秋日物语" \
  --subtitle "留住此刻" \
  --output ./output/poster.png
```

这个工具会把照片裁切成指定画布，并在下方加暗色渐变和文字。它不能自动判断照片是不是适合这种布局，所以还需要人工检查裁切、字形、可读性和主体是否被遮挡。

真实海报学习请向能看图的 Agent 上传**有权分析的参考图**并调用 `poster-genome`。未获授权前，不应把这张图片提交到公共代码库。
