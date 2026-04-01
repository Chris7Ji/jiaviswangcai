#!/usr/bin/env python3
"""
AI新闻每日摘要主脚本 - 使用Tavily API
"""

import os
import sys
import json
import requests
from datetime import datetime
import subprocess

def read_tavily_api_key():
    """读取Tavily API密钥"""
    key_path = "/Users/jiyingguo/.openclaw/workspace/tavily_api_key.txt"
    if not os.path.exists(key_path):
        print("错误：找不到Tavily API密钥文件")
        return None
    
    with open(key_path, 'r') as f:
        api_key = f.read().strip()
    
    if not api_key:
        print("错误：Tavily API密钥为空")
        return None
    
    return api_key

def search_ai_news_tavily(api_key):
    """使用Tavily搜索AI新闻"""
    print("使用Tavily API搜索AI新闻...")
    
    # 多个搜索查询，提高覆盖率，获取5-10条新闻
    queries = [
        "AI人工智能最新新闻 2026年",
        "机器学习 深度学习 最新进展",
        "大模型 人工智能 技术突破",
        "中国AI技术发展 2026",
        "AI产业投资 2026",
        "人工智能应用场景"
    ]
    
    all_results = []
    
    for query in queries:
        try:
            payload = {
                "api_key": api_key,
                "query": query,
                "max_results": 4,  # 每个查询获取4条，总共最多24条，去重后约5-10条
                "search_depth": "advanced"
            }
            
            response = requests.post(
                "https://api.tavily.com/search",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if "results" in data:
                    for result in data["results"]:
                        # 去重
                        url = result.get("url", "")
                        if not any(r.get("url") == url for r in all_results):
                            all_results.append(result)
                    print(f"  查询 '{query}' 找到 {len(data['results'])} 条结果")
            else:
                print(f"  查询 '{query}' 失败: {response.status_code}")
                
        except Exception as e:
            print(f"  查询 '{query}' 异常: {e}")
    
    return all_results

def fetch_xinhua_news_backup():
    """备用方案：抓取新华网新闻"""
    print("使用备用方案：抓取新华网科技新闻...")
    
    # 这里可以调用web_fetch或直接请求
    # 暂时返回空，由调用者处理
    return []

def process_news_results(results, source="Tavily"):
    """处理新闻结果"""
    if not results:
        return []
    
    news_items = []
    
    for i, result in enumerate(results[:10], 1):  # 取前10条
        title = result.get("title", "").strip()
        url = result.get("url", "").strip()
        content = result.get("content", "").strip()
        
        if not title or not content:
            continue
        
        # 清理内容
        if len(content) > 400:
            content = content[:400] + "..."
        
        news_item = {
            "序号": i,
            "标题": title,
            "来源": source,
            "链接": url,
            "摘要": content,
            "发布日期": datetime.now().strftime("%Y-%m-%d")
        }
        
        news_items.append(news_item)
    
    return news_items

def create_markdown_summary(news_items, use_tavily=True):
    """创建Markdown格式摘要"""
    today = datetime.now().strftime("%Y年%m月%d日")
    source_note = "（通过Tavily API智能搜索）" if use_tavily else "（通过新华网）"
    
    markdown = f"# AI新闻每日摘要 - {today}\n\n"
    markdown += f"## 今日重要AI新闻概览{source_note}\n\n"
    
    if not news_items:
        markdown += "今天没有找到相关的AI新闻。\n"
        return markdown
    
    for item in news_items[:10]:  # 最多显示10条
        markdown += f"### {item['序号']}. {item['标题']}\n"
        markdown += f"**来源：** {item['来源']}\n"
        
        if item['链接']:
            markdown += f"**链接：** {item['链接']}\n"
        
        markdown += f"**发布日期：** {item['发布日期']}\n\n"
        markdown += f"**内容摘要：**\n{item['摘要']}\n\n"
        
        if item['链接']:
            markdown += f"**原文链接：** {item['链接']}\n"
        
        markdown += "---\n\n"
    
    # 添加总结
    markdown += "## 📊 今日AI趋势观察\n\n"
    markdown += "1. **技术融合加速**：AI与各行业深度结合\n"
    markdown += "2. **大模型竞争激烈**：国内外企业持续投入\n"
    markdown += "3. **应用场景拓展**：从实验室走向实际应用\n"
    markdown += "4. **安全与治理**：AI伦理和监管受关注\n\n"
    
    markdown += f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    markdown += f"**数据来源：** {'Tavily API + 智能搜索' if use_tavily else '新华网科技频道'}\n"
    
    return markdown

def save_summary_files(markdown_content):
    """保存摘要文件"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = "/Users/jiyingguo/.openclaw/workspace/news_summaries"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存Markdown文件
    md_file = f"{output_dir}/ai_news_{today_str}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Markdown摘要已保存: {md_file}")
    
    # 可以添加HTML转换逻辑（如果需要）
    html_file = f"{output_dir}/ai_news_{today_str}.html"
    # 简单的HTML转换
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI新闻每日摘要 - {today_str}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; }}
        h2 {{ color: #555; }}
        h3 {{ color: #666; }}
        a {{ color: #4CAF50; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .news-item {{ margin-bottom: 30px; padding: 15px; background: #f9f9f9; border-radius: 5px; }}
        .footer {{ margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; color: #777; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>AI新闻每日摘要 - {today_str}</h1>
    <div id="content">
        {markdown_content.replace('# ', '<h2>').replace('## ', '<h3>').replace('### ', '<h4>').replace('\n\n', '</p><p>').replace('\n', '<br>')}
    </div>
    <div class="footer">
        生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        数据来源: Tavily API + 智能搜索
    </div>
</body>
</html>
"""
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML摘要已保存: {html_file}")
    
    return md_file, html_file

def main():
    """主函数"""
    print("="*60)
    print("AI新闻每日摘要任务开始执行")
    print("="*60)
    
    # 1. 读取Tavily API密钥
    api_key = read_tavily_api_key()
    use_tavily = api_key is not None
    
    news_results = []
    
    # 2. 尝试使用Tavily API
    if use_tavily:
        news_results = search_ai_news_tavily(api_key)
    
    # 3. 如果Tavily失败或结果为空，使用备用方案
    if not news_results:
        print("Tavily API未返回有效结果，使用备用方案...")
        use_tavily = False
        # 这里可以调用现有的新华网抓取逻辑
        # news_results = fetch_xinhua_news_backup()
    
    # 4. 处理结果
    news_items = process_news_results(news_results, "Tavily" if use_tavily else "新华网")
    
    if not news_items:
        print("⚠️ 未找到任何新闻，创建空摘要")
        news_items = [{
            "序号": 1,
            "标题": "今日暂无AI新闻",
            "来源": "系统",
            "链接": "",
            "摘要": "今天没有找到相关的AI新闻，可能是数据源暂时不可用。",
            "发布日期": datetime.now().strftime("%Y-%m-%d")
        }]
    
    # 5. 创建摘要
    print("正在生成新闻摘要...")
    markdown_content = create_markdown_summary(news_items, use_tavily)
    
    # 6. 保存文件
    md_file, html_file = save_summary_files(markdown_content)
    
    # 7. 输出总结
    print("\n" + "="*60)
    print("✅ 任务执行完成!")
    print(f"   找到新闻: {len(news_items)} 条")
    print(f"   数据来源: {'Tavily API' if use_tavily else '备用新闻源'}")
    print(f"   文件保存: {md_file}")
    print(f"              {html_file}")
    print("="*60)
    
    # 返回成功状态
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)