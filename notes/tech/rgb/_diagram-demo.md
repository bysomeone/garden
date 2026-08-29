# 图切换演示：HTML vs Mermaid

同一张「RGB 侧车架构」图的两种展示方式，用 `<details>` 折叠切换（零 JS，Docsify 直接支持）。

## HTML 视图

<details open>
<summary>▸ 展开 / 收起（HTML+CSS 版）</summary>

<div class="arch-wrap">
  <div class="arch-flow">
    <div class="arch-node type-user">RGB 钱包</div>
    <div class="arch-arrow">→</div>
    <div class="arch-node type-btc">Bitcoin 链</div>
    <div class="arch-arrow">→</div>
    <div class="arch-node type-sidecar">sidecar<small>Rust · watch-only</small></div>
    <div class="arch-arrow">→</div>
    <div class="arch-node type-go">Go 桥<small>gRPC 编排</small></div>
    <div class="arch-arrow">→</div>
    <div class="arch-node type-c33">Chain33<small>rgbx 合约</small></div>
  </div>
</div>

<style>
.arch-wrap { margin: 12px 0; overflow-x: auto; }
.arch-flow { display: flex; align-items: center; gap: 6px; }
.arch-node {
  border: 1px solid var(--accent, #F7931A);
  border-radius: 6px;
  padding: 10px 14px;
  text-align: center;
  min-width: 74px;
  font-size: 14px;
  line-height: 1.3;
  white-space: nowrap;
}
.arch-node small { display: block; color: var(--muted, #888); font-size: 11px; margin-top: 3px; }
.arch-node.type-user { border-color: #4a90d9; }
.arch-node.type-btc { border-color: #888; }
.arch-node.type-sidecar { border-color: var(--accent, #F7931A); }
.arch-node.type-go { border-color: #9b59b6; }
.arch-node.type-c33 { border-color: #3cb371; }
.arch-arrow { color: var(--muted, #888); font-size: 16px; }
</style>

</details>

## Mermaid 视图

<details>
<summary>▸ 展开 / 收起（Mermaid 版）</summary>

```mermaid
flowchart LR
  U["RGB 钱包"] --> B["Bitcoin 链"]
  B --> S["sidecar<br/>Rust · watch-only"]
  S -->|gRPC 编排| G["Go 桥"]
  G --> C["Chain33<br/>rgbx 合约"]
```

</details>

---

**验证点**：
1. HTML 版用 `<div>`+scoped `<style>`，跟随 garden 主题（`--accent`）；
2. Mermaid 版由 beforeEach 钩子转成 `div.mermaid` 渲染；
3. 两者可独立展开/收起，互不干扰。
