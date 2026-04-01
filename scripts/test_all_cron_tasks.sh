#!/bin/bash
# 定时任务统一执行脚本
# 测试所有5个定时任务

echo "=========================================="
echo "定时任务统一测试"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

export TAVILY_API_KEY="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"

# 任务1: AI新闻摘要 (06:30)
echo ""
echo "📰 [任务1/5] AI新闻摘要..."
python3 /Users/jiyingguo/.openclaw/workspace/scripts/ai_news_daily.py >> /tmp/cron_test.log 2>&1
if [ $? -eq 0 ]; then
    echo "✅ AI新闻摘要 - 成功"
else
    echo "❌ AI新闻摘要 - 失败"
fi

# 任务2: B站热门视频 (07:30)
echo ""
echo "📺 [任务2/5] B站热门视频日报..."
python3 /Users/jiyingguo/.openclaw/workspace/scripts/bilibili_daily.py >> /tmp/cron_test.log 2>&1
if [ $? -eq 0 ]; then
    echo "✅ B站热门视频日报 - 成功"
else
    echo "❌ B站热门视频日报 - 失败"
fi

# 任务3: 教育行业AI资讯 (08:00)
echo ""
echo "📚 [任务3/5] 教育行业AI资讯..."
python3 /Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.py >> /tmp/cron_test.log 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 教育行业AI资讯 - 成功"
else
    echo "❌ 教育行业AI资讯 - 失败"
fi

# 任务4: 股票监控提醒 (08:30)
echo ""
echo "📈 [任务4/5] 股票监控提醒..."
python3 /Users/jiyingguo/.openclaw/workspace/scripts/stock_monitor_daily.py >> /tmp/cron_test.log 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 股票监控提醒 - 成功"
else
    echo "❌ 股票监控提醒 - 失败"
fi

# 任务5: 每日工作日报 (09:00)
echo ""
echo "📋 [任务5/5] 每日工作日报..."
python3 /Users/jiyingguo/.openclaw/workspace/scripts/daily_work_report.py >> /tmp/cron_test.log 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 每日工作日报 - 成功"
else
    echo "❌ 每日工作日报 - 失败"
fi

echo ""
echo "=========================================="
echo "测试完成!"
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "日志文件: /tmp/cron_test.log"
echo "=========================================="