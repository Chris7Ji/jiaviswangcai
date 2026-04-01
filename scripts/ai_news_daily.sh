#!/bin/bash
# 高校分队-AI新闻每日简报脚本（高质量实时版）
# 执行时间：每天 06:15 (北京时间)

echo "=== 高校分队-AI新闻每日简报 ==="
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 设置环境变量
export TAVILY_API_KEY="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"
export GEMINI_API_KEY="$(cat ~/.openclaw/workspace/.env | grep GEMINI_API_KEY | cut -d'=' -f2)"

# 2. 创建新闻简报
echo "正在搜索过去24-48小时内的AI新闻..."
echo "搜索策略：只看真实事件，排除分析预测类文章"
echo ""

# 3. 使用新策略生成简报
TODAY=$(date '+%Y-%m-%d')
HTML_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_brief_${TODAY}.html"

echo "执行Python搜索脚本..."
python3 "/Users/jiyingguo/.openclaw/workspace/scripts/ai_news_search.py" > "$HTML_FILE"

if [ $? -eq 0 ]; then
    echo "简报已生成: $HTML_FILE"
    echo "文件大小: $(wc -c < "$HTML_FILE") 字节"
else
    echo "错误：新闻搜索失败"
    exit 1
fi

echo ""

# 4. 发送邮件
echo "正在发送邮件..."
echo "收件人: jiyingguo@huawei.com, xushengsheng@huawei.com, 86940135@qq.com"
echo ""

# 使用华为邮箱兼容脚本发送
if [ -f "/Users/jiyingguo/.openclaw/workspace/scripts/huawei_compatible_sender.py" ]; then
    # 提取最重磅新闻标题作为邮件主题
    MAIL_SUBJECT="2026年3月19日 高校分队- AI 新闻每日简报"
    
    # 发送邮件
    python3 "/Users/jiyingguo/.openclaw/workspace/scripts/huawei_compatible_sender.py" \
        --html "$HTML_FILE" \
        --subject "$MAIL_SUBJECT"
    
    if [ $? -eq 0 ]; then
        echo "✅ 邮件发送完成！"
    else
        echo "❌ 邮件发送失败"
        exit 1
    fi
else
    echo "错误：华为邮箱兼容脚本不存在"
    echo "请检查: /Users/jiyingguo/.openclaw/workspace/scripts/huawei_compatible_sender.py"
    exit 1
fi

echo ""
echo "=== 任务完成 ==="