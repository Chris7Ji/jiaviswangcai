import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件配置
smtp_server = "smtp.qq.com"
smtp_port = 587
sender_email = "86940135@qq.com"
sender_password = "icxhfzuyzbhbbjie"

# 收件人列表（灯塔项目配置）
recipients = [
    "liuwei44259@huawei.com",
    "tiankunyang@huawei.com",
    "qinhongyi2@huawei.com",
    "jiawei18@huawei.com",
    "jiyingguo@huawei.com",
    "linfeng67@huawei.com",
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
with open('/Users/jiyingguo/.openclaw/workspace/dengta_project_daily_v3_20260319.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 创建邮件
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = ", ".join(recipients)
msg['Subject'] = "🎯 [03月18日] 高校分队灯塔项目每日动态：井贤栋捐赠1.3亿支持AI教育，中科大光钟刷新人类计时极限"

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
    print("✅ 灯塔项目简报V3（修正版）发送成功！")
    print(f"📧 收件人: {len(recipients)}人")
    print("📊 情报模块: 5个")
    print("🎯 重点动态: 河套学院3条 + 中科大6条 + 北邮6条 + 上交大6条 + 民大0条")
    print("⏰ 发送时间: 06:45")
    print("📅 监测周期: 过去3天")
    print("📰 内容范围: 科研动态+学校新闻+人事变动")
    print("🔍 数据来源: 高校官网+官方微信公众号")
    print("✅ 已修正: 日期改为03月18日")
except Exception as e:
    print(f"❌ 发送失败: {e}")