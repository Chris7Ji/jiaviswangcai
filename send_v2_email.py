#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

smtp_server = "smtp.qq.com"
smtp_port = 465
sender_email = "86940135@qq.com"
password = "swqfjvmoupdebhgh"
receivers = ["86940135@qq.com", "jiyingguo@huawei.com"]

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ", ".join(receivers)
msg['Subject'] = f"【更新版】Mac mini + 飞书 + Deepseek + OpenClaw 部署指导书 v2.0"

body = """
尊敬的Boss，

您好！

根据您的要求，我已经重新整理了《Mac mini + 飞书 + Deepseek + OpenClaw 部署指导书 v2.0》。

本次主要更新内容：

✅ 1. 使用Deepseek官方API（去掉Ollama本地部署）
   - 直接调用Deepseek云服务
   - 无需下载大模型
   - 响应速度更快

✅ 2. OpenClaw官方命令行一键安装
   - Mac: curl -fsSL https://openclaw.ai/install.sh | bash
   - Windows: irm https://openclaw.ai/install.ps1 | iex
   - Linux: curl -fsSL https://openclaw.ai/install.sh | bash

✅ 3. 去掉Docker容器化
   - 直接机器部署
   - 更轻量、更简单

✅ 4. 去掉Python+FastAPI开发框架
   - 使用OpenClaw内置功能
   - 无需额外开发

✅ 5. 增加飞书配置图文说明
   - 14张配图标注
   - 详细的步骤截图说明
   - 从创建应用到添加机器人的完整流程

✅ 6. 支持多平台
   - Mac系统
   - Windows系统
   - Linux系统

文档特点：
- 极简部署：一条命令完成安装
- 跨平台支持：Mac/Windows/Linux
- 图文并茂：详细的飞书配置配图
- 快速上手：30分钟完成部署

附件中的Word文档包含了完整的更新内容，请查收。

如有任何问题，请随时联系我。

祝好！
Jarvis AI助手
"""

msg.attach(MIMEText(body, 'plain', 'utf-8'))

file_path = "/Users/jiyingguo/.openclaw/workspace/Mac_mini_飞书_Deepseek_OpenClaw_部署指导书_v2.docx"
with open(file_path, "rb") as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= "Mac_mini_飞书_Deepseek_OpenClaw_部署指导书_v2.docx"'
    )
    msg.attach(part)

try:
    print("正在连接SMTP服务器...")
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
    server.login(sender_email, password)
    server.sendmail(sender_email, receivers, msg.as_string())
    server.quit()
    print("✅ 邮件发送成功！")
except Exception as e:
    print(f"❌ 发送失败: {e}")
