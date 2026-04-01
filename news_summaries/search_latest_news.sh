#!/bin/bash
# 搜索过去24小时最新AI新闻

echo "🔍 搜索过去24小时最新AI新闻 (2026-03-15 08:00 至 2026-03-16 08:00)"
echo "=========================================================="

# 1. 检查OpenAI官方博客最新文章
echo "1. 检查OpenAI官方博客..."
curl -s "https://openai.com/blog" | grep -E "(2026-03-1[56]|March 1[56], 2026)" | head -5

echo ""

# 2. 检查Google AI Blog
echo "2. 检查Google AI Blog..."
curl -s "https://blog.google/technology/ai/" | grep -E "(2026-03-1[56]|March 1[56], 2026)" | head -5

echo ""

# 3. 检查华为昇腾新闻
echo "3. 检查华为昇腾新闻..."
curl -s "https://www.huawei.com/cn/news/cn/ascend" | grep -E "(2026-03-1[56]|3月1[56]日)" | head -5

echo ""

# 4. 检查深度求索官方动态
echo "4. 检查深度求索官方动态..."
curl -s "https://www.deepseek.com/news" | grep -E "(2026-03-1[56]|3月1[56]日)" | head -5

echo ""

# 5. 检查Meta AI最新发布
echo "5. 检查Meta AI最新发布..."
curl -s "https://ai.meta.com/blog/" | grep -E "(2026-03-1[56]|March 1[56], 2026)" | head -5

echo ""
echo "✅ 搜索完成"