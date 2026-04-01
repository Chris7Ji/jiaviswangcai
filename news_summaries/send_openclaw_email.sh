#!/bin/bash
# OpenClaw和AI新闻每日摘要自动邮件发送脚本
# 在定时任务生成新闻后自动调用

set -e

# 配置
EMAIL_PASSWORD="icxhfzuyzbhbbjie"
SENDER_EMAIL="86940135@qq.com"
RECIPIENTS=("86940135@qq.com" "jiyingguo@huawei.com")
NEWS_DIR="/Users/jiyingguo/.openclaw/workspace/news_summaries"
SEND_EMAIL_SCRIPT="/Users/jiyingguo/.openclaw/workspace/news_summaries/send_combined_email.py"

# 获取今天的日期
TODAY=$(date +%Y-%m-%d)

echo "=========================================="
echo "OpenClaw + AI新闻每日摘要 - 自动邮件发送"
echo "=========================================="
echo "日期: $TODAY"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 检查OpenClaw新闻文件是否存在
OPENCLAW_MD_FILE="$NEWS_DIR/openclaw_news_high_quality_${TODAY}.md"
OPENCLAW_JSON_FILE="$NEWS_DIR/openclaw_news_high_quality_${TODAY}.json"

# 检查AI新闻文件是否存在
AI_MD_FILE="$NEWS_DIR/ai_news_${TODAY}.md"
AI_HTML_FILE="$NEWS_DIR/ai_news_${TODAY}.html"

# 检查至少有一种新闻文件存在
if [ ! -f "$OPENCLAW_MD_FILE" ] && [ ! -f "$AI_MD_FILE" ]; then
    echo "❌ 错误: 找不到今天的新闻文件"
    echo "   - OpenClaw: $OPENCLAW_MD_FILE"
    echo "   - AI新闻: $AI_MD_FILE"
    exit 1
fi

if [ -f "$OPENCLAW_MD_FILE" ]; then
    echo "✅ OpenClaw新闻文件已找到: $OPENCLAW_MD_FILE"
else
    echo "⚠️  OpenClaw新闻文件不存在"
fi

if [ -f "$AI_MD_FILE" ]; then
    echo "✅ AI新闻文件已找到: $AI_MD_FILE"
else
    echo "⚠️  AI新闻文件不存在"
fi

# 检查邮件发送脚本是否存在
if [ ! -f "$SEND_EMAIL_SCRIPT" ]; then
    echo "❌ 错误: 找不到邮件发送脚本: $SEND_EMAIL_SCRIPT"
    exit 1
fi

echo "✅ 邮件发送脚本已找到"

# 发送邮件
echo ""
echo "📧 正在发送邮件..."
echo "   发件人: $SENDER_EMAIL"
echo "   收件人: ${RECIPIENTS[*]}"
echo ""

export EMAIL_PASSWORD
export TODAY
python3 "$SEND_EMAIL_SCRIPT"

SEND_STATUS=$?

if [ $SEND_STATUS -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 邮件发送成功!"
    echo "=========================================="
    
    # 记录发送日志
    LOG_FILE="$NEWS_DIR/combined_email_sent_${TODAY}.log"
    echo "OpenClaw + AI新闻邮件发送成功" > "$LOG_FILE"
    echo "发送时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    echo "收件人: ${RECIPIENTS[*]}" >> "$LOG_FILE"
    if [ -f "$OPENCLAW_MD_FILE" ]; then
        echo "OpenClaw文件: $OPENCLAW_MD_FILE" >> "$LOG_FILE"
    fi
    if [ -f "$AI_MD_FILE" ]; then
        echo "AI新闻文件: $AI_MD_FILE" >> "$LOG_FILE"
    fi
    
    exit 0
else
    echo ""
    echo "=========================================="
    echo "❌ 邮件发送失败!"
    echo "=========================================="
    
    # 记录错误日志
    ERROR_FILE="$NEWS_DIR/combined_email_error_${TODAY}.log"
    echo "OpenClaw + AI新闻邮件发送失败" > "$ERROR_FILE"
    echo "错误时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$ERROR_FILE"
    echo "错误码: $SEND_STATUS" >> "$ERROR_FILE"
    
    exit 1
fi
