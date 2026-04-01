#!/bin/bash

echo "🔍 检查所有定时任务状态"
echo "=========================================="

# 1. 列出所有定时任务
echo "1. 当前定时任务列表："
openclaw cron list

echo ""
echo "2. 检查各任务执行状态："
echo "=========================================="

# 2. 检查AI新闻任务
echo "📰 AI新闻每日摘要 (ID: 0bd3de5c-a4f9-4774-9511-75f344ba114c)"
if [ -f "/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-16.md" ]; then
    echo "✅ 今日报告已生成: ai_news_2026-03-16.md"
    echo "   文件大小: $(wc -l < /Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-16.md) 行"
else
    echo "❌ 今日报告未生成"
fi

echo ""

# 3. 检查健康长寿任务
echo "🩺 健康长寿科研成果监控 (ID: 784cee35-e004-40b4-a44a-a5102a930b7e)"
if [ -f "/Users/jiyingguo/.openclaw/workspace/news_summaries/health_longevity_2026-03-16.md" ]; then
    echo "✅ 今日报告已生成: health_longevity_2026-03-16.md"
    echo "   文件大小: $(wc -l < /Users/jiyingguo/.openclaw/workspace/news_summaries/health_longevity_2026-03-16.md) 行"
else
    echo "❌ 今日报告未生成（状态显示error）"
    echo "   可能原因：搜索API限制、脚本错误、权限问题"
fi

echo ""

# 4. 检查OpenClaw任务
echo "🦞 OpenClaw每日新闻监控 (ID: 5aa186d0-d623-41aa-bef3-352aec56eb20)"
if [ -f "/Users/jiyingguo/.openclaw/workspace/news_summaries/openclaw_news_high_quality_2026-03-16.md" ]; then
    echo "✅ 今日报告已生成: openclaw_news_high_quality_2026-03-16.md"
    echo "   文件大小: $(wc -l < /Users/jiyingguo/.openclaw/workspace/news_summaries/openclaw_news_high_quality_2026-03-16.md) 行"
else
    echo "❌ 今日报告未生成"
fi

echo ""

# 5. 检查昇腾AI任务
echo "🚀 华为昇腾新闻监控 (ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890)"
if [ -f "/Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_news_2026-03-16.md" ]; then
    echo "✅ 今日报告已生成: ascend_news_2026-03-16.md"
    echo "   文件大小: $(wc -l < /Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_news_2026-03-16.md) 行"
else
    echo "❌ 今日报告未生成"
fi

echo ""
echo "3. 检查日志文件："
echo "=========================================="

# 检查日志文件
for log in /Users/jiyingguo/.openclaw/workspace/news_summaries/cron_execution_*.log; do
    if [ -f "$log" ]; then
        task_name=$(basename "$log" | sed 's/cron_execution_//' | sed 's/\.log//')
        echo "📋 $task_name 日志:"
        echo "   文件: $(basename $log)"
        echo "   最后修改: $(date -r "$log" "+%Y-%m-%d %H:%M")"
        echo ""
    fi
done

echo "4. 问题诊断："
echo "=========================================="

# 检查健康长寿任务具体问题
echo "🔧 健康长寿任务问题诊断："
echo "1. 检查搜索API配置..."
if [ -z "$TAVILY_API_KEY" ]; then
    echo "   ❌ TAVILY_API_KEY 环境变量未设置"
else
    echo "   ✅ TAVILY_API_KEY 已配置"
fi

echo "2. 检查脚本权限..."
if [ -f "/Users/jiyingguo/.openclaw/workspace/scripts/health_longevity_monitor.sh" ]; then
    if [ -x "/Users/jiyingguo/.openclaw/workspace/scripts/health_longevity_monitor.sh" ]; then
        echo "   ✅ 脚本有执行权限"
    else
        echo "   ❌ 脚本无执行权限，运行: chmod +x /Users/jiyingguo/.openclaw/workspace/scripts/health_longevity_monitor.sh"
    fi
else
    echo "   ❌ 脚本文件不存在"
fi

echo "3. 检查输出目录..."
if [ -d "/Users/jiyingguo/.openclaw/workspace/news_summaries" ]; then
    echo "   ✅ 输出目录存在且有写入权限"
else
    echo "   ❌ 输出目录不存在"
fi

echo ""
echo "5. 建议修复步骤："
echo "=========================================="
echo "1. 重新配置健康长寿任务："
echo "   openclaw cron delete 784cee35-e004-40b4-a44a-a5102a930b7e"
echo "   openclaw cron add --name '健康长寿科研成果监控' --schedule '0 7 * * *' --command 'cd /Users/jiyingguo/.openclaw/workspace && ./scripts/health_longevity_monitor.sh'"
echo ""
echo "2. 检查环境变量："
echo "   echo \$TAVILY_API_KEY"
echo "   echo \$GEMINI_API_KEY"
echo ""
echo "3. 手动测试脚本："
echo "   cd /Users/jiyingguo/.openclaw/workspace && ./scripts/health_longevity_monitor.sh"
echo ""
echo "✅ 检查完成"