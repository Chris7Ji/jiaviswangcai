import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件配置
smtp_server = "smtp.qq.com"
smtp_port = 587
sender_email = "86940135@qq.com"
sender_password = "icxhfzuyzbhbbjie"

# 收件人列表
recipients = [
    "qinhongyi2@huawei.com",
    "tiankunyang@huawei.com", 
    "jiawei18@huawei.com",
    "jiyingguo@huawei.com",
    "linfeng67@huawei.com",
    "liuwei44259@huawei.com",
    "lvluling1@huawei.com",
    "suqi1@huawei.com",
    "susha@huawei.com",
    "wangdongxiao@huawei.com",
    "xiongguifang@huawei.com",
    "xushengsheng@huawei.com",
    "zhangqianfeng2@huawei.com",
    "zhangyexing2@huawei.com"
]

# 读取HTML内容
with open('/Users/jiyingguo/.openclaw/workspace/test_email_20260318_v2.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 创建邮件
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = ", ".join(recipients)
msg['Subject'] = "🚀 [03月18日] 高校分队 AI 新闻每日简报：OpenAI战略调整聚焦核心业务"

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
    print(f"📧 收件人: {len(recipients)}人")
    print("📊 新闻数量: 20条")
    print("🧪 测试版本")
except Exception as e:
    print(f"❌ 发送失败: {e}")