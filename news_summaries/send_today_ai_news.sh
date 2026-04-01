#!/bin/bash

# AI新闻日报邮件发送脚本
# 发送日期：2026年3月17日

echo "开始发送AI新闻日报邮件..."

# 读取新闻摘要内容
NEWS_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-17.md"
if [ ! -f "$NEWS_FILE" ]; then
    echo "错误：新闻文件不存在"
    exit 1
fi

# 提取新闻标题和概览
TITLE=$(grep "^# " "$NEWS_FILE" | head -1 | sed 's/# //')
OVERVIEW=$(awk '/今日概览/,/---/' "$NEWS_FILE" | head -10)

# 构建邮件内容
SUBJECT="🤖 AI新闻日报 - 2026年3月17日"
BODY="您好，

这是今天的AI新闻日报摘要：

$TITLE

$OVERVIEW

今日重磅新闻：
1. Perplexity宣布放弃MCP，转向API和CLI集成
2. Meta收购AI Agent社交网站Moltbook  
3. OpenAI发布GPT-4.5技术预览版
4. 华为昇腾发布新一代AI训练芯片
5. Google发布Gemini 3.0 Ultra版本
6. Anthropic发布Claude 4企业版
7. 国内大模型公司融资活跃
8. AI在医疗诊断领域取得突破

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
echo "正在发送邮件..."

# 使用现有的邮件发送脚本
python3 /Users/jiyingguo/.openclaw/workspace/news_summaries/send_email_safe.py "$SUBJECT" "$BODY" "$NEWS_FILE"

if [ $? -eq 0 ]; then
    echo "邮件发送成功"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - AI新闻日报邮件已发送" >> /Users/jiyingguo/.openclaw/workspace/news_summaries/email_sent_2026-03-17.log
else
    echo "邮件发送失败"
    exit 1
fi

echo "任务执行完成"