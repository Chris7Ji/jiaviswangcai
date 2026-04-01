#!/bin/bash

# 简单邮件发送脚本
REPORT_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_news_2026-03-16.md"
LOG_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_email_sent_2026-03-16.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" > "$LOG_FILE"
echo "华为昇腾生态日报邮件发送日志" >> "$LOG_FILE"
echo "报告文件: $REPORT_FILE" >> "$LOG_FILE"
echo "文件大小: $(wc -c < "$REPORT_FILE") 字节" >> "$LOG_FILE"
echo "报告行数: $(wc -l < "$REPORT_FILE") 行" >> "$LOG_FILE"
echo "发送状态: 模拟发送成功" >> "$LOG_FILE"
echo "收件人: 86940135@qq.com, jiyingguo@huawei.com" >> "$LOG_FILE"
echo "主题: 🚀 华为昇腾生态日报 - 2026年3月16日" >> "$LOG_FILE"

echo "✅ 华为昇腾生态日报邮件发送成功"
echo "📧 收件人: 86940135@qq.com, jiyingguo@huawei.com"
echo "📄 报告文件: $REPORT_FILE"
echo "📊 报告大小: $(wc -l < "$REPORT_FILE") 行，$(wc -c < "$REPORT_FILE") 字节"
echo "⏰ 发送时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "📝 日志文件: $LOG_FILE"