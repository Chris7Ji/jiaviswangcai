#!/bin/bash
# 健康长寿科研成果监控报告自动邮件发送脚本
# 在定时任务生成报告后自动调用

set -e

# 配置
EMAIL_PASSWORD="swqfjvmoupdebhgh"
SENDER_EMAIL="86940135@qq.com"
RECIPIENTS=("86940135@qq.com" "jiyingguo@huawei.com")
WORKSPACE_DIR="/Users/jiyingguo/.openclaw/workspace"
SEND_EMAIL_SCRIPT="$WORKSPACE_DIR/send_health_email.py"

# 获取今天的日期
TODAY=$(date +%Y-%m-%d)

echo "=========================================="
echo "健康长寿科研成果监控 - 自动邮件发送"
echo "=========================================="
echo "日期: $TODAY"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 查找今天的健康报告文件
REPORT_FILE="$WORKSPACE_DIR/健康长寿科研成果监控报告_${TODAY}.md"

# 如果找不到今天的文件，找最新的文件
if [ ! -f "$REPORT_FILE" ]; then
    echo "⚠️  未找到今天的报告文件，搜索最新文件..."
    REPORT_FILE=$(find "$WORKSPACE_DIR" -name "健康长寿科研成果监控报告_*.md" -type f -exec stat -f '%m %N' {} \; | sort -n | tail -1 | cut -d' ' -f2-)
    
    if [ -z "$REPORT_FILE" ]; then
        echo "❌ 错误: 找不到任何健康报告文件"
        exit 1
    fi
    
    echo "✅ 找到最新报告文件: $REPORT_FILE"
else
    echo "✅ 今天的报告文件已找到: $REPORT_FILE"
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
export REPORT_FILE
python3 "$SEND_EMAIL_SCRIPT"

SEND_STATUS=$?

if [ $SEND_STATUS -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 邮件发送成功!"
    echo "=========================================="
    
    # 记录发送日志
    LOG_FILE="$WORKSPACE_DIR/health_email_sent_${TODAY}.log"
    echo "健康长寿报告邮件发送成功" > "$LOG_FILE"
    echo "发送时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    echo "收件人: ${RECIPIENTS[*]}" >> "$LOG_FILE"
    echo "文件: $REPORT_FILE" >> "$LOG_FILE"
    
    exit 0
else
    echo ""
    echo "=========================================="
    echo "❌ 邮件发送失败!"
    echo "=========================================="
    
    # 记录错误日志
    ERROR_FILE="$WORKSPACE_DIR/health_email_error_${TODAY}.log"
    echo "健康长寿报告邮件发送失败" > "$ERROR_FILE"
    echo "错误时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$ERROR_FILE"
    echo "错误码: $SEND_STATUS" >> "$ERROR_FILE"
    
    exit 1
fi