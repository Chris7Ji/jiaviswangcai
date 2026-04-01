#!/bin/bash
# AI新闻每日摘要完整任务脚本
# 1. 生成新闻摘要 2. 发送邮件

set -e

echo "=========================================="
echo "AI新闻每日摘要 - 完整任务执行"
echo "=========================================="
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 步骤1: 调用OpenClaw生成新闻摘要
echo ""
echo "📰 步骤1: 生成AI新闻摘要..."
echo "   正在调用OpenClaw cron任务..."

# 使用openclaw cron run执行定时任务
openclaw cron run --id 0bd3de5c-a4f9-4774-9511-75f344ba114c

echo "✅ 新闻摘要生成完成"

# 等待文件生成（给系统一点时间）
echo ""
echo "⏳ 等待文件写入完成..."
sleep 5

# 步骤2: 发送邮件
echo ""
echo "📧 步骤2: 发送邮件..."

AUTO_SEND_SCRIPT="/Users/jiyingguo/.openclaw/workspace/news_summaries/auto_send_email.sh"

if [ -f "$AUTO_SEND_SCRIPT" ]; then
    bash "$AUTO_SEND_SCRIPT"
    EMAIL_STATUS=$?
    
    if [ $EMAIL_STATUS -eq 0 ]; then
        echo "✅ 邮件发送成功"
    else
        echo "⚠️ 邮件发送失败，但新闻文件已生成"
    fi
else
    echo "⚠️ 找不到自动邮件发送脚本: $AUTO_SEND_SCRIPT"
fi

echo ""
echo "=========================================="
echo "✅ 完整任务执行完毕"
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
