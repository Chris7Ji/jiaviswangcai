#!/usr/bin/env python3
"""
AI新闻每日简报邮件发送脚本
发送日期：2026年3月19日
收件人：jiyingguo@huawei.com, xushengsheng@huawei.com, 86940135@qq.com
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import sys

def send_ai_news_email():
    """发送AI新闻每日简报邮件"""
    
    # 邮件配置
    sender = '86940135@qq.com'
    receivers = ['jiyingguo@huawei.com', 'xushengsheng@huawei.com', '86940135@qq.com']
    
    # QQ邮箱授权码（根据TOOLS.md配置）
    password = 'icxhfzuyzbhbbjie'  # 2026-03-18更新，已全局记录
    
    # 邮件主题
    subject = '[2026-03-19] 高校分队- AI 新闻每日简报'
    
    # 读取HTML内容
    html_file = '/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026_03_19.html'
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {html_file}")
        return False
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return False
    
    # 创建邮件
    message = MIMEMultipart('alternative')
    message['From'] = Header('AI新闻简报系统 <86940135@qq.com>', 'utf-8')
    message['To'] = Header(','.join(receivers), 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    
    # 添加HTML版本
    html_part = MIMEText(html_content, 'html', 'utf-8')
    message.attach(html_part)
    
    # 添加纯文本版本（备用）
    text_content = """
高校分队 AI 新闻每日简报 - 2026年3月19日

主要内容：
1. IBM与NVIDIA扩大合作推进企业AI应用
2. Mistral推出Forge平台帮助企业构建自有AI模型
3. 中国加强对OpenClaw等AI代理的监管
4. NVIDIA CEO预测2026年底AI订单将达1万亿美元
5. 伊朗战争影响全球氦气供应和AI芯片制造
6. Snowflake推出"自主"AI层，不仅回答问题还能执行工作
7. Reco推出针对AI代理盲点的新安全功能
8. 大英百科全书起诉OpenAI侵犯AI训练版权
9. 田纳西州青少年起诉Elon Musk的xAI生成儿童性虐待材料
10. 亚马逊Bedrock、LangSmith和SGLang中的AI漏洞可能导致数据泄露
11. 沙特宣布2026年为"人工智能年"

详细内容请查看HTML版本邮件。
"""
    text_part = MIMEText(text_content, 'plain', 'utf-8')
    message.attach(text_part)
    
    try:
        # 连接SMTP服务器
        smtp_server = 'smtp.qq.com'
        smtp_port = 587
        
        print(f"正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS加密
        server.login(sender, password)
        
        # 发送邮件
        print(f"正在发送邮件到: {', '.join(receivers)}")
        server.sendmail(sender, receivers, message.as_string())
        server.quit()
        
        print("邮件发送成功！")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("SMTP认证失败：请检查邮箱和授权码")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP错误：{e}")
        return False
    except Exception as e:
        print(f"发送邮件时出错：{e}")
        return False

if __name__ == "__main__":
    print("开始发送AI新闻每日简报邮件...")
    success = send_ai_news_email()
    
    if success:
        print("邮件发送任务完成！")
        sys.exit(0)
    else:
        print("邮件发送失败！")
        sys.exit(1)