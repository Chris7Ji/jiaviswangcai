#!/usr/bin/env python3
"""
QQ邮箱和Gmail邮箱会议搜索工具
"""

import sys
from datetime import datetime, timedelta

def get_tomorrow_info():
    """获取明天的时间信息"""
    tomorrow = datetime.now() + timedelta(days=1)
    return {
        'date_ymd': tomorrow.strftime("%Y-%m-%d"),
        'date_mdy': tomorrow.strftime("%m/%d/%Y"),
        'date_dmy': tomorrow.strftime("%d/%m/%Y"),
        'chinese_date': tomorrow.strftime("%Y年%m月%d日"),
        'weekday': tomorrow.strftime("%A"),
        'chinese_weekday': get_chinese_weekday(tomorrow.weekday())
    }

def get_chinese_weekday(weekday):
    """获取中文星期"""
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[weekday]

def print_qq_mail_search():
    """打印QQ邮箱搜索指南"""
    print("\n" + "="*60)
    print("📧 QQ邮箱搜索指南")
    print("="*60)
    
    print("\n🔗 访问方式:")
    print("   1. 网页版: https://mail.qq.com")
    print("   2. 手机APP: QQ邮箱APP")
    
    print("\n🔍 搜索语法（QQ邮箱支持）:")
    print("   1. 基础搜索:")
    print("      - 关键词: 直接在搜索框输入关键词")
    print("      - 示例: '会议 明天'")
    
    print("\n   2. 高级搜索语法:")
    print("      - from:发件人邮箱 - 按发件人搜索")
    print("      - to:收件人邮箱 - 按收件人搜索")
    print("      - subject:主题词 - 按主题搜索")
    print("      - 日期范围: 在高级搜索中选择日期")
    
    print("\n   3. 组合搜索示例:")
    print("      - from:同事@qq.com subject:会议")
    print("      - subject:项目讨论 from:领导@company.com")
    
    print("\n📱 QQ邮箱手机APP搜索技巧:")
    print("   1. 点击顶部搜索图标")
    print("   2. 输入关键词后，可以筛选:")
    print("      - 全部邮件")
    print("      - 收件箱")
    print("      - 已发送")
    print("      - 特定文件夹")
    
    print("\n💡 QQ邮箱特有功能:")
    print("   1. 会话模式: 查看完整邮件往来")
    print("   2. 附件预览: 直接预览附件内容")
    print("   3. 星标邮件: 重要邮件可以加星标")

def print_gmail_search():
    """打印Gmail搜索指南"""
    print("\n" + "="*60)
    print("📧 Gmail搜索指南")
    print("="*60)
    
    print("\n🔗 访问方式:")
    print("   1. 网页版: https://mail.google.com")
    print("   2. 手机APP: Gmail APP")
    
    print("\n🔍 Gmail强大搜索运算符:")
    print("   1. 时间相关:")
    print("      - after:2026/02/28 - 2月28日之后")
    print("      - before:2026/03/02 - 3月2日之前")
    print("      - newer_than:2d - 2天内的邮件")
    
    print("\n   2. 发件人/收件人:")
    print("      - from:example@gmail.com")
    print("      - to:someone@domain.com")
    print("      - cc:抄送人@email.com")
    print("      - bcc:密送人@email.com")
    
    print("\n   3. 邮件属性:")
    print("      - subject:会议主题")
    print("      - has:attachment - 有附件")
    print("      - filename:agenda.pdf - 附件名为agenda.pdf")
    print("      - larger:5M - 大于5MB的邮件")
    
    print("\n   4. 标签和状态:")
    print("      - label:重要 - 重要标签")
    print("      - is:unread - 未读邮件")
    print("      - is:starred - 星标邮件")
    print("      - is:draft - 草稿")
    
    print("\n🎯 针对明天的会议搜索示例:")
    tomorrow = get_tomorrow_info()
    
    print(f"\n   1. 精确日期搜索:")
    print(f"      after:{tomorrow['date_ymd']} before:{tomorrow['date_ymd']}")
    print(f"      subject:会议 after:{tomorrow['date_ymd']}")
    
    print(f"\n   2. 会议相关搜索:")
    print(f"      subject:(meeting OR 会议) after:{tomorrow['date_ymd']}")
    print(f"      from:(同事) subject:(agenda OR 议程)")
    
    print(f"\n   3. 平台相关搜索:")
    print(f"      (Zoom OR Teams OR \"腾讯会议\") after:{tomorrow['date_ymd']}")

def print_combined_search_strategy():
    """打印组合搜索策略"""
    tomorrow = get_tomorrow_info()
    
    print("\n" + "="*60)
    print("🎯 双邮箱组合搜索策略")
    print("="*60)
    
    print(f"\n📅 明天: {tomorrow['chinese_date']} {tomorrow['chinese_weekday']}")
    
    print("\n🔄 建议搜索流程:")
    print("   第1步: 在QQ邮箱中搜索工作相关会议")
    print("   第2步: 在Gmail中搜索国际或技术相关会议")
    print("   第3步: 交叉验证重要会议")
    
    print("\n🔑 关键搜索词（中英文结合）:")
    print("   1. 会议/meeting")
    print("   2. 邀请/invitation")
    print("   3. 议程/agenda")
    print("   4. 日历邀请/calendar invite")
    print("   5. Zoom/Teams/腾讯会议")
    
    print(f"\n📋 具体搜索命令:")
    
    print("\n   A. QQ邮箱搜索:")
    print(f"      1. subject:会议 {tomorrow['date_ymd']}")
    print(f"      2. {tomorrow['chinese_date']} 会议")
    print(f"      3. 明天 例会")
    
    print("\n   B. Gmail搜索:")
    print(f"      1. after:{tomorrow['date_ymd']} before:{tomorrow['date_ymd']}")
    print(f"      2. subject:(meeting OR conference) after:{tomorrow['date_ymd']}")
    print(f"      3. has:attachment filename:(agenda OR ppt) newer_than:7d")
    
    print("\n💡 高效技巧:")
    print("   1. 先宽后窄: 先宽泛搜索，再逐步缩小范围")
    print("   2. 保存搜索: 将常用搜索保存为过滤器")
    print("   3. 使用标签: 为重要会议邮件添加标签")
    print("   4. 检查垃圾邮件: 重要邮件可能被误判")

def print_automation_options():
    """打印自动化选项"""
    print("\n" + "="*60)
    print("🤖 自动化搜索选项")
    print("="*60)
    
    print("\n我可以帮你创建自动化脚本，需要以下信息:")
    
    print("\n1. IMAP访问配置（安全方式）:")
    print("   - QQ邮箱IMAP: imap.qq.com (SSL, 端口993)")
    print("   - Gmail IMAP: imap.gmail.com (SSL, 端口993)")
    print("   - 需要应用专用密码（非登录密码）")
    
    print("\n2. API访问（更安全）:")
    print("   - Gmail API: 需要OAuth 2.0配置")
    print("   - QQ邮箱可能没有公开API")
    
    print("\n3. 浏览器自动化:")
    print("   - 使用Selenium自动登录并搜索")
    print("   - 需要保存登录状态")
    
    print("\n⚠️ 安全提醒:")
    print("   1. 不要将密码硬编码在脚本中")
    print("   2. 使用环境变量存储敏感信息")
    print("   3. 考虑使用OAuth等安全认证方式")

def main():
    """主函数"""
    print("="*70)
    print("📧 QQ邮箱 & Gmail邮箱 - 会议邮件搜索专家")
    print("="*70)
    
    tomorrow = get_tomorrow_info()
    print(f"\n🎯 目标: 搜索明天({tomorrow['chinese_date']})的会议及相关背景邮件")
    
    # 显示各邮箱搜索指南
    print_qq_mail_search()
    print_gmail_search()
    print_combined_search_strategy()
    
    # 询问是否需要自动化
    print("\n" + "="*70)
    print("❓ 需要自动化搜索吗？")
    print("="*70)
    
    print_automation_options()
    
    print("\n📝 下一步建议:")
    print("   1. 先手动搜索，找到会议主题")
    print("   2. 告诉我会议关键词，我提供更精准建议")
    print("   3. 如果需要自动化，提供邮箱类型和访问方式")

if __name__ == "__main__":
    main()