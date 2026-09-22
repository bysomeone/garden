# garden · 文档库

个人知识库。Markdown 源在 `notes/`，由 Docsify 渲染（本页即首页）。

## 目录

- [ops](ops/) — 线上问题定位与故障复盘
- [tech](tech/) — 技术笔记
- [finance](finance/) — 宏观经济与货币体系
- [tools](tools/) — 工具与 AI 方法论

## 说明

- 新增文档：按 **大类/领域** 放入 `notes/` 下的对应目录，Markdown 即可，Docsify 自动渲染；
- 每个大类目录下的 `README.md` 是本类的文档索引；
- 私密内容：frontmatter 标 `visibility: private`，pre-push 钩子会拦截推送；
- 本地：可用 Obsidian 打开 `notes/` 作为 vault。
