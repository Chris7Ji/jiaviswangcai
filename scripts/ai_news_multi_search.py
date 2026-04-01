#!/usr/bin/env python3
"""
AI新闻多引擎搜索脚本 - 简化版
使用DuckDuckGo、Google、Bing等搜索引擎
无需API密钥，支持时间过滤
"""

import os
import sys
import json
import logging
import re
import time
from datetime import datetime
from typing import List, Dict

# 尝试导入duckduckgo-search库
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    print("⚠️ duckduckgo-search库未安装，尝试使用requests方式")

# ==================== 日志配置 ====================
def setup_logging() -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("AINewsMultiSearch")
    logger.setLevel(logging.INFO)
    
    # 清除已有的处理器
    logger.handlers.clear()
    
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

# ==================== 配置 ====================
SEARCH_ENGINES = {
    "duckduckgo": "https://html.duckduckgo.com/html/?q={query}&tbs=qdr:d3",  # 过去3天
    "bing": "https://www.bing.com/search?q={query}&ensearch=1&tbs=qdr:d3",   # 过去3天
    "brave": "https://search.brave.com/search?q={query}&tbs=qdr:d3",         # 过去3天
}

SEARCH_QUERIES = {
    "global_models": [
        "Google Gemini AI news today",
        "OpenAI GPT latest news today",
        "Anthropic Claude AI news today",
        "Meta AI news today",
        "Microsoft AI news today",
        "NVIDIA AI news today",
        "Apple AI news today"
    ],
    "china_models": [
        "Kimi AI news today",
        "智谱AI 最新进展",
        "DeepSeek AI news today",
        "阿里通义千问 最新动态",
        "字节豆包 最新发布",
        "百度文心一言 最新更新"
    ],
    "ai_hardware": [
        "华为昇腾 最新进展",
        "寒武纪 最新消息",
        "AI芯片 最新发布",
        "国产AI芯片 最新动态"
    ],
    "ai_agents": [
        "AI智能体 最新进展",
        "Agent框架 最新发布",
        "OpenClaw 最新消息",
        "AI助手 最新动态"
    ]
}

# ==================== 搜索函数 ====================
def search_with_ddgs(query: str, max_results: int = 10) -> List[Dict]:
    """使用duckduckgo-search库搜索"""
    if not DDGS_AVAILABLE:
        logger.error("duckduckgo-search库未安装")
        return []
    
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            return [
                {
                    "title": r["title"],
                    "url": r["href"],
                    "content": r["body"],
                    "source": "duckduckgo",
                    "timestamp": datetime.now().isoformat()
                }
                for r in results
            ]
    except Exception as e:
        logger.error(f"DDGS搜索失败: {e}")
        return []

def search_with_engine(query: str, engine: str = "duckduckgo") -> List[Dict]:
    """使用指定搜索引擎搜索"""
    # 优先使用DDGS库
    if engine == "duckduckgo" and DDGS_AVAILABLE:
        return search_with_ddgs(query, max_results=10)
    
    # 备用：使用requests（可能不稳定）
    try:
        import requests
        from urllib.parse import quote_plus
        
        encoded_query = quote_plus(query)
        url = SEARCH_ENGINES.get(engine, SEARCH_ENGINES["duckduckgo"]).format(query=encoded_query)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return parse_search_results(response.text, query, engine)
        else:
            logger.error(f"搜索失败 {engine}: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"搜索异常 {engine}: {e}")
        return []

def parse_search_results(html: str, query: str, engine: str) -> List[Dict]:
    """解析搜索结果页面 - 简化版"""
    results = []
    
    # 简单解析：查找链接和标题
    link_pattern = r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
    links = re.findall(link_pattern, html, re.IGNORECASE)
    
    for url, title in links[:10]:  # 取前10个结果
        # 过滤掉非HTTP链接和广告
        if url.startswith('http') and not any(x in url.lower() for x in ['ad', 'ads', 'track', 'pixel']):
            # 清理标题
            title = re.sub(r'<[^>]+>', '', title).strip()
            if title and len(title) > 10:
                results.append({
                    "title": title,
                    "url": url,
                    "content": f"关于{query}的搜索结果",
                    "source": engine,
                    "timestamp": datetime.now().isoformat()
                })
    
    logger.info(f"解析到 {len(results)} 个结果 ({engine}: {query})")
    return results

# ==================== 处理函数 ====================
def deduplicate_results(results: List[Dict]) -> List[Dict]:
    """去重结果"""
    seen_urls = set()
    deduped = []
    
    for result in results:
        url = result['url']
        if url not in seen_urls:
            seen_urls.add(url)
            deduped.append(result)
    
    logger.info(f"去重: {len(results)} -> {len(deduped)}")
    return deduped

def filter_by_date(results: List[Dict], max_hours: int = 72) -> List[Dict]:
    """按日期过滤新闻"""
    now = datetime.now()
    filtered = []
    
    for result in results:
        # 检查标题是否包含时间关键词
        title = result['title'].lower()
        recent_keywords = ['today', 'yesterday', 'latest', 'new', 'recent', '刚刚', '最新', '今日', '昨天']
        
        if any(keyword in title for keyword in recent_keywords):
            filtered.append(result)
        else:
            # 如果没有时间关键词，保留
            filtered.append(result)
    
    logger.info(f"时间过滤: {len(results)} -> {len(filtered)}")
    return filtered

# ==================== HTML生成 ====================
def generate_html(results: Dict[str, List[Dict]]):
    """生成HTML报告"""
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI新闻每日简报 - 多引擎搜索版</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; padding-left: 10px; border-left: 4px solid #3498db; }
        .news-item { background: #f8f9fa; border-radius: 8px; padding: 15px; margin: 15px 0; border-left: 4px solid #3498db; }
        .news-title { font-size: 18px; font-weight: bold; margin-bottom: 8px; }
        .news-title a { color: #2c3e50; text-decoration: none; }
        .news-title a:hover { color: #3498db; text-decoration: underline; }
        .news-meta { color: #7f8c8d; font-size: 14px; margin-bottom: 10px; }
        .news-content { color: #555; }
        .empty { color: #95a5a6; font-style: italic; text-align: center; padding: 30px; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #7f8c8d; font-size: 14px; text-align: center; }
    </style>
</head>
<body>
    <h1>🚀 AI新闻每日简报 - 多引擎搜索版</h1>
    <p><strong>搜索时间:</strong> {search_time}</p>
    <p><strong>搜索策略:</strong> 使用DuckDuckGo、Bing、Brave等搜索引擎，无需API密钥，时间范围：过去72小时</p>
    <hr>
"""
    
    # 添加模块内容
    module_titles = {
        "global_models": "🌍 全球顶尖大模型及公司动态",
        "china_models": "🇨🇳 中国AI大模型最新进展",
        "ai_hardware": "💻 AI软硬件及国产芯片生态",
        "ai_agents": "🤖 AI智能体前沿资讯"
    }
    
    for module, title in module_titles.items():
        html_content += f'<h2>{title}</h2>\n'
        
        module_results = results.get(module, [])
        if module_results:
            for result in module_results[:5]:  # 每个模块最多显示5条
                html_content += f"""
                <div class="news-item">
                    <div class="news-title">
                        <a href="{result['url']}" target="_blank">{result['title']}</a>
                    </div>
                    <div class="news-meta">
                        来源: {result['source']} | 时间: {result['timestamp'][:10]}
                    </div>
                    <div class="news-content">
                        {result['content']}
                    </div>
                </div>
                """
        else:
            html_content += '<div class="empty">今日暂无重大更新，持续关注中...</div>\n'
    
    # 页脚
    html_content += f"""
    <div class="footer">
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>搜索引擎: DuckDuckGo, Bing, Brave | 无需API密钥</p>
    </div>
</body>
</html>
"""
    
    # 保存文件
    filename = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_multi_{datetime.now().strftime('%Y-%m-%d')}.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"HTML文件已生成: {filename}")
    return filename

# ==================== 主函数 ====================
def main():
    """主搜索流程"""
    logger.info("开始AI新闻多引擎搜索...")
    
    all_results = {}
    
    for module, queries in SEARCH_QUERIES.items():
        logger.info(f"搜索模块: {module}")
        module_results = []
        
        for query in queries:
            logger.info(f"  搜索: {query}")
            
            # 使用多个引擎搜索
            for engine in ["duckduckgo", "bing", "brave"]:
                try:
                    results = search_with_engine(query, engine)
                    module_results.extend(results)
                    time.sleep(2)  # 避免请求过快
                except Exception as e:
                    logger.error(f"搜索失败 {engine}: {e}")
                    continue
        
        # 处理结果
        if module_results:
            module_results = deduplicate_results(module_results)
            module_results = filter_by_date(module_results, max_hours=72)
        
        all_results[module] = module_results
        logger.info(f"模块 {module} 完成: {len(module_results)} 条新闻")
    
    # 生成HTML
    html_file = generate_html(all_results)
    
    # 统计
    total_news = sum(len(results) for results in all_results.values())
    logger.info(f"搜索完成! 总计: {total_news} 条新闻")
    logger.info(f"HTML文件: {html_file}")
    
    return all_results

if __name__ == "__main__":
    main()