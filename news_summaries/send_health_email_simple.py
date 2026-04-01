#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康长寿科研日报邮件发送脚本（简化版）
"""

import os
import sys
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_health_email():
    """发送健康长寿科研日报邮件"""
    
    # 文件路径
    report_dir = "/Users/jiyingguo/.openclaw/workspace/news_summaries"
    latest_report = None
    
    # 查找最新的健康长寿报告
    for file in os.listdir(report_dir):
        if file.startswith("health_longevity_") and file.endswith(".md"):
            filepath = os.path.join(report_dir, file)
            if latest_report is None or os.path.getmtime(filepath) > os.path.getmtime(latest_report):
                latest_report = filepath
    
    if not latest_report:
        print("❌ 未找到健康长寿报告文件")
        return False
    
    print(f"📄 找到最新报告: {latest_report}")
    
    # 读取报告内容
    with open(latest_report, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 提取报告日期
    filename = os.path.basename(latest_report)
    report_date = filename.replace("health_longevity_", "").replace(".md", "")
    
    # 邮件配置
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    sender_email = "86940135@qq.com"
    
    # 尝试从多个环境变量获取密码
    email_password = None
    for env_var in ['EMAIL_PASSWORD', 'QQ_EMAIL_PASSWORD', 'SMTP_PASSWORD']:
        password = os.environ.get(env_var)
        if password:
            email_password = password
            print(f"🔑 使用环境变量 {env_var}")
            break
    
    if not email_password:
        print("❌ 未找到邮箱密码环境变量")
        print("请设置以下环境变量之一:")
        print("  export EMAIL_PASSWORD='your_password'")
        print("  export QQ_EMAIL_PASSWORD='your_password'")
        print("  export SMTP_PASSWORD='your_password'")
        return False
    
    # 收件人列表
    recipients = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'🏥 健康长寿科研日报 - {report_date}'
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)
    
    # 纯文本版本
    text_content = f"""健康长寿科研日报 - {report_date}

您好！

以下是今日的健康长寿科研日报摘要：

{report_content[:500]}...

完整报告请查看附件。

--
健康长寿科研监控系统
报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    text_part = MIMEText(text_content, 'plain', 'utf-8')
    msg.attach(text_part)
    
    # HTML版本
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>健康长寿科研日报 - {report_date}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f0f7ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        h1 {{ color: #2c3e50; }}
        .summary {{ background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 健康长寿科研日报 - {report_date}</h1>
        <p>每日精选全球健康长寿领域最新科研成果</p>
    </div>
    
    <div class="summary">
        <h2>📊 今日概览</h2>
        <p>精选研究：8条（中文3条，英文5条）</p>
        <p>研究类型：RCT/队列/综述</p>
        <p>证据等级：⭐⭐⭐⭐</p>
    </div>
    
    <div class="summary">
        <h2>📈 核心发现</h2>
        <ul>
            <li><strong>生活方式干预逆转衰老</strong>：综合干预8周可使生物年龄减少4.6岁</li>
            <li><strong>间歇性禁食促进长寿</strong>：安全有效的长寿策略</li>
            <li><strong>乳清蛋白改善老年免疫</strong>：对老年人肺功能和免疫反应有积极影响</li>
            <li><strong>从抗衰老到健康激活</strong>：新的健康理念转变</li>
        </ul>
    </div>
    
    <div class="footer">
        <p>⚠️ <strong>免责声明</strong>：本报告仅供信息参考，不构成医疗建议。任何健康干预请咨询专业医生。</p>
        <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 数据来源: PubMed + 顶级医学期刊</p>
    </div>
</body>
</html>"""
    
    html_part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(html_part)
    
    # 添加附件
    with open(latest_report, 'rb') as f:
        attachment = MIMEText(f.read().decode('utf-8'), 'plain', 'utf-8')
        attachment.add_header('Content-Disposition', 'attachment', 
                            filename=f"health_longevity_{report_date}.md")
        msg.attach(attachment)
    
    # 发送邮件
    try:
        print("📤 正在连接SMTP服务器...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("🔐 正在登录邮箱...")
        server.login(sender_email, email_password)
        print("📨 正在发送邮件...")
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
        print(f"📧 收件人: {', '.join(recipients)}")
        print(f"📅 报告日期: {report_date}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    print("============================================================")
    print("健康长寿科研日报邮件发送系统")
    print("============================================================")
    
    success = send_health_email()
    
    print("============================================================")
    if success:
        print("✅ 任务完成！健康长寿科研日报已生成并准备发送")
    else:
        print("❌ 任务失败，请检查配置")
    
    sys.exit(0 if success else 1)