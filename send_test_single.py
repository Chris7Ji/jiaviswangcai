import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件配置
smtp_server = "smtp.qq.com"
smtp_port = 587
sender_email = "86940135@qq.com"
sender_password = "icxhfzuyzbhbbjie"

# 只发送给老板测试
recipients = ["jiyingguo@huawei.com"]

# 读取HTML内容
with open('/Users/jiyingguo/.openclaw/workspace/dengta_project_daily_v4_20260318.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 创建邮件
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = ", ".join(recipients)
msg['Subject'] = "🎯 [03月18日] 高校分队-灯塔学校的每日动态：井贤栋向上海交大捐赠1.3亿元支持AI教育"

# 添加HTML内容
html_part = MIMEText(html_content, 'html', 'utf-8')
msg.attach(html_part)

# 发送邮件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("✅ 测试邮件发送成功！")
    print(f"📧 收件人: {recipients}")
    print("📧 发送时间: 刚刚")
except Exception as e:
    print(f"❌ 发送失败: {e}")