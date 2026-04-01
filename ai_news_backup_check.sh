#!/bin/bash
# AI News Backup Check Script
# 如果主任务失败，执行备用任务
# 创建时间: 2026-03-14

WORKSPACE="/Users/jiyingguo/.openclaw/workspace"
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$WORKSPACE/news_summaries/ai_news_$TODAY.md"
LOG_FILE="$WORKSPACE/news_summaries/backup_check_$(date +%Y%m%d).log"

echo "[$(date)] Checking for today's news file..." >> "$LOG_FILE"

if [ ! -f "$TODAY_FILE" ]; then
    echo "[$(date)] News file not found, running backup task..." >> "$LOG_FILE"
    
    cd "$WORKSPACE" || exit 1
    
    # 执行备用任务
    if ./ai_news_daily.sh >> "$LOG_FILE" 2>&1; then
        echo "[$(date)] Backup task completed" >> "$LOG_FILE"
        
        # 复制文件
        if [ -f "/tmp/ai_news_$(date +%Y%m%d).md" ]; then
            cp "/tmp/ai_news_$(date +%Y%m%d).md" "$TODAY_FILE"
            echo "[$(date)] File copied successfully" >> "$LOG_FILE"
        fi
    else
        echo "[$(date)] Backup task also failed" >> "$LOG_FILE"
    fi
else
    echo "[$(date)] News file already exists, skipping backup" >> "$LOG_FILE"
fi
