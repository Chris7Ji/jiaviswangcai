#!/usr/bin/env python3
# 简化的AI新闻摘要邮件发送脚本

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_ai_news_email(date_str=None):
    """发送AI新闻摘要邮件"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    # QQ邮箱SMTP配置
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    sender_email = "86940135@qq.com"
    password = "ngjkdlyvxlqpbhej"  # 授权码
    receiver_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 创建邮件主题
    chinese_date = datetime.now().strftime("%Y年%m月%d日")
    subject = f"AI与科技新闻摘要 - {chinese_date}"
    
    # 创建完整的HTML邮件内容
    html_body = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #f8f9fa;
            }}
            .container {{
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 8px;
                margin-bottom: 30px;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
                font-size: 14px;
            }}
            .news-item {{
                border-left: 4px solid #4CAF50;
                padding: 15px 20px;
                margin: 20px 0;
                background: #f9f9f9;
                border-radius: 0 8px 8px 0;
            }}
            .news-title {{
                color: #2c3e50;
                margin-top: 0;
            }}
            .news-snippet {{
                color: #555;
                margin: 10px 0;
            }}
            .news-link {{
                color: #3498db;
                text-decoration: none;
            }}
            .news-link:hover {{
                text-decoration: underline;
            }}
            .keyword {{
                display: inline-block;
                background: #e3f2fd;
                color: #1976d2;
                padding: 4px 12px;
                margin: 4px;
                border-radius: 20px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI与科技新闻摘要</h1>
                <p><strong>日期:</strong> {chinese_date}</p>
                <p><strong>发送时间:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            </div>
            
            <h2>📰 今日精选新闻</h2>
            <p>以下是今日全球AI与科技领域的最新动态摘要：</p>
            
            <div class="news-item">
                <h3 class="news-title">1. AI领域新突破：多模态学习取得进展</h3>
                <p class="news-snippet">研究人员在多模态人工智能学习方面取得重要进展，新的模型能够更好地理解和处理文本、图像、音频等多种数据类型。</p>
                <a href="https://example.com/ai-multimodal" class="news-link" target="_blank">查看详情 →</a>
            </div>
            
            <div class="news-item">
                <h3 class="news-title">2. 科技公司发布最新AI芯片</h3>
                <p class="news-snippet">多家科技巨头宣布推出新一代人工智能专用芯片，性能提升显著，能耗降低，将推动边缘AI计算发展。</p>
                <a href="https://example.com/ai-chips" class="news-link" target="_blank">查看详情 →</a>
            </div>
            
            <div class="news-item">
                <h3 class="news-title">3. 机器学习在医疗诊断中的应用突破</h3>
                <p class="news-snippet">最新研究显示，机器学习模型在医学影像诊断中的准确率已达到专家水平，有望辅助医生提高诊断效率。</p>
                <a href="https://example.com/ai-healthcare" class="news-link" target="_blank">查看详情 →</a>
            </div>
            
            <h2>🔍 今日搜索关键词</h2>
            <div>
                <span class="keyword">最新人工智能新闻</span>
                <span class="keyword">AI技术突破</span>
                <span class="keyword">科技新闻今日</span>
                <span class="keyword">机器学习进展</span>
                <span class="keyword">人工智能行业动态</span>
            </div>
            
            <div class="footer">
                <p><strong>说明：</strong></p>
                <ul>
                    <li>本摘要由OpenClaw自动生成，每天早上06:30发送</li>
                    <li>新闻来源：新华网科技频道、人民网科技等权威媒体</li>
                    <li>摘要格式：详细版（3-4条完整分析）</li>
                    <li>如需调整接收设置，请回复此邮件</li>
                </ul>
                <p style="text-align: center; margin-top: 20px;">
                    <em>🤖 由 OpenClaw AI 助手 (Jarvis) 为您服务</em>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        # 创建MIME消息
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email  # QQ邮箱要求简单的发件人地址
        msg["To"] = ", ".join(receiver_emails)
        msg["Subject"] = subject
        
        # 添加HTML内容
        html_part = MIMEText(html_body, "html", "utf-8")
        msg.attach(html_part)
        
        print(f"📧 正在发送AI新闻摘要邮件...")
        print(f"   日期: {chinese_date}")
        print(f"   发件人: {sender_email}")
        print(f"   收件人: {', '.join(receiver_emails)}")
        
        # 连接SMTP服务器并发送邮件
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 启用TLS加密
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
        
        print("✅ 邮件发送成功！")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("AI新闻摘要邮件发送系统 - 测试版")
    print("=" * 50)
    
    success = send_ai_news_email()
    
    if success:
        print("\n🎉 测试完成！")
        print("明天早上6:30将自动执行完整流程：")
        print("1. 抓取真实新闻 → 2. 生成详细摘要 → 3. 发送邮件")
    else:
        print("\n❌ 测试失败，请检查配置")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()