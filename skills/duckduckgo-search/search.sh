#!/bin/bash
# DuckDuckGo 搜索脚本
# 无需API Key，立即可用

# 检查是否安装了 ddgr
if ! command -v ddgr &> /dev/null; then
    echo "正在安装 ddgr..."
    brew install ddgr 2>/dev/null || pip3 install ddgr 2>/dev/null
fi

# 获取搜索关键词
QUERY="$*"

if [ -z "$QUERY" ]; then
    echo "用法: $0 <搜索关键词>"
    echo "示例: $0 OpenClaw 最新版本"
    exit 1
fi

echo "🔍 搜索: $QUERY"
echo "=========================="

# 执行搜索并格式化输出
ddgr -n 10 --json "$QUERY" 2>/dev/null | python3 -c "
import json
import sys

try:
    results = json.load(sys.stdin)
    for i, r in enumerate(results, 1):
        print(f'{i}. {r[\"title\"]}')
        print(f'   URL: {r[\"url\"]}')
        print(f'   {r[\"abstract\"][:150]}...')
        print()
except:
    print('搜索完成')
" || ddgr -n 10 "$QUERY"
