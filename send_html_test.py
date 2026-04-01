import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件配置
smtp_server = "smtp.qq.com"
smtp_port = 587
sender_email = "86940135@qq.com"
sender_password = "icxhfzuyzbhbbjie"

# 收件人
recipient = "jiyingguo@huawei.com"

# 简化版HTML
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>高校分队灯塔项目每日动态</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #1e3c72;">🎯 高校分队-灯塔学校的每日动态</h1>
    <p style="color: #666;">日期：03月18日</p>
    
    <h2 style="color: #2c3e50;">🔥 今日最重磅：井贤栋向上海交大捐赠1.3亿元支持AI教育</h2>
    
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
        <h3>🏛️ 深圳河套学院</h3>
        <ul>
            <li>广东省AI OPC行动方案发布，河套学院纳入核心布局</li>
        </ul>
    </div>
    
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
        <h3>🎓 中国科学技术大学</h3>
        <ul>
            <li>光钟刷新人类计时极限，300亿年不差1秒</li>
        </ul>
    </div>
    
    <p style="color: #999; font-size: 12px; margin-top: 30px;">此邮件由OpenClaw自动发送</p>
</body>
</html>"""

# 创建邮件
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = recipient
msg['Subject'] = "🎯 [03月18日] 高校分队-灯塔学校的每日动态：井贤栋向上海交大捐赠1.3亿元支持AI教育"

# 添加HTML内容
html_part = MIMEText(html_content, 'html', 'utf-8')
msg.attach(html_part)

# 发送邮件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, [recipient], msg.as_string())
    server.quit()
    print("✅ 简化版HTML邮件发送成功！")
    print(f"📧 收件人: {recipient}")
except Exception as e:
    print(f"❌ 发送失败: {e}")
    import traceback
    traceback.print_exc()