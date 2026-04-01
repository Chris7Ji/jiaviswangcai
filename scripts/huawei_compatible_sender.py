#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为邮箱兼容的AI新闻简报发送脚本

特点：
1. 华为邮箱兼容格式（无emoji，简洁样式）
2. 支持华为邮箱SMTP（如需要）
3. 详细的发送状态报告
4. 错误处理和重试机制

使用方法：
    python huawei_compatible_sender.py --html /path/to/newsletter.html
    python huawei_compatible_sender.py --html /path/to/newsletter.html --subject "自定义主题"
"""

import argparse
import logging
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional, Dict, Tuple

# ==================== 配置信息 ====================
# 默认使用QQ邮箱SMTP（华为邮箱需要特殊配置）
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SENDER_EMAIL = "86940135@qq.com"
SENDER_PASSWORD = "icxhfzuyzbhbbjie"  # QQ邮箱授权码

# 华为邮箱SMTP配置（如需要）
HUAWEI_SMTP_SERVER = "smtp.huawei.com"
HUAWEI_SMTP_PORT = 587

# 收件人列表（高校分队-AI新闻每日简报）
RECIPIENTS = [
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
    "zhangyexing2@huawei.com",
    "86940135@qq.com"
]

DEFAULT_SUBJECT = "高校分队-AI新闻每日简报"
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 5  # 重试间隔（秒）

# ==================== 日志配置 ====================
def setup_logging() -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("HuaweiCompatibleSender")
    logger.setLevel(logging.DEBUG)
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    # 文件处理器
    log_file = Path.home() / ".openclaw" / "workspace" / "logs" / "huawei_sender.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

# ==================== 华为邮箱兼容处理 ====================
def make_huawei_compatible(html_content: str) -> str:
    """
    将HTML内容转换为华为邮箱兼容格式
    
    华为企业邮箱限制：
    1. 不支持emoji
    2. 对复杂CSS样式有限制
    3. 对某些HTML标签有限制
    """
    # 移除所有emoji
    import re
    
    # 移除emoji和特殊字符
    html_content = re.sub(r'[^\x00-\x7F\u4e00-\u9fff]', '', html_content)
    
    # 简化CSS样式
    html_content = html_content.replace(
        'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);',
        'background: #667eea;'
    )
    
    html_content = html_content.replace(
        'box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);',
        'border: 1px solid #e0e0e0;'
    )
    
    # 移除复杂的CSS动画
    html_content = html_content.replace('transition: all 0.3s ease;', '')
    
    # 确保使用安全的字体
    html_content = html_content.replace(
        'font-family: -apple-system, BlinkMacSystemFont',
        'font-family: Arial, sans-serif'
    )
    
    return html_content

# ==================== 邮件发送函数 ====================
def send_email(
    html_file_path: str,
    subject: str,
    use_huawei_smtp: bool = False,
    huawei_email: Optional[str] = None,
    huawei_password: Optional[str] = None
) -> Tuple[bool, Dict[str, str]]:
    """
    发送邮件到所有收件人
    
    Args:
        html_file_path: HTML文件路径
        subject: 邮件主题
        use_huawei_smtp: 是否使用华为邮箱SMTP
        huawei_email: 华为邮箱地址
        huawei_password: 华为邮箱授权码
    
    Returns:
        (成功状态, {收件人: 状态})
    """
    # 读取HTML内容
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        logger.error(f"读取HTML文件失败: {e}")
        return False, {}
    
    # 华为邮箱兼容处理
    html_content = make_huawei_compatible(html_content)
    
    # 配置SMTP
    if use_huawei_smtp and huawei_email and huawei_password:
        smtp_server = HUAWEI_SMTP_SERVER
        smtp_port = HUAWEI_SMTP_PORT
        sender_email = huawei_email
        sender_password = huawei_password
        logger.info(f"使用华为邮箱SMTP: {huawei_email}")
    else:
        smtp_server = SMTP_SERVER
        smtp_port = SMTP_PORT
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD
        logger.info(f"使用QQ邮箱SMTP: {SENDER_EMAIL}")
    
    # 发送结果跟踪
    results = {}
    
    for recipient in RECIPIENTS:
        success = False
        error_msg = ""
        
        for attempt in range(MAX_RETRIES):
            try:
                # 创建邮件
                msg = MIMEMultipart('alternative')
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                
                # 添加HTML内容
                html_part = MIMEText(html_content, 'html', 'utf-8')
                msg.attach(html_part)
                
                # 连接SMTP服务器并发送
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                
                success = True
                logger.info(f"邮件发送成功: {recipient}")
                break
                
            except smtplib.SMTPAuthenticationError as e:
                error_msg = f"SMTP认证失败: {e}"
                logger.error(f"第{attempt+1}次尝试失败 - {recipient}: {error_msg}")
            except smtplib.SMTPException as e:
                error_msg = f"SMTP错误: {e}"
                logger.error(f"第{attempt+1}次尝试失败 - {recipient}: {error_msg}")
            except Exception as e:
                error_msg = f"未知错误: {e}"
                logger.error(f"第{attempt+1}次尝试失败 - {recipient}: {error_msg}")
            
            # 重试前等待
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
        
        # 记录结果
        if success:
            results[recipient] = "✅ 发送成功"
        else:
            results[recipient] = f"❌ 发送失败: {error_msg}"
    
    # 总体成功状态
    overall_success = all("✅" in status for status in results.values())
    
    return overall_success, results

# ==================== 主函数 ====================
def main():
    parser = argparse.ArgumentParser(description='华为邮箱兼容的AI新闻简报发送脚本')
    parser.add_argument('--html', required=True, help='HTML文件路径')
    parser.add_argument('--subject', help='邮件主题（可选）')
    parser.add_argument('--use-huawei-smtp', action='store_true', help='使用华为邮箱SMTP')
    parser.add_argument('--huawei-email', help='华为邮箱地址')
    parser.add_argument('--huawei-password', help='华为邮箱授权码')
    
    args = parser.parse_args()
    
    # 验证文件存在
    html_path = Path(args.html)
    if not html_path.exists():
        logger.error(f"HTML文件不存在: {args.html}")
        sys.exit(1)
    
    # 设置主题
    subject = args.subject or DEFAULT_SUBJECT
    
    logger.info(f"开始发送邮件: {html_path}")
    logger.info(f"邮件主题: {subject}")
    logger.info(f"收件人: {', '.join(RECIPIENTS)}")
    
    # 发送邮件
    success, results = send_email(
        str(html_path),
        subject,
        args.use_huawei_smtp,
        args.huawei_email,
        args.huawei_password
    )
    
    # 输出结果
    print("\n" + "="*50)
    print("邮件发送结果:")
    print("="*50)
    
    for recipient, status in results.items():
        print(f"{recipient}: {status}")
    
    print("="*50)
    
    if success:
        print("✅ 所有邮件发送成功！")
        logger.info("所有邮件发送成功")
    else:
        print("⚠️ 部分邮件发送失败，请查看日志")
        logger.warning("部分邮件发送失败")
        sys.exit(1)

if __name__ == "__main__":
    main()