#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

# 配置
smtp_server = "smtp.qq.com"
smtp_port = 465
sender_email = "86940135@qq.com"
password = "swqfjvmoupdebhgh"  # 新授权码
receivers = ["86940135@qq.com", "jiyingguo@huawei.com"]

# 创建邮件
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ", ".join(receivers)
msg['Subject'] = f"Mac mini + 飞书 + Deepseek 部署指导书 - {datetime.now().strftime('%Y年%m月%d日')}"

# 邮件正文
body = """
尊敬的Boss，

您好！

根据您的要求，我已经搜索了全网最新资料，整理了一份详细的《Mac mini + 飞书 + Deepseek Chat 大模型部署对接指导书》。

文档内容包括：
✅ 项目概述与系统架构
✅ 硬件与系统要求（含性能参考）
✅ 完整的环境准备步骤
✅ Ollama与Deepseek模型部署
✅ 飞书机器人配置详解
✅ 系统集成开发代码
✅ Docker部署与运维
✅ 故障排除指南
✅ 附录（命令速查、资源链接）

文档特点：
- 基于2025年最新技术资料
- 包含详细的命令和配置
- 提供多种部署方案
- 适合从零开始的用户

附件中的Word文档包含了完整的指导内容，请查收。

如有任何问题，请随时联系我。

祝好！
Jarvis AI助手
"""

msg.attach(MIMEText(body, 'plain', 'utf-8'))

# 添加附件
file_path = "/Users/jiyingguo/.openclaw/workspace/Mac_mini_飞书_Deepseek_部署指导书.docx"
with open(file_path, "rb") as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= "Mac_mini_飞书_Deepseek_部署指导书.docx"'
    )
    msg.attach(part)

# 发送邮件
try:
    print("正在连接QQ邮箱SMTP服务器...")
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
    print("正在登录...")
    server.login(sender_email, password)
    print("正在发送邮件...")
    server.sendmail(sender_email, receivers, msg.as_string())
    server.quit()
    print("✅ 邮件发送成功！")
    print(f"收件人: {', '.join(receivers)}")
except Exception as e:
    print(f"❌ 发送失败: {e}")
