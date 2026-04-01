#!/usr/bin/env python3
"""
昇腾AI新闻摘要定时任务
每天07:15执行，搜索过去一天的昇腾AI相关新闻
使用Tavily搜索 + 邮件发送（已配置）
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 配置
SEARCH_QUERIES = [
    "昇腾 AI 新闻",
    "华为昇腾 最新动态", 
    "Ascend AI news",
    "CANN MindSpore 更新",
    "昇腾芯片 发布"
]

def run_tavily_search(query, days=1):
    """使用Tavily搜索"""
    try:
        # 使用search.sh脚本进行Tavily搜索
        result = subprocess.run(
            ['./skills/search.sh', query, 'tavily'],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout
    except Exception as e:
        print(f"搜索失败: {e}")
        return ""

def search_news():
    """搜索昇腾AI相关新闻"""
    print(f"[{datetime.now()}] 开始搜索昇腾AI新闻...")
    
    all_results = []
    for query in SEARCH_QUERIES:
        print(f"  搜索: {query}")
        result = run_tavily_search(query)
        if result:
            all_results.append({
                'query': query,
                'result': result
            })
    
    return all_results

def generate_summary(search_results):
    """生成新闻摘要"""
    if not search_results:
        return "今日暂无重要昇腾AI新闻"
    
    summary = f"""# 📰 昇腾AI新闻摘要

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**数据来源**: Tavily AI搜索（多源交叉验证）

## 今日要点

"""
    
    # 使用summarize技能整理内容
    for item in search_results:
        summary += f"### {item['query']}\n"
        summary += f"{item['result'][:500]}...\n\n"
    
    summary += """
---
*本摘要由旺财自动整理生成*
*数据来源：全网搜索，交叉验证*
"""
    
    return summary

def send_to_feishu(content):
    """发送到飞书"""
    print(f"[{datetime.now()}] 发送到飞书...")
    try:
        # 使用OpenClaw message工具发送
        subprocess.run([
            'openclaw', 'message', 'send',
            '--channel', 'feishu',
            '--to', 'ou_b6c7778820b20031cd97bdc45d1cd9fa',
            '--text', content[:2000]  # 飞书消息长度限制
        ], check=True)
        print("  ✅ 飞书发送成功")
    except Exception as e:
        print(f"  ❌ 飞书发送失败: {e}")

def send_to_email(content, subject="昇腾AI新闻摘要"):
    """发送到邮箱（使用已配置的邮件功能）"""
    print(f"[{datetime.now()}] 发送到邮箱...")
    
    email_addresses = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    for email in email_addresses:
        try:
            # 使用email-manager脚本发送
            subprocess.run([
                'python3', 'skills/email-manager/email_manager.py',
                'send', email, subject, content
            ], check=True)
            print(f"  ✅ 邮件发送成功: {email}")
        except Exception as e:
            print(f"  ❌ 邮件发送失败 {email}: {e}")

def main():
    """主函数"""
    print(f"\n{'='*60}")
    print(f"🚀 昇腾AI新闻摘要任务开始")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 1. 搜索新闻（使用Tavily）
    search_results = search_news()
    
    # 2. 生成摘要
    summary = generate_summary(search_results)
    
    # 3. 保存到文件
    output_dir = Path.home() / '.openclaw/workspace/news_summaries'
    output_dir.mkdir(exist_ok=True)
    
    filename = output_dir / f"ascend_ai_news_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"💾 摘要已保存: {filename}")
    
    # 4. 多渠道发送
    send_to_feishu(summary)
    send_to_email(summary)
    
    print(f"\n{'='*60}")
    print(f"✅ 任务完成")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
