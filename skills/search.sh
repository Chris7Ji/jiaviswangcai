#!/bin/bash
# 统一搜索脚本 - 智能选择搜索引擎
# 创建时间: 2026-03-14

KEYWORD="$1"
ENGINE="${2:-tavily}"  # 默认使用tavily

echo "🔍 搜索: $KEYWORD"
echo "引擎: $ENGINE"
echo "=================================================="

case "$ENGINE" in
    tavily|tav)
        bash /Users/jiyingguo/.openclaw/workspace/skills/tavily-search/search.sh "$KEYWORD" basic 5
        ;;
    duck|duckduckgo|ddg)
        python3 /Users/jiyingguo/.openclaw/workspace/skills/duckduckgo-search/duckduckgo_search.py "$KEYWORD"
        ;;
    multi|all)
        echo "使用 Multi Search Engine..."
        echo "Google: https://www.google.com/search?q=$KEYWORD"
        echo "DuckDuckGo: https://duckduckgo.com/html/?q=$KEYWORD"
        echo "百度: https://www.baidu.com/s?wd=$KEYWORD"
        ;;
    *)
        echo "未知引擎，使用默认Tavily"
        bash /Users/jiyingguo/.openclaw/workspace/skills/tavily-search/search.sh "$KEYWORD" basic 5
        ;;
esac
