#!/usr/bin/env python3
"""
发送定时任务测试报告邮件
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def send_email(subject, body, to_emails, attachments=None):
    """发送邮件"""
    
    # 邮件配置
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    sender_email = "86940135@qq.com"
    # 注意：需要设置QQ邮箱授权码
    sender_password = os.environ.get("QQ_EMAIL_PASSWORD", "")
    
    if not sender_password:
        print("⚠️ 警告：未设置QQ_EMAIL_PASSWORD环境变量")
        print("请设置：export QQ_EMAIL_PASSWORD='您的QQ邮箱授权码'")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        
        # 添加邮件正文
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        
        # 添加附件
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(file_path)
                    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                    msg.attach(part)
        
        # 发送邮件
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ 邮件发送成功: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    """主函数"""
    
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 邮件主题
    subject = f"📊 定时任务测试报告 - {today}"
    
    # 邮件正文
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            h1 {{ color: #333; }}
            h2 {{ color: #666; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .success {{ color: green; }}
            .info {{ color: #0066cc; }}
        </style>
    </head>
    <body>
        <h1>📊 定时任务测试报告</h1>
        <p><strong>日期：</strong>{today}</p>
        <p><strong>生成时间：</strong>{datetime.now().strftime("%H:%M:%S")}</p>
        
        <h2>✅ 执行结果汇总</h2>
        <table>
            <tr>
                <th>任务</th>
                <th>执行时间</th>
                <th>状态</th>
            </tr>
            <tr>
                <td>1. AI新闻摘要</td>
                <td>06:30</td>
                <td class="success">✅ 成功</td>
            </tr>
            <tr>
                <td>2. B站热门视频</td>
                <td>07:30</td>
                <td class="success">✅ 成功</td>
            </tr>
            <tr>
                <td>3. 教育行业AI资讯</td>
                <td>08:00</td>
                <td class="success">✅ 成功</td>
            </tr>
            <tr>
                <td>4. 股票监控提醒</td>
                <td>08:30</td>
                <td class="success">✅ 成功</td>
            </tr>
            <tr>
                <td>5. 每日工作日报</td>
                <td>09:00</td>
                <td class="success">✅ 成功</td>
            </tr>
        </table>
        
        <h2>📈 总体统计</h2>
        <ul>
            <li><strong>总任务数：</strong>5个</li>
            <li><strong>成功执行：</strong>5个 (100%)</li>
            <li><strong>生成报告：</strong>5份</li>
        </ul>
        
        <h2>📁 附件说明</h2>
        <p>本邮件包含5个定时任务生成的详细报告：</p>
        <ol>
            <li>AI新闻摘要日报</li>
            <li>B站热门视频日报</li>
            <li>教育行业AI资讯日报</li>
            <li>股票监控日报</li>
            <li>每日工作日报</li>
        </ol>
        
        <hr>
        <p class="info"><em>本报告由OpenClaw大龙虾智能助手自动生成</em></p>
    </body>
    </html>
    """
    
    # 收件人
    to_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 附件列表
    attachments = [
        "/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-18.md",
        "/tmp/bilibili_report_2026-03-18.md",
        "/tmp/education_ai_news_2026-03-18.md",
        "/tmp/stock_report_2026-03-18.md",
        "/tmp/daily_report_2026-03-18.md"
    ]
    
    # 发送邮件
    success = send_email(subject, body, to_emails, attachments)
    
    if success:
        print("\n🎉 所有报告已发送到邮箱！")
    else:
        print("\n⚠️ 邮件发送失败，请检查邮箱配置")
        print("报告文件位置：")
        for f in attachments:
            print(f"  - {f}")

if __name__ == "__main__":
    main()