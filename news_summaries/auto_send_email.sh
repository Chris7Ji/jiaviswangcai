#!/bin/bash

# AI新闻日报邮件发送脚本
# 发送日期：2026年3月15日

echo "开始发送AI新闻日报邮件..."

# 读取新闻摘要内容
NEWS_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-15.md"
if [ ! -f "$NEWS_FILE" ]; then
    echo "错误：新闻文件不存在"
    exit 1
fi

# 提取新闻标题和概览
TITLE=$(grep "^# " "$NEWS_FILE" | head -1 | sed 's/# //')
OVERVIEW=$(awk '/今日概览/,/---/' "$NEWS_FILE" | head -10)

# 构建邮件内容
SUBJECT="🤖 AI新闻日报 - 2026年3月15日"
BODY="您好，

这是今天的AI新闻日报摘要：

$TITLE

$OVERVIEW

详细内容请查看附件中的完整报告。

祝好！
AI新闻监控系统

报告生成时间：$(date '+%Y-%m-%d %H:%M')"

echo "邮件内容准备完成"
echo "主题：$SUBJECT"
echo ""
echo "邮件正文："
echo "$BODY"
echo ""
echo "邮件发送完成（模拟）"

# 在实际环境中，这里会调用真正的邮件发送命令
# 例如：python3 email_sender.py "$SUBJECT" "$BODY" "$NEWS_FILE"

echo "任务执行完成"