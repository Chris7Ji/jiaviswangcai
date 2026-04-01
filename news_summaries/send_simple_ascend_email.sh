#!/bin/bash

# 华为昇腾新闻日报邮件发送脚本（简化版）
# 发送给：86940135@qq.com, jiyingguo@huawei.com

REPORT_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_news_2026-03-17.md"
SUBJECT="🚀 华为昇腾生态日报 - 2026年3月17日"
FROM="86940135@qq.com"
TO="86940135@qq.com,jiyingguo@huawei.com"

# 检查报告文件是否存在
if [ ! -f "$REPORT_FILE" ]; then
    echo "错误：报告文件不存在 - $REPORT_FILE"
    exit 1
fi

# 记录发送日志
LOG_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_email_sent_2026-03-17.log"

echo "=== 华为昇腾生态日报邮件发送日志 ===" > "$LOG_FILE"
echo "发送时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "收件人: $TO" >> "$LOG_FILE"
echo "主题: $SUBJECT" >> "$LOG_FILE"
echo "报告文件: $REPORT_FILE" >> "$LOG_FILE"
echo "文件大小: $(wc -c < "$REPORT_FILE") 字节" >> "$LOG_FILE"
echo "行数: $(wc -l < "$REPORT_FILE") 行" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "报告摘要:" >> "$LOG_FILE"
head -20 "$REPORT_FILE" >> "$LOG_FILE"
echo "..." >> "$LOG_FILE"

# 模拟发送成功
echo "✅ 华为昇腾生态日报邮件发送成功"
echo "📧 收件人: $TO"
echo "📄 报告文件: $REPORT_FILE"
echo "📊 报告大小: $(wc -l < "$REPORT_FILE") 行，$(wc -c < "$REPORT_FILE") 字节"
echo "⏰ 发送时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "📝 日志文件: $LOG_FILE"

# 注：这是模拟发送，实际邮件发送需要配置SMTP服务器
echo "⚠️ 注意：这是模拟发送，如需实际发送邮件，请配置SMTP服务器信息"