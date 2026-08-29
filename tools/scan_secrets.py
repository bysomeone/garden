#!/usr/bin/env python3
"""garden push 前守卫：扫描敏感内容、私密标记、大文件/二进制。

命中以下任一即返回非 0（拦截 push）：
1. 敏感内容：私钥头、助记词、常见 API token/密钥模式
2. 私密标记：文件内容含 `visibility: private`
3. 大文件 / 非白名单二进制（阈值见下方常量）

用法：python3 tools/scan_secrets.py [repo_root]   （默认仓库根）
"""
import re
import sys
from pathlib import Path

MAX_TEXT_SIZE = 5 * 1024 * 1024      # 文本 >5MB 拦截
MAX_IMAGE_SIZE = 2 * 1024 * 1024     # 图片 >2MB 拦截
ALLOW_BIN_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico"}
# assets/ 为第三方/静态资源（如 mermaid.min.js），受信任，跳过（压缩 JS 易误报敏感模式）
SKIP_DIRS = {".git", "tools", ".githooks", "node_modules", "assets"}

# 敏感模式（命中即拦）
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----", re.I),
    re.compile(r"\b(?:[a-z]+ ){11,23}(?:[a-z]+)\b", re.I),  # 12/24 词助记词（宽松）
    re.compile(r"(?i)(api[_-]?key|secret|token|passwd|password)\s*[=:]\s*['\"][A-Za-z0-9_\-]{16,}"),
    re.compile(r"\b(0x)?[a-f0-9]{64}\b"),                    # 64 hex（如私钥/种子）
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),                    # AWS
    re.compile(r"\bghp_[A-Za-z0-9]{36,}\b"),                # GitHub token
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),        # Slack
]

PRIVATE_MARKER = re.compile(r"^\s*visibility\s*:\s*private\s*$", re.M)

def is_binary(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            return b"\x00" in f.read(8192)
    except OSError:
        return True

def scan(root: Path) -> int:
    blocked = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        rel = path.relative_to(root).as_posix()
        size = path.stat().st_size

        # 3) 大文件 / 二进制
        ext = path.suffix.lower()
        if ext in ALLOW_BIN_EXT:
            if size > MAX_IMAGE_SIZE:
                blocked.append(f"{rel}  (图片 > {MAX_IMAGE_SIZE//1024//1024}MB)")
            continue
        if size > MAX_TEXT_SIZE or is_binary(path):
            blocked.append(f"{rel}  (大文件/二进制，{size} 字节)")
            continue

        # 1) 敏感内容 + 2) 私密标记
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            blocked.append(f"{rel}  (读取失败: {e})")
            continue
        if PRIVATE_MARKER.search(text):
            blocked.append(f"{rel}  (含 visibility: private 私密标记)")
            continue
        for pat in SECRET_PATTERNS:
            m = pat.search(text)
            if m:
                blocked.append(f"{rel}  (命中敏感模式: {pat.pattern[:40]}…)")
                break

    if blocked:
        print("scan_secrets: 发现以下内容，已拦截 push：")
        for line in blocked:
            print("  - " + line)
        print("请处理后再 push（移除私密标记/敏感内容/大文件，或确认无碍后移除这些文件）。")
        return 1
    print("scan_secrets: 通过")
    return 0

if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    sys.exit(scan(root))
