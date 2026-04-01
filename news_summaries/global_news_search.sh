#!/bin/bash
# 全球新闻搜索脚本 - 支持中英文多源搜索
# 使用 multi-search-engine 技能进行全球新闻采集

WORKSPACE="/Users/jiyingguo/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
NEWS_DIR="$WORKSPACE/news_summaries"

# 确保目录存在
mkdir -p "$NEWS_DIR"

echo "🌍 全球新闻采集任务启动"
echo "📅 日期: $DATE"
echo "=================================================="

# 定义搜索函数
search_global_news() {
    local topic=$1
    local keywords_cn=$2
    local keywords_en=$3
    local output_file=$4
    
    echo "🔍 搜索主题: $topic"
    echo "   中文关键词: $keywords_cn"
    echo "   英文关键词: $keywords_en"
    
    # 使用 Tavily 进行深度搜索（中英文）
    cd "$WORKSPACE"
    
    # 中文搜索
    echo "📡 执行中文搜索..."
    bash skills/tavily-search/search.sh "$keywords_cn" advanced 10 > /tmp/search_cn_$topic.txt 2>&1 || true
    
    # 英文搜索
    echo "📡 执行英文搜索..."
    bash skills/tavily-search/search.sh "$keywords_en" advanced 10 > /tmp/search_en_$topic.txt 2>&1 || true
    
    echo "✅ $topic 搜索完成"
    echo ""
}

# 1. AI新闻搜索
echo "【1/4】AI人工智能新闻..."
search_global_news "ai" \
    "人工智能 AI 大模型 机器学习 深度学习 2026年3月" \
    "artificial intelligence AI large language model machine learning deep learning March 2026" \
    "ai_news"

# 2. OpenClaw新闻搜索
echo "【2/4】OpenClaw新闻..."
search_global_news "openclaw" \
    "OpenClaw AI Agent 自动化 最新版本" \
    "OpenClaw AI agent automation MCP latest news March 2026" \
    "openclaw_news"

# 3. 健康长寿研究
echo "【3/4】健康长寿科研成果..."
search_global_news "health" \
    "长寿研究 抗衰老 健康科学 运动养生 饮食干预" \
    "longevity research anti-aging health science exercise nutrition March 2026" \
    "health_news"

# 4. 华为昇腾新闻
echo "【4/4】华为昇腾新闻..."
search_global_news "ascend" \
    "华为昇腾 昇腾AI芯片 CANN MindSpore 算子开发" \
    "Huawei Ascend AI chip CANN MindSpore operator development March 2026" \
    "ascend_news"

echo "=================================================="
echo "✅ 所有搜索任务完成"
echo "📁 临时结果保存在 /tmp/search_*.txt"
