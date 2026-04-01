#!/bin/bash

# AI新闻日报邮件发送脚本
# 发送日期：2026年3月18日

echo "开始发送AI新闻日报邮件..."

# 读取新闻摘要内容
NEWS_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-18.md"
if [ ! -f "$NEWS_FILE" ]; then
    echo "错误：新闻文件不存在"
    exit 1
fi

# 提取新闻标题和概览
TITLE=$(grep "^# " "$NEWS_FILE" | head -1 | sed 's/# //')
OVERVIEW=$(awk '/今日概览/,/---/' "$NEWS_FILE" | head -10)

# 构建邮件内容
SUBJECT="🤖 AI新闻日报 - 2026年3月18日"
BODY="您好，

这是今天的AI新闻日报摘要：

$TITLE

$OVERVIEW

详细内容请查看附件中的完整报告。

今日精选新闻：
1. 月之暗面Kimi发布《Attention Residuals》技术报告，马斯克评价'令人印象深刻'
2. Yann LeCun的AMI Labs融资10.3亿美元构建世界模型
3. 十年人机共生：围棋AI从对弈到教学测评已融入日常
4. Qwen团队发布Qwen 3.5开源模型
5. Grammarly的'专家评审'功能引发AI伦理争议

祝好！
AI新闻监控系统

报告生成时间：$(date '+%Y-%m-%d %H:%M')"

echo "邮件内容准备完成"
echo "主题：$SUBJECT"
echo ""
echo "邮件正文："
echo "$BODY"
echo ""

# 使用Python发送邮件
echo "正在发送邮件..."
python3 << 'EOF'
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

# 邮件配置
sender_email = "86940135@qq.com"
receiver_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
password = "icxhfzuyzbhbbjie"  # QQ邮箱授权码

# 邮件内容
subject = "🤖 AI新闻日报 - 2026年3月18日"
body = """您好，

这是今天的AI新闻日报摘要：

🤖 AI新闻日报 - 2026年3月18日

📊 今日概览
- 精选新闻：8条（中文4条，英文4条）
- 覆盖领域：大模型架构突破、AI融资、围棋AI发展、AI写作工具伦理
- 质量评级：⭐⭐⭐⭐

今日精选新闻：
1. 月之暗面Kimi发布《Attention Residuals》技术报告，马斯克评价'令人印象深刻'
2. Yann LeCun的AMI Labs融资10.3亿美元构建世界模型
3. 十年人机共生：围棋AI从对弈到教学测评已融入日常
4. Qwen团队发布Qwen 3.5开源模型
5. Grammarly的'专家评审'功能引发AI伦理争议

详细内容请查看附件中的完整报告。

祝好！
AI新闻监控系统

报告生成时间：""" + datetime.now().strftime("%Y-%m-%d %H:%M")

# 创建邮件
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ", ".join(receiver_emails)
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain', 'utf-8'))

# 添加附件
news_file = "/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-18.md"
if os.path.exists(news_file):
    with open(news_file, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="ai_news_2026-03-18.md"')
        msg.attach(part)

# 发送邮件
try:
    server = smtplib.SMTP('smtp.qq.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()
    print("✅ 邮件发送成功！")
    print(f"收件人：{receiver_emails}")
except Exception as e:
    print(f"❌ 邮件发送失败：{e}")
EOF

echo "任务执行完成"