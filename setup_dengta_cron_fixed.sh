#!/bin/bash
# 高校分队灯塔项目定时任务配置脚本（修正版）

echo "🎯 配置高校分队灯塔项目定时任务..."

# 任务1：AI 新闻每日简报（06:30）
echo "📧 创建 AI 新闻每日简报定时任务..."
openclaw cron add \
  --name "高校分队 AI 新闻每日简报" \
  --schedule "30 6 * * * Asia/Shanghai" \
  --command "python3 /Users/jiyingguo/.openclaw/workspace/send_ai_news_daily.py"

if [ $? -eq 0 ]; then
    echo "✅ AI 新闻每日简报定时任务创建成功"
else
    echo "❌ AI 新闻每日简报定时任务创建失败"
fi

# 任务2：灯塔学校每日动态（06:45）
echo "💬 创建灯塔学校每日动态定时任务..."
openclaw cron add \
  --name "高校分队-灯塔学校的每日动态" \
  --schedule "45 6 * * * Asia/Shanghai" \
  --command "python3 /Users/jiyingguo/.openclaw/workspace/send_dengta_final.py"

if [ $? -eq 0 ]; then
    echo "✅ 灯塔学校每日动态定时任务创建成功"
else
    echo "❌ 灯塔学校每日动态定时任务创建失败"
fi

echo ""
echo "📋 验证任务列表:"
openclaw cron list

echo ""
echo "🎉 配置完成！"