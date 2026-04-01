#!/bin/bash
# Tavily搜索脚本 - 使用虚拟环境

VENV_PATH="/Users/jiyingguo/.openclaw/workspace/venv_tavily"
API_KEY="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"

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: $0 <搜索关键词> [basic|advanced] [数量]"
    echo "示例: $0 'OpenClaw 最新版本' basic 5"
    exit 1
fi

QUERY="$1"
DEPTH="${2:-basic}"
MAX_RESULTS="${3:-10}"

echo "🔍 Tavily搜索: $QUERY"
echo "   深度: $DEPTH, 数量: $MAX_RESULTS"
echo "=================================================="

# 使用虚拟环境运行Python
source "$VENV_PATH/bin/activate"

python3 << EOF
from tavily import TavilyClient
import json

api_key = "$API_KEY"
client = TavilyClient(api_key=api_key)

try:
    response = client.search(
        query="$QUERY",
        search_depth="$DEPTH",
        max_results=$MAX_RESULTS,
        include_answer=True,
        include_raw_content=True
    )
    
    # 显示AI答案
    answer = response.get('answer')
    if answer:
        print("🤖 AI摘要:")
        print(answer)
        print()
        print("=" * 50)
        print()
    
    # 显示结果
    results = response.get('results', [])
    print(f"📊 找到 {len(results)} 条结果:\n")
    
    for i, r in enumerate(results, 1):
        title = r.get('title', '无标题')
        url = r.get('url', '')
        content = r.get('content', '')[:200]
        score = r.get('score', 0)
        
        print(f"{i}. {title} (相关度: {score:.2f})")
        print(f"   URL: {url}")
        print(f"   {content}...")
        print()
    
    # 保存完整结果
    with open('/tmp/tavily_search_result.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
    print(f"💾 完整结果已保存到: /tmp/tavily_search_result.json")
    
except Exception as e:
    print(f"❌ 搜索失败: {e}")
    exit(1)
EOF

deactivate
