#!/usr/bin/env python3
"""
搜索会议相关邮件的脚本
需要根据你的邮件客户端配置进行调整
"""

import os
import re
from datetime import datetime, timedelta

def search_local_mail(keywords):
    """
    搜索本地邮件文件中的关键词
    这只是一个示例，需要根据你的实际邮件存储位置调整
    """
    # 常见的邮件存储位置
    mail_dirs = [
        "~/Library/Mail",  # macOS Mail
        "~/Library/Thunderbird/Profiles",  # Thunderbird
        "~/.mutt",  # Mutt
        "~/Mail",  # 通用邮件目录
    ]
    
    results = []
    
    for mail_dir in mail_dirs:
        expanded_dir = os.path.expanduser(mail_dir)
        if os.path.exists(expanded_dir):
            print(f"📁 检查邮件目录: {expanded_dir}")
            
            # 这里可以添加实际的邮件搜索逻辑
            # 例如：遍历.eml文件，解析邮件内容等
            
    return results

def get_tomorrow_date():
    """获取明天的日期"""
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")

def main():
    """主函数"""
    print("=" * 50)
    print("会议邮件搜索工具")
    print("=" * 50)
    
    tomorrow = get_tomorrow_date()
    print(f"📅 明天日期: {tomorrow}")
    
    # 常见的会议关键词
    keywords = [
        "meeting", "会议", "call", "zoom", "teams",
        "agenda", "议程", "schedule", "日程",
        "invitation", "邀请", "calendar", "日历"
    ]
    
    print(f"🔍 搜索关键词: {', '.join(keywords)}")
    
    print("\n📋 建议的搜索方法:")
    print("1. 在邮件客户端中搜索以下关键词:")
    for keyword in keywords:
        print(f"   - {keyword}")
    
    print("\n2. 搜索包含日期的邮件:")
    print(f"   - 日期: {tomorrow}")
    print(f"   - 日期格式: {tomorrow.replace('-', '/')}")
    
    print("\n3. 常见的会议邮件特征:")
    print("   - 主题包含: Meeting, 会议, Invitation, 邀请")
    print("   - 包含: Zoom链接, Teams链接, 会议ID")
    print("   - 包含: 议程, 时间, 地点")
    
    print("\n💡 提示:")
    print("- 如果你使用QQ邮箱，可以在网页版或手机APP中搜索")
    print("- 如果你使用华为邮箱，同样可以在相应客户端中搜索")
    print("- 如果你有重要的会议，通常会有相关的邮件往来")

if __name__ == "__main__":
    main()