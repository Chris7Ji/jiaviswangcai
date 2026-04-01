#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 配置
smtp_server = "smtp.qq.com"
smtp_port = 465
sender_email = "86940135@qq.com"
password = "swqfjvmoupdebhgh"
receivers = ["86940135@qq.com", "jiyingguo@huawei.com"]

# 链接
link = "https://cloud.tencent.com/developer/article/2626160"

# 创建邮件
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ", ".join(receivers)
msg['Subject'] = f"链接分享 - {datetime.now().strftime('%Y年%m月%d日 %H:%M')}"

# 邮件正文
body = f"""
尊敬的Boss，

您好！

以下是您要求分享的链接：

{link}

请查收！

祝好！
Jarvis AI助手
{datetime.now().strftime('%Y年%m月%d日 %H:%M')}
"""

msg.attach(MIMEText(body, 'plain', 'utf-8'))

# 发送邮件
try:
    print("正在连接SMTP服务器...")
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
    print("正在登录...")
    server.login(sender_email, password)
    print("正在发送邮件...")
    server.sendmail(sender_email, receivers, msg.as_string())
    server.quit()
    print("✅ 邮件发送成功！")
    print(f"收件人: {', '.join(receivers)}")
    print(f"链接: {link}")
except Exception as e:
    print(f"❌ 发送失败: {e}")
