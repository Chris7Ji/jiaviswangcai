#!/bin/bash
# AI News Daily Cron Wrapper
# 系统级定时任务包装脚本
# 创建时间: 2026-03-14

LOG_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/cron_log_$(date +%Y%m%d).txt"
WORKSPACE="/Users/jiyingguo/.openclaw/workspace"

echo "[$(date)] Starting AI news daily task..." >> "$LOG_FILE"

cd "$WORKSPACE" || exit 1

# 执行新闻脚本
if ./ai_news_daily.sh >> "$LOG_FILE" 2>&1; then
    echo "[$(date)] Task completed successfully" >> "$LOG_FILE"
    
    # 移动生成的文件到正确位置
    if [ -f "/tmp/ai_news_$(date +%Y%m%d).md" ]; then
        cp "/tmp/ai_news_$(date +%Y%m%d).md" "$WORKSPACE/news_summaries/ai_news_$(date +%Y-%m-%d).md"
        echo "[$(date)] File copied to news_summaries/" >> "$LOG_FILE"
    fi
    
    # 发送邮件通知
    if [ -f "/tmp/ai_news_email_$(date +%Y%m%d).txt" ]; then
        echo "[$(date)] Email ready to send" >> "$LOG_FILE"
    fi
    
    exit 0
else
    echo "[$(date)] Task failed with error code $?" >> "$LOG_FILE"
    exit 1
fi
