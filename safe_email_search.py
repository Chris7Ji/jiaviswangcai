#!/usr/bin/env python3
"""
安全邮件搜索脚本 - 使用环境变量存储密码
"""

import os
import sys
from datetime import datetime, timedelta

def check_environment():
    """检查环境变量配置"""
    print("🔍 检查环境变量配置...")
    
    env_vars = {
        'QQ_EMAIL': 'QQ邮箱地址 (如: 12345678@qq.com)',
        'QQ_APP_PASSWORD': 'QQ邮箱授权码 (16位)',
        'GMAIL_ADDRESS': 'Gmail邮箱地址',
        'GMAIL_APP_PASSWORD': 'Gmail应用专用密码 (16位)'
    }
    
    missing_vars = []
    for var, description in env_vars.items():
        if var not in os.environ:
            missing_vars.append((var, description))
    
    if missing_vars:
        print("❌ 缺少以下环境变量:")
        for var, description in missing_vars:
            print(f"   {var}: {description}")
        return False
    else:
        print("✅ 环境变量配置完整")
        return True

def generate_search_commands():
    """生成搜索命令"""
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    
    print(f"\n📅 明天日期: {tomorrow_str}")
    
    print("\n🔍 推荐搜索命令:")
    
    print("\n1. QQ邮箱网页版搜索:")
    print(f"   a. 精确日期: \"{tomorrow_str}\"")
    print(f"   b. 会议相关: \"{tomorrow_str} 会议\"")
    print(f"   c. 邀请相关: \"{tomorrow_str} 邀请\"")
    print(f"   d. 议程相关: \"{tomorrow_str} 议程\"")
    
    print("\n2. Gmail网页版搜索:")
    print(f"   a. 日期范围: after:{tomorrow_str} before:{tomorrow_str}")
    print(f"   b. 会议搜索: subject:(meeting OR 会议) after:{tomorrow_str}")
    print(f"   c. 附件搜索: has:attachment after:{tomorrow_str}")
    print(f"   d. 平台搜索: (Zoom OR Teams OR \"腾讯会议\") after:{tomorrow_str}")
    
    print("\n3. 组合搜索（提高命中率）:")
    print(f"   a. \"{tomorrow_str}\" (会议 OR meeting OR 邀请 OR invitation)")
    print(f"   b. \"议程\" OR \"agenda\" AND \"{tomorrow_str}\"")
    print(f"   c. \"日历邀请\" AND \"{tomorrow_str}\"")

def setup_environment_instructions():
    """提供环境变量设置说明"""
    print("\n" + "="*70)
    print("🛠️ 环境变量设置指南")
    print("="*70)
    
    print("\n📋 设置方法（选择一种）:")
    
    print("\nA. 临时设置（当前终端会话）:")
    print("""
    # 在终端中执行
    export QQ_EMAIL="你的QQ邮箱"
    export QQ_APP_PASSWORD="你的QQ邮箱授权码"
    export GMAIL_ADDRESS="你的Gmail地址"
    export GMAIL_APP_PASSWORD="你的Gmail应用密码"
    """)
    
    print("\nB. 永久设置（添加到shell配置文件）:")
    print("""
    # 编辑 ~/.zshrc 或 ~/.bash_profile
    export QQ_EMAIL="你的QQ邮箱"
    export QQ_APP_PASSWORD="你的QQ邮箱授权码"
    export GMAIL_ADDRESS="你的Gmail地址"
    export GMAIL_APP_PASSWORD="你的Gmail应用密码"
    
    # 然后执行
    source ~/.zshrc
    """)
    
    print("\nC. 使用.env文件（推荐用于项目）:")
    print("""
    # 创建 .env 文件
    cat > .env << EOF
    QQ_EMAIL=你的QQ邮箱
    QQ_APP_PASSWORD=你的QQ邮箱授权码
    GMAIL_ADDRESS=你的Gmail地址
    GMAIL_APP_PASSWORD=你的Gmail应用密码
    EOF
    
    # 加载环境变量
    export $(grep -v '^#' .env | xargs)
    """)

def quick_search_guide():
    """快速搜索指南"""
    print("\n" + "="*70)
    print("⚡ 5分钟快速搜索方案")
    print("="*70)
    
    print("\n🎯 目标: 在5分钟内找到明天的会议邮件")
    
    print("\n🔄 操作流程:")
    print("   1. 打开QQ邮箱网页版 (mail.qq.com)")
    print("   2. 在搜索框输入: \"2026-03-01 会议\"")
    print("   3. 按时间倒序排列结果")
    print("   4. 查看前10封邮件")
    
    print("\n   5. 打开Gmail网页版 (mail.google.com)")
    print("   6. 在搜索框输入: \"after:2026-03-01 before:2026-03-01 meeting\"")
    print("   7. 同样按时间倒序排列")
    print("   8. 查看前10封邮件")
    
    print("\n🔑 关键检查点:")
    print("   1. 会议邀请邮件（通常有日历附件）")
    print("   2. 会议议程邮件（通常有PDF/PPT附件）")
    print("   3. 会议确认邮件（确认参会）")
    print("   4. 会议变更通知（时间/地点变更）")
    
    print("\n💡 如果找不到:")
    print("   1. 检查垃圾邮件文件夹")
    print("   2. 搜索更宽泛的关键词: \"明天\"、\"3月1日\"")
    print("   3. 检查日历应用（可能有直接邀请）")
    print("   4. 查看团队协作工具（飞书/钉钉/Slack）")

def create_automation_script():
    """创建自动化脚本模板"""
    script_content = '''#!/usr/bin/env python3
"""
自动化邮件搜索脚本
使用前请设置环境变量
"""

import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta

def search_qq_emails():
    """搜索QQ邮箱"""
    try:
        # 从环境变量获取配置
        username = os.getenv('QQ_EMAIL')
        password = os.getenv('QQ_APP_PASSWORD')
        
        if not username or not password:
            print("❌ 请设置QQ_EMAIL和QQ_APP_PASSWORD环境变量")
            return []
        
        # 连接到QQ邮箱
        print("🔗 连接到QQ邮箱...")
        mail = imaplib.IMAP4_SSL('imap.qq.com', 993)
        mail.login(username, password)
        
        # 选择收件箱
        mail.select('INBOX')
        
        # 设置搜索条件（明天）
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y')
        search_criteria = f'(SINCE "{tomorrow}") (OR SUBJECT "会议" SUBJECT "meeting")'
        
        # 搜索邮件
        status, messages = mail.search(None, search_criteria)
        
        results = []
        if status == 'OK':
            email_ids = messages[0].split()
            print(f"📨 QQ邮箱找到 {len(email_ids)} 封相关邮件")
            
            # 获取前5封邮件的详情
            for i, email_id in enumerate(email_ids[:5]):
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # 解析主题
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    
                    results.append({
                        'source': 'QQ邮箱',
                        'subject': subject,
                        'from': msg.get('From', ''),
                        'date': msg.get('Date', '')
                    })
        
        mail.logout()
        return results
        
    except Exception as e:
        print(f"❌ QQ邮箱搜索失败: {str(e)}")
        return []

def search_gmail_emails():
    """搜索Gmail"""
    try:
        # 从环境变量获取配置
        username = os.getenv('GMAIL_ADDRESS')
        password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not username or not password:
            print("❌ 请设置GMAIL_ADDRESS和GMAIL_APP_PASSWORD环境变量")
            return []
        
        # 连接到Gmail
        print("🔗 连接到Gmail...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(username, password)
        
        # 选择收件箱
        mail.select('INBOX')
        
        # 设置搜索条件
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y')
        search_criteria = f'(SINCE "{tomorrow}") (OR SUBJECT "meeting" SUBJECT "conference")'
        
        # 搜索邮件
        status, messages = mail.search(None, search_criteria)
        
        results = []
        if status == 'OK':
            email_ids = messages[0].split()
            print(f"📨 Gmail找到 {len(email_ids)} 封相关邮件")
            
            # 获取前5封邮件的详情
            for i, email_id in enumerate(email_ids[:5]):
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # 解析主题
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    
                    results.append({
                        'source': 'Gmail',
                        'subject': subject,
                        'from': msg.get('From', ''),
                        'date': msg.get('Date', '')
                    })
        
        mail.logout()
        return results
        
    except Exception as e:
        print(f"❌ Gmail搜索失败: {str(e)}")
        return []

def main():
    """主函数"""
    print("="*60)
    print("📧 自动化邮件搜索")
    print("="*60)
    
    # 搜索QQ邮箱
    qq_results = search_qq_emails()
    
    # 搜索Gmail
    gmail_results = search_gmail_emails()
    
    # 显示结果
    all_results = qq_results + gmail_results
    
    if all_results:
        print(f"\n🎯 总共找到 {len(all_results)} 封相关邮件:")
        for i, result in enumerate(all_results, 1):
            print(f"\n{i}. [{result['source']}]")
            print(f"   主题: {result['subject']}")
            print(f"   发件人: {result['from']}")
            print(f"   日期: {result['date']}")
    else:
        print("\n📭 未找到相关会议邮件")
        print("💡 建议:")
        print("   1. 检查环境变量配置")
        print("   2. 尝试手动搜索")
        print("   3. 检查垃圾邮件文件夹")

if __name__ == "__main__":
    main()
'''
    
    script_path = "/Users/jiyingguo/.openclaw/workspace/auto_email_search.py"
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # 设置执行权限
        os.chmod(script_path, 0o755)
        
        print(f"\n✅ 自动化脚本已创建: {script_path}")
        print("\n📋 使用步骤:")
        print(f"   1. 设置环境变量（参考上面的指南）")
        print(f"   2. 运行脚本: python3 {script_path}")
        print(f"   3. 或直接运行: ./{script_path}")
        
        return script_path
        
    except Exception as e:
        print(f"❌ 创建脚本失败: {str(e)}")
        return None

def main():
    """主函数"""
    print("="*80)
    print("📧 QQ邮箱 & Gmail邮箱 - 安全搜索解决方案")
    print("="*80)
    
    # 检查环境变量
    env_ok = check_environment()
    
    # 生成搜索命令
    generate_search_commands()
    
    if not env_ok:
        # 提供环境变量设置指南
        setup_environment_instructions()
    
    # 提供快速搜索方案
    quick_search_guide()
    
    # 创建自动化脚本
    print("\n" + "="*80)
    print("🤖 自动化选项")
    print("="*80)
    
    script_path = create_automation_script()
    
    if script_path:
        print("\n⚠️ 重要安全提醒:")
        print("   1. 不要将脚本提交到Git等版本控制系统")
        print("   2. 定期更新邮箱授权码/应用密码")
        print("   3. 仅在受信任的环境中使用")
        print("   4. 考虑使用更安全的OAuth认证")
    
    print("\n🎯 总结建议:")
    print("   1. 先使用快速搜索方案手动查找")
    print("   2. 如果经常需要搜索，设置环境变量并使用自动化脚本")
    print("   3. 找到会议后，我可以帮你分析背景信息")

if __name__ == "__main__":
    main()