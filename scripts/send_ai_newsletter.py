#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高校分队AI新闻简报邮件发送脚本

功能：
- 使用QQ邮箱SMTP发送HTML格式邮件
- 支持命令行参数指定HTML文件路径
- 包含详细的日志记录功能
- 错误重试机制（失败时重试3次）

使用方法：
    python send_ai_newsletter.py --html /path/to/newsletter.html
    python send_ai_newsletter.py --html /path/to/newsletter.html --subject "自定义主题"
"""

import argparse
import logging
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional

# ==================== 配置信息 ====================
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SENDER_EMAIL = "86940135@qq.com"
SENDER_PASSWORD = "icxhfzuyzbhbbjie"  # QQ邮箱授权码

# 收件人列表
RECIPIENTS = [
    "jiyingguo@huawei.com",
    "xushengsheng@huawei.com",
    "86940135@qq.com"
]

DEFAULT_SUBJECT = "高校分队-AI新闻每日简报"
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 5  # 重试间隔（秒）

# ==================== 日志配置 ====================
def setup_logging() -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("AINewsletter")
    logger.setLevel(logging.DEBUG)
    
    # 清除已有的处理器
    logger.handlers = []
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # 文件处理器
    log_file = Path(__file__).parent / "send_ai_newsletter.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    logger.info(f"日志文件位置: {log_file}")
    return logger

# ==================== 邮件发送类 ====================
class NewsletterSender:
    """AI新闻简报邮件发送器"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
        self.recipients = RECIPIENTS
        self.max_retries = MAX_RETRIES
        self.retry_delay = RETRY_DELAY
    
    def read_html_content(self, html_path: str) -> str:
        """
        读取HTML文件内容
        
        Args:
            html_path: HTML文件路径
            
        Returns:
            HTML内容字符串
            
        Raises:
            FileNotFoundError: 文件不存在
            IOError: 读取文件失败
        """
        self.logger.info(f"正在读取HTML文件: {html_path}")
        
        path = Path(html_path)
        if not path.exists():
            self.logger.error(f"HTML文件不存在: {html_path}")
            raise FileNotFoundError(f"HTML文件不存在: {html_path}")
        
        if not path.is_file():
            self.logger.error(f"路径不是文件: {html_path}")
            raise ValueError(f"路径不是文件: {html_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.info(f"成功读取HTML文件，大小: {len(content)} 字符")
            return content
        except UnicodeDecodeError:
            self.logger.warning("UTF-8解码失败，尝试使用GBK编码")
            try:
                with open(path, 'r', encoding='gbk') as f:
                    content = f.read()
                self.logger.info(f"成功读取HTML文件（GBK编码），大小: {len(content)} 字符")
                return content
            except Exception as e:
                self.logger.error(f"读取HTML文件失败: {e}")
                raise IOError(f"读取HTML文件失败: {e}")
        except Exception as e:
            self.logger.error(f"读取HTML文件失败: {e}")
            raise IOError(f"读取HTML文件失败: {e}")
    
    def create_email_message(self, html_content: str, subject: str) -> MIMEMultipart:
        """
        创建邮件消息
        
        Args:
            html_content: HTML内容
            subject: 邮件主题
            
        Returns:
            MIMEMultipart邮件对象
        """
        self.logger.info(f"创建邮件消息，主题: {subject}")
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = ', '.join(self.recipients)
        
        # 添加纯文本版本（作为后备）
        text_content = "这是一封HTML格式的邮件，请使用支持HTML的邮件客户端查看。"
        msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
        
        # 添加HTML版本
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        self.logger.debug("邮件消息创建完成")
        return msg
    
    def send_email(self, html_content: str, subject: str) -> bool:
        """
        发送邮件（带重试机制）
        
        Args:
            html_content: HTML内容
            subject: 邮件主题
            
        Returns:
            发送成功返回True，否则返回False
        """
        self.logger.info(f"开始发送邮件，收件人: {', '.join(self.recipients)}")
        self.logger.info(f"⚠️ 注意：使用QQ邮箱({self.sender_email})发送邮件到华为邮箱可能被拦截")
        self.logger.info(f"⚠️ 建议：华为邮箱用户检查垃圾邮件文件夹或联系IT部门")
        
        msg = self.create_email_message(html_content, subject)
        
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"第 {attempt}/{self.max_retries} 次尝试发送...")
                
                # 连接SMTP服务器
                self.logger.debug(f"连接SMTP服务器: {self.smtp_server}:{self.smtp_port}")
                with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                    server.set_debuglevel(1)  # 设置为1可查看详细调试信息
                    
                    # 启动TLS加密
                    self.logger.debug("启动TLS加密...")
                    server.starttls()
                    
                    # 登录
                    self.logger.debug(f"登录邮箱: {self.sender_email}")
                    server.login(self.sender_email, self.sender_password)
                    
                    # 发送邮件 - 分别发送给每个收件人以获取详细的投递状态
                    self.logger.debug("发送邮件...")
                    failed_recipients = server.sendmail(
                        self.sender_email,
                        self.recipients,
                        msg.as_string()
                    )
                    
                    if failed_recipients:
                        self.logger.error(f"❌ 以下收件人投递失败: {failed_recipients}")
                    else:
                        self.logger.info(f"✅ SMTP服务器接受所有收件人地址")
                
                self.logger.info(f"✅ 邮件已提交到SMTP服务器！共 {len(self.recipients)} 位收件人")
                self.logger.info(f"⚠️ 注意：SMTP接受不代表收件人实际收到，可能被垃圾邮件过滤")
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                self.logger.error(f"❌ 邮箱认证失败: {e}")
                self.logger.error("请检查邮箱地址和授权码是否正确")
                return False
                
            except smtplib.SMTPConnectError as e:
                self.logger.error(f"❌ SMTP连接失败: {e}")
                
            except smtplib.SMTPRecipientsRefused as e:
                self.logger.error(f"❌ 收件人地址被拒绝: {e}")
                return False
                
            except smtplib.SMTPSenderRefused as e:
                self.logger.error(f"❌ 发件人地址被拒绝: {e}")
                return False
                
            except smtplib.SMTPException as e:
                self.logger.error(f"❌ SMTP错误: {e}")
                
            except TimeoutError as e:
                self.logger.error(f"❌ 连接超时: {e}")
                
            except Exception as e:
                self.logger.error(f"❌ 发送邮件时发生未知错误: {type(e).__name__}: {e}")
            
            # 如果不是最后一次尝试，则等待后重试
            if attempt < self.max_retries:
                self.logger.info(f"{self.retry_delay}秒后重试...")
                time.sleep(self.retry_delay)
        
        self.logger.error(f"❌ 邮件发送失败，已重试 {self.max_retries} 次")
        return False
    
    def send_newsletter(self, html_path: str, subject: Optional[str] = None) -> bool:
        """
        发送新闻简报的主函数
        
        Args:
            html_path: HTML文件路径
            subject: 邮件主题（可选，默认使用DEFAULT_SUBJECT）
            
        Returns:
            发送成功返回True，否则返回False
        """
        subject = subject or DEFAULT_SUBJECT
        
        try:
            # 读取HTML内容
            html_content = self.read_html_content(html_path)
            
            # 发送邮件
            return self.send_email(html_content, subject)
            
        except FileNotFoundError as e:
            self.logger.error(f"❌ {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ 发送简报时发生错误: {e}")
            return False


# ==================== 命令行参数解析 ====================
def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="高校分队AI新闻简报邮件发送脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python send_ai_newsletter.py --html newsletter.html
  python send_ai_newsletter.py --html newsletter.html --subject "本周AI新闻简报"
        """
    )
    
    parser.add_argument(
        '--html', '-f',
        required=True,
        help='HTML文件路径（必需）'
    )
    
    parser.add_argument(
        '--subject', '-s',
        default=DEFAULT_SUBJECT,
        help=f'邮件主题（默认: "{DEFAULT_SUBJECT}"）'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    return parser.parse_args()


# ==================== 主函数 ====================
def main() -> int:
    """
    主函数
    
    Returns:
        0: 成功
        1: 失败
    """
    # 设置日志
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("高校分队AI新闻简报邮件发送脚本启动")
    logger.info("=" * 50)
    
    # 解析命令行参数
    args = parse_arguments()
    
    logger.info(f"HTML文件: {args.html}")
    logger.info(f"邮件主题: {args.subject}")
    
    # 创建发送器并发送邮件
    sender = NewsletterSender(logger)
    success = sender.send_newsletter(args.html, args.subject)
    
    if success:
        logger.info("=" * 50)
        logger.info("✅ 任务完成！")
        logger.info("=" * 50)
        return 0
    else:
        logger.error("=" * 50)
        logger.error("❌ 任务失败！")
        logger.error("=" * 50)
        return 1


if __name__ == "__main__":
    sys.exit(main())
