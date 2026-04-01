#!/bin/bash

# AI新闻每日摘要邮件发送脚本（简化版）
# 使用系统mail命令发送邮件

# 获取当前日期
TODAY=$(date +"%Y-%m-%d")

# 文件路径
MD_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_${TODAY}.md"
HTML_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_${TODAY}.html"

# 检查文件是否存在
if [ ! -f "$MD_FILE" ]; then
    echo "错误：Markdown文件不存在: $MD_FILE"
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo "错误：HTML文件不存在: $HTML_FILE"
    exit 1
fi

echo "开始发送AI新闻每日摘要邮件..."
echo "发送时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "发件人: AI新闻摘要系统 <noreply@ai-news.com>"
echo "收件人: 86940135@qq.com, jiyingguo@huawei.com"
echo "主题: AI新闻每日摘要 - $(date '+%Y年%m月%d日')"

# 读取Markdown文件内容
MD_CONTENT=$(cat "$MD_FILE")

# 创建邮件内容
MAIL_CONTENT="AI新闻每日摘要 - $(date '+%Y年%m月%d日')

您好！

以下是今日的AI新闻每日摘要，包含4条重要AI新闻：

$(head -n 100 "$MD_FILE")

完整内容请查看附件或访问HTML版本。

--
AI新闻每日摘要系统
自动生成于 $(date '+%Y-%m-%d %H:%M:%S')
"

# 尝试发送邮件（需要系统配置了邮件发送）
echo "尝试发送邮件..."

# 方法1：使用mail命令（需要系统配置）
if command -v mail &> /dev/null; then
    echo "$MAIL_CONTENT" | mail -s "AI新闻每日摘要 - $(date '+%Y年%m月%d日')" -c "86940135@qq.com" "jiyingguo@huawei.com"
    if [ $? -eq 0 ]; then
        echo "邮件发送成功！"
    else
        echo "邮件发送失败，请检查系统邮件配置"
    fi
else
    echo "系统mail命令不可用"
fi

echo "任务完成！"
echo "新闻摘要文件已保存到："
echo "  Markdown: $MD_FILE"
echo "  HTML: $HTML_FILE"