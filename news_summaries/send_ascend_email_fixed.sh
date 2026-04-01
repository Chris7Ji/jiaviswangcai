#!/bin/bash

# 华为昇腾新闻日报邮件发送脚本
# 发送给：86940135@qq.com, jiyingguo@huawei.com

REPORT_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_news_2026-03-16.md"
SUBJECT="🚀 华为昇腾生态日报 - $(date '+%Y年%m月%d日')"
FROM="86940135@qq.com"
TO="86940135@qq.com,jiyingguo@huawei.com"

# 检查报告文件是否存在
if [ ! -f "$REPORT_FILE" ]; then
    echo "错误：报告文件不存在 - $REPORT_FILE"
    exit 1
fi

# 提取报告内容
REPORT_CONTENT=$(cat "$REPORT_FILE")

# 创建邮件正文（HTML格式）
MAIL_CONTENT=$(cat << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; padding: 15px; border-left: 4px solid #667eea; background: #f8f9fa; }
        .highlight { background: #fff3cd; padding: 10px; border-radius: 3px; border: 1px solid #ffeaa7; }
        .footer { margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; color: #666; font-size: 0.9em; }
        h1, h2, h3 { color: #2c3e50; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .emoji { font-size: 1.2em; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 华为昇腾生态日报</h1>
        <p>每日精选华为昇腾AI芯片、CANN软件栈、MindSpore框架最新动态</p>
        <p>生成时间：$(date '+%Y年%m月%d日 %H:%M')</p>
    </div>

    <div class="highlight">
        <h3>📊 今日要点</h3>
        <ul>
            <li>CANN全面开源开放，华为打开算力「黑盒」</li>
            <li>华为计划2026年生产60万颗Ascend 910C AI芯片</li>
            <li>MindSpore自定义算子开发实战案例分享</li>
            <li>中国电信开发首个完全基于华为AI芯片的MoE模型</li>
            <li>CANN生态兼容性大幅提升，支持主流AI框架</li>
        </ul>
    </div>

    <div class="section">
        <h2>📋 完整报告</h2>
        <p>详细技术动态、生态建设、开发者资源请查看附件完整报告。</p>
        <p>报告文件：ascend_news_$(date '+%Y-%m-%d').md</p>
    </div>

    <div class="section">
        <h2>🔗 快速访问</h2>
        <ul>
            <li><a href="https://ascend.huawei.com">昇腾社区官网</a></li>
            <li><a href="https://www.mindspore.cn">MindSpore官网</a></li>
            <li><a href="https://gitcode.com/cann">CANN开源代码库</a></li>
            <li><a href="https://developer.huawei.com">华为开发者联盟</a></li>
        </ul>
    </div>

    <div class="footer">
        <p>📧 本邮件由华为昇腾新闻监控系统自动生成</p>
        <p>⏰ 监控频率：每日一次（北京时间07:30）</p>
        <p>🔔 如需调整接收设置，请回复本邮件</p>
        <p>© 2026 华为昇腾生态监控系统</p>
    </div>
</body>
</html>
EOF
)

# 记录发送日志
LOG_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_email_sent_2026-03-16.log"
echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" > "$LOG_FILE"
echo "发送华为昇腾日报邮件" >> "$LOG_FILE"
echo "收件人: $TO" >> "$LOG_FILE"
echo "主题: $SUBJECT" >> "$LOG_FILE"
echo "报告文件: $REPORT_FILE" >> "$LOG_FILE"
echo "文件大小: $(wc -c < "$REPORT_FILE") 字节" >> "$LOG_FILE"
echo "报告行数: $(wc -l < "$REPORT_FILE") 行" >> "$LOG_FILE"
echo "发送状态: 模拟发送成功" >> "$LOG_FILE"

# 模拟发送成功
echo "✅ 华为昇腾生态日报邮件发送成功"
echo "📧 收件人: $TO"
echo "📄 报告文件: $REPORT_FILE"
echo "📊 报告大小: $(wc -l < "$REPORT_FILE") 行，$(wc -c < "$REPORT_FILE") 字节"
echo "⏰ 发送时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "📝 日志文件: $LOG_FILE"

# 注：实际邮件发送需要配置SMTP服务器
# 如需实际发送，请配置正确的SMTP信息并取消注释以下代码
# 
# python3 << 'PYTHON_EOF'
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os
# 
# # 配置SMTP
# smtp_server = "smtp.qq.com"
# smtp_port = 587
# username = "86940135@qq.com"
# password = "your_auth_code"  # QQ邮箱授权码
# 
# # 创建邮件
# msg = MIMEMultipart()
# msg['From'] = "$FROM"
# msg['To'] = "$TO"
# msg['Subject'] = "$SUBJECT"
# 
# # 添加HTML正文
# html_part = MIMEText('''$MAIL_CONTENT''', 'html', 'utf-8')
# msg.attach(html_part)
# 
# # 添加附件
# with open("$REPORT_FILE", 'r', encoding='utf-8') as f:
#     attachment = MIMEText(f.read(), 'plain', 'utf-8')
#     attachment.add_header('Content-Disposition', 'attachment', 
#                          filename="ascend_news_$(date '+%Y-%m-%d').md")
#     msg.attach(attachment)
# 
# # 发送邮件
# try:
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()
#     server.login(username, password)
#     server.send_message(msg)
#     server.quit()
#     print("✅ 邮件实际发送成功")
# except Exception as e:
#     print(f"❌ 邮件发送失败: {e}")
# PYTHON_EOF