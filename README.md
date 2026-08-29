# garden

个人知识库总仓库（公开）。统一存放 Markdown 笔记源与渲染后的 HTML 文档页。

## 内容

- `notes/` — Markdown 笔记源，按 **大类/领域** 组织（如 `tech/rgb/`）。标准 Markdown 结构，便于后续接入知识库 / 知识图谱系统。
- `pages/` — 渲染好的 HTML 文档页（artifact 链接），按 **大类/领域** 组织。

## 目录结构

```
garden/
├── index.html           # 文档库首页（tools/build_index.py 自动生成）
├── notes/               # Markdown 笔记源
│   └── tech/rgb/…
├── pages/               # 渲染 HTML 文档页
│   └── tech/rgb/…
├── tools/               # build_index.py / scan_secrets.py
└── .githooks/pre-push   # push 前扫描钩子
```

## 如何添加内容

1. 将文档按 **大类/领域** 放入 `pages/`（HTML）或 `notes/`（Markdown）；
2. 运行 `python3 tools/build_index.py` 更新首页；
3. `git add` + commit + push（pre-push 钩子自动扫描）。

## 安全与隐私规则

- 内容含 `visibility: private` 标记 → **禁止推送**（pre-push 拦截）；
- 敏感信息（密钥、token、助记词等）→ **禁止推送**；
- 大文件 / 非白名单二进制 → **禁止推送**；
- 机密内容不应进入本公开仓库。
