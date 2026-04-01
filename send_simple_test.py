import smtplib
from email.mime.text import MIMEText

# 邮件配置
smtp_server = "smtp.qq.com"
smtp_port = 587
sender_email = "86940135@qq.com"
sender_password = "icxhfzuyzbhbbjie"

# 收件人
recipient = "jiyingguo@huawei.com"

# 创建简单文本邮件
subject = "🎯 [03月18日] 高校分队-灯塔学校的每日动态：井贤栋向上海交大捐赠1.3亿元支持AI教育"
body = """高校分队-灯塔学校的每日动态

日期：03月18日

今日重点：
1. 井贤栋向上海交大捐赠1.3亿元支持AI教育
2. 中科大光钟刷新人类计时极限
3. 广东省AI OPC行动方案发布，河套学院纳入核心布局
4. 北邮张平院士团队MWC 2026亮相
5. 中央民族大学暂无异动

详细内容请查看附件或联系管理员。

---
此邮件由OpenClaw自动发送
"""

msg = MIMEText(body, 'plain', 'utf-8')
msg['From'] = sender_email
msg['To'] = recipient
msg['Subject'] = subject

# 发送邮件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, [recipient], msg.as_string())
    server.quit()
    print("✅ 简单文本邮件发送成功！")
    print(f"📧 收件人: {recipient}")
    print(f"📧 主题: {subject}")
except Exception as e:
    print(f"❌ 发送失败: {e}")
    import traceback
    traceback.print_exc()