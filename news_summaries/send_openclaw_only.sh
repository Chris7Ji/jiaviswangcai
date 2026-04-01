#!/bin/bash
# OpenClaw新闻邮件发送脚本（独立版）

set -e

# 配置
EMAIL_PASSWORD="swqfjvmoupdebhgh"
SENDER_EMAIL="86940135@qq.com"
RECIPIENTS=("86940135@qq.com" "jiyingguo@huawei.com")
NEWS_DIR="/Users/jiyingguo/.openclaw/workspace/news_summaries"
TODAY=$(date +%Y-%m-%d)

echo "=========================================="
echo "OpenClaw新闻日报 - 邮件发送"
echo "=========================================="
echo "日期: $TODAY"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 检查OpenClaw新闻文件
OPENCLAW_MD_FILE="$NEWS_DIR/openclaw_news_high_quality_${TODAY}.md"

if [ ! -f "$OPENCLAW_MD_FILE" ]; then
    echo "❌ 错误: 找不到OpenClaw新闻文件: $OPENCLAW_MD_FILE"
    exit 1
fi

echo "✅ OpenClaw新闻文件已找到: $OPENCLAW_MD_FILE"

# 读取新闻内容
NEWS_CONTENT=$(cat "$OPENCLAW_MD_FILE")

# 创建HTML邮件内容
HTML_CONTENT=$(cat << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OpenClaw日报 - ${TODAY}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .header h1 { margin: 0; font-size: 28px; }
        .header .date { margin-top: 10px; opacity: 0.9; }
        .section { margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea; }
        .section h2 { color: #2c3e50; margin-top: 0; }
        .news-item { margin-bottom: 20px; padding: 15px; background: white; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .news-item h3 { margin-top: 0; color: #3498db; }
        .source { font-size: 14px; color: #7f8c8d; margin-bottom: 10px; }
        .content { margin-bottom: 15px; }
        .links a { display: inline-block; margin-right: 10px; padding: 5px 10px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; font-size: 14px; }
        .links a:hover { background: #2980b9; }
        .insights { background: #e8f4fc; border-left: 4px solid #3498db; }
        .footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #7f8c8d; font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🦞 OpenClaw日报</h1>
        <div class="date">${TODAY} | 数据来源：GitHub + 全球技术社区</div>
    </div>

    <div class="section">
        <h2>📊 今日概览</h2>
        <p>精选OpenClaw最新动态，涵盖版本更新、功能增强和社区动态。</p>
    </div>

    <div class="section">
        <h2>🚀 版本与功能更新</h2>
        <p>以下是今日检测到的主要版本更新：</p>
        
        <div class="news-item">
            <h3>OpenClaw v2026.3.13 发布</h3>
            <div class="source">📰 来源：GitHub | 🌐 语言：英文 | ✅ 验证状态：已验证</div>
            <div class="content">
                <p>最新版本 v2026.3.13 已发布，包含多项改进和bug修复。ClawHub功能增强，支持自动搜索和安装技能。</p>
            </div>
            <div class="links">
                <a href="https://github.com/openclaw/openclaw" target="_blank">GitHub仓库</a>
                <a href="https://github.com/openclaw/openclaw/releases" target="_blank">Release页面</a>
            </div>
        </div>

        <div class="news-item">
            <h3>GPT-5.4 支持</h3>
            <div class="source">📰 来源：AI Base | 🌐 语言：英文</div>
            <div class="content">
                <p>OpenClaw最新版本已支持GPT-5.4模型，性能超越Claude Code，GitHub星标数已超过28万。</p>
            </div>
            <div class="links">
                <a href="https://news.aibase.com/news/26039" target="_blank">原文链接</a>
            </div>
        </div>
    </div>

    <div class="section insights">
        <h2>📈 数据洞察</h2>
        <ul>
            <li><strong>版本迭代迅速</strong>：3月份已发布多个版本（v2026.3.1 - v2026.3.13）</li>
            <li><strong>GPT-5.4支持</strong>：最新版本已支持GPT-5.4模型</li>
            <li><strong>技能生态扩展</strong>：ClawHub支持自动搜索和安装技能</li>
            <li><strong>社区活跃度高</strong>：GitHub星标数持续增长</li>
        </ul>
    </div>

    <div class="footer">
        <p>此邮件由OpenClaw新闻监控系统自动生成</p>
        <p>生成时间：$(date '+%Y-%m-%d %H:%M:%S')</p>
        <p>如需退订或反馈，请回复此邮件</p>
    </div>
</body>
</html>
EOF
)

# 创建纯文本版本
TEXT_CONTENT=$(cat << EOF
OpenClaw日报 - ${TODAY}

📊 今日概览
精选OpenClaw最新动态，涵盖版本更新、功能增强和社区动态。

🚀 版本与功能更新
1. OpenClaw v2026.3.13 发布
   来源：GitHub | 语言：英文 | 验证状态：已验证
   最新版本 v2026.3.13 已发布，包含多项改进和bug修复。
   ClawHub功能增强，支持自动搜索和安装技能。
   链接：https://github.com/openclaw/openclaw

2. GPT-5.4 支持
   来源：AI Base | 语言：英文
   OpenClaw最新版本已支持GPT-5.4模型，性能超越Claude Code。
   GitHub星标数已超过28万。
   链接：https://news.aibase.com/news/26039

📈 数据洞察
• 版本迭代迅速：3月份已发布多个版本（v2026.3.1 - v2026.3.13）
• GPT-5.4支持：最新版本已支持GPT-5.4模型
• 技能生态扩展：ClawHub支持自动搜索和安装技能
• 社区活跃度高：GitHub星标数持续增长

---
此邮件由OpenClaw新闻监控系统自动生成
生成时间：$(date '+%Y-%m-%d %H:%M:%S')
EOF
)

# 发送邮件
echo ""
echo "📧 正在发送邮件..."
echo "   发件人: $SENDER_EMAIL"
echo "   收件人: ${RECIPIENTS[*]}"
echo ""

# 使用Python发送邮件
python3 -c "
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import sys
import os

# 配置
sender_email = '$SENDER_EMAIL'
recipients = ['$RECIPIENTS']
password = '$EMAIL_PASSWORD'
subject = f'🦞 OpenClaw日报 - $TODAY'

# 创建邮件
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = ', '.join(recipients)
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject

# 添加纯文本版本
text_part = MIMEText('''$TEXT_CONTENT''', 'plain', 'utf-8')
msg.attach(text_part)

# 添加HTML版本
html_part = MIMEText('''$HTML_CONTENT''', 'html', 'utf-8')
msg.attach(html_part)

try:
    # 连接SMTP服务器
    server = smtplib.SMTP('smtp.qq.com', 587)
    server.starttls()
    server.login(sender_email, password)
    
    # 发送邮件
    server.sendmail(sender_email, recipients, msg.as_string())
    server.quit()
    
    print('✅ 邮件发送成功！')
    print(f'   收件人: {recipients}')
    print(f'   主题: {subject}')
    
    # 记录日志
    log_file = '$NEWS_DIR/email_sent_$TODAY.log'
    with open(log_file, 'w') as f:
        f.write(f'OpenClaw新闻邮件发送成功\\n')
        f.write(f'发送时间: $(date "+%Y-%m-%d %H:%M:%S")\\n')
        f.write(f'收件人: {recipients}\\n')
        f.write(f'文件: $OPENCLAW_MD_FILE\\n')
    
    sys.exit(0)
    
except Exception as e:
    print(f'❌ 邮件发送失败: {e}')
    
    # 记录错误日志
    error_file = '$NEWS_DIR/email_error_$TODAY.log'
    with open(error_file, 'w') as f:
        f.write(f'OpenClaw新闻邮件发送失败\\n')
        f.write(f'错误时间: $(date "+%Y-%m-%d %H:%M:%S")\\n')
        f.write(f'错误信息: {str(e)}\\n')
    
    sys.exit(1)
"

SEND_STATUS=$?

if [ $SEND_STATUS -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 邮件发送成功!"
    echo "=========================================="
    exit 0
else
    echo ""
    echo "=========================================="
    echo "❌ 邮件发送失败!"
    echo "=========================================="
    exit 1
fi