#!/usr/bin/env python3
"""
邮件搜索助手
提供多种邮件搜索方案
"""

import sys
from datetime import datetime, timedelta

def print_search_instructions():
    """打印搜索说明"""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    print("=" * 60)
    print("📧 邮件搜索助手 - 会议背景信息查找")
    print("=" * 60)
    
    print(f"\n📅 明天日期: {tomorrow}")
    
    print("\n🔍 推荐搜索策略:")
    print("1. 首先搜索会议邀请邮件")
    print("2. 然后搜索相关主题的邮件往来")
    print("3. 最后搜索相关的文档和资料")
    
    print("\n📋 具体搜索关键词组合:")
    
    print("\nA. 基础搜索（在邮件客户端中执行）:")
    print(f"   1. 日期搜索: \"{tomorrow}\" OR \"{tomorrow.replace('-', '/')}\"")
    print("   2. 会议关键词: meeting OR 会议 OR 例会")
    print("   3. 邀请关键词: invitation OR 邀请 OR 请参加")
    
    print("\nB. 高级搜索组合:")
    print("   1. 明天 + 会议: ")
    print(f"      \"{tomorrow} meeting\" OR \"{tomorrow} 会议\"")
    print("   2. 会议 + 特定时间:")
    print("      \"9:00 meeting\" OR \"10:00 会议\"")
    print("   3. 会议平台:")
    print("      \"Zoom\" OR \"Teams\" OR \"腾讯会议\"")
    
    print("\nC. 背景信息搜索:")
    print("   1. 项目/产品名称（如果你知道会议主题）")
    print("   2. 相关人员姓名")
    print("   3. 相关文档名称")
    
    print("\n📱 不同邮件客户端的搜索方法:")
    
    print("\n1. QQ邮箱:")
    print("   - 网页版: 登录 mail.qq.com → 点击搜索框")
    print("   - 手机APP: 打开APP → 点击顶部搜索图标")
    print("   - 支持高级搜索语法: from:发件人 subject:主题")
    
    print("\n2. 华为邮箱:")
    print("   - 网页版: 登录 mail.huawei.com")
    print("   - 手机APP: 打开华为邮箱APP")
    print("   - 同样支持高级搜索语法")
    
    print("\n3. Gmail:")
    print("   - 网页版: mail.google.com")
    print("   - 支持强大的搜索运算符:")
    print("     after:2026/02/28 before:2026/03/02")
    print("     has:attachment")
    print("     filename:pdf")
    
    print("\n💡 实用技巧:")
    print("1. 按时间排序: 找到邮件后，按时间倒序排列")
    print("2. 查看附件: 会议相关邮件常有议程、PPT等附件")
    print("3. 查看完整会话: 有些客户端支持查看完整邮件往来")
    print("4. 搜索相关人: 找到组织者后，搜索与TA的所有邮件")
    
    print("\n🔄 如果找不到会议邮件:")
    print("1. 检查垃圾邮件文件夹")
    print("2. 检查日历应用中的会议详情")
    print("3. 查看团队协作工具（如飞书、钉钉、Slack）")
    print("4. 直接询问会议组织者")
    
    print("\n🤖 我可以帮你:")
    print("1. 如果你提供会议关键词，我可以生成更具体的搜索建议")
    print("2. 如果你提供邮箱配置，我可以尝试编写自动搜索脚本")
    print("3. 如果你找到相关邮件，我可以帮你分析和总结")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 如果有特定会议主题，提供定制化建议
        meeting_topic = " ".join(sys.argv[1:])
        print(f"\n🎯 针对会议主题: {meeting_topic}")
        print(f"\n🔍 定制搜索建议:")
        print(f"   1. \"{meeting_topic} meeting\"")
        print(f"   2. \"{meeting_topic} 会议\"")
        print(f"   3. \"{meeting_topic} agenda\"")
        print(f"   4. \"{meeting_topic} 讨论\"")
        print(f"   5. \"{meeting_topic} 资料\"")
    
    print_search_instructions()

if __name__ == "__main__":
    main()