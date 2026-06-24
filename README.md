# 严复 Skill

严复 Skill 是草诀歌 AI Labs 的产品故事翻译官：把开发者视角的 Landing Page 和核心产品截图，翻译成用户 5 秒能懂的落地页故事。

## 仓库结构

- `skills/yanfu/`：Codex Skill 源文件、参考说明与交付校验脚本。
- `landing/index.html`：严复 Skill 官网首页，可作为静态站点部署。
- `landing/assets/bundle/`：从官网源文件拆出的图片、字体与运行时资源。
- `tests/`：Skill 与 Landing Page 的基础契约测试。

## 本地预览

```bash
cd landing
python3 -m http.server 4173
```

然后打开 `http://127.0.0.1:4173/`。

## Cloudflare Pages 部署

推荐用 Cloudflare Pages 部署静态站点：

- Framework preset: `None`
- Build command: 留空
- Build output directory: `landing`
- Root directory: 仓库根目录

后续可以把自定义域名配置到 Cloudflare Pages，例如与 `simaqian.caojuege.com`、`b.caojuege.com` 放在同一组官方入口中。

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 /Users/aroma/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/yanfu
```
