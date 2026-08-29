# Claude 工具储备清单

> 见过/用过的 Claude 工具与 skill 记在这里，免得以后要用时想不起名字、找不到入口。需要时回这里翻。

## Diagram Design（图表 skill）

- **是什么**：生成"编辑级"自包含 HTML+SVG 图的 Claude Code skill，27 种图类型（架构/流程/时序/象限/金字塔/时间线…），带严格设计系统 + 品牌色 onboarding，可导出 SVG/PNG、能把 draw.io/Mermaid 重绘成它的风格。
- **何时用**：要一张"撑门面"的精致图时。Mermaid 够用就别用——它单图 token 约是 Mermaid 的 5~20 倍（skill 加载 + 长输出 + 可能迭代）。
- **装法**：`/plugin marketplace add cathrynlavery/diagram-design` + `/plugin install diagram-design`
- **仓库**：https://github.com/cathrynlavery/diagram-design
- **注意**：渐进式加载（不画图不常驻），不必长期装着，真需要再装。

## Claude in Chrome（官方 Chrome 扩展）

- **是什么**：Anthropic 官方 Chrome 扩展，Claude 能在浏览器里自主操作当前页面（读/点/填表单/翻页/导航），复用你的登录态，操作没有 API 的网页系统（内部后台、供应商门户、旧系统）。
- **何时用**：要处理网页上的重复操作、填表、整理邮箱/文档，而这些网站没有 API 时。
- **状态**：2026-08-26 对所有付费计划 GA；有 prompt injection 防护，可回退到手动批准。
- **对比**：Claude Cowork 桌面端另有**内置浏览器**（Chromium，不看你自己浏览器的标签/书签/密码，可选导入登录）——两者互补：扩展管"你已打开的页面"，内置浏览器管"交给 Claude 独立去跑"。
