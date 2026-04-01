#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime

def create_email_content():
    """创建邮件内容但不实际发送"""
    
    # 读取文件内容
    today = datetime.now().strftime("%Y-%m-%d")
    markdown_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{today}.md"
    html_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{today}.html"
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 邮件配置
    sender_email = "86940135@qq.com"
    receiver_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 创建邮件内容文件
    email_content_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/email_ready_{today}.txt"
    
    email_content = f"""邮件配置信息：
发件人：{sender_email}
收件人：{', '.join(receiver_emails)}
主题：AI新闻每日摘要 - {datetime.now().strftime('%Y年%m月%d日')}

邮件内容已准备好，但由于缺少QQ邮箱授权码，无法自动发送。
请手动登录QQ邮箱发送，或设置QQ_EMAIL_PASSWORD环境变量。

邮件内容摘要：
{markdown_content[:500]}...

完整内容已保存至：
Markdown格式：{markdown_file}
HTML格式：{html_file}

要手动发送邮件，请：
1. 登录QQ邮箱 (86940135@qq.com)
2. 新建邮件
3. 收件人填写：86940135@qq.com, jiyingguo@huawei.com
4. 主题：AI新闻每日摘要 - {datetime.now().strftime('%Y年%m月%d日')}
5. 将HTML文件内容复制为邮件正文（HTML格式）
6. 发送
"""
    
    with open(email_content_file, 'w', encoding='utf-8') as f:
        f.write(email_content)
    
    print("邮件内容已准备就绪！")
    print(f"邮件配置已保存至：{email_content_file}")
    print(f"HTML内容文件：{html_file}")
    print(f"Markdown内容文件：{markdown_file}")
    print("\n由于缺少QQ邮箱授权码，需要手动发送邮件。")
    print("请按照上述说明操作。")
    
    return True

if __name__ == "__main__":
    create_email_content()