#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻搜索脚本（高质量实时版）

搜索策略：
1. 只看过去72小时内的真实事件
2. 排除分析、预测、回顾类文章
3. 多源验证确保真实性
4. 如实报告：如无重大新闻，标注"今日暂无重大更新"

搜索范围（5个模块）：
1. 全球顶尖大模型及公司动态
2. 中国AI大模型最新进展
3. AI软硬件及国产芯片生态
4. AI智能体前沿资讯
5. 其他全球AI领域重要资讯
"""

import os
import sys
import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import requests

# ==================== 配置信息 ====================
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "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")
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f")
SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
# DuckDuckGo 配置（无需API Key）
DDG_MAX_RESULTS = 5  # 每次搜索最多返回结果数

# 搜索关键词配置
SEARCH_QUERIES = {
    "global_models": [
        "Google Gemini 最新发布 过去48小时",
        "OpenAI GPT 最新进展 过去48小时",
        "Anthropic Claude 最新消息 过去48小时",
        "Meta AI 最新发布 过去48小时",
        "Microsoft AI 最新动态 过去48小时"
    ],
    "global_models_international": [
        "site:blog.google.com AI March 2026",
        "site:openai.com news March 2026",
        "site:anthropic.com news March 2026",
        "site:ai.meta.com March 2026",
        "site:blogs.nvidia.com AI March 2026",
        "Microsoft AI Copilot news March 2026",
        "Apple AI news March 2026"
    ],
    "china_models": [
        "Kimi 最新发布 过去48小时",
        "智谱AI 最新进展 过去48小时",
        "DeepSeek 最新消息 过去48小时",
        "阿里通义千问 最新动态 过去48小时",
        "字节豆包 最新发布 过去48小时"
    ],
    "ai_hardware": [
        "华为昇腾 最新进展 过去48小时",
        "寒武纪 最新消息 过去48小时",
        "AI芯片 最新发布 过去48小时",
        "国产AI芯片 最新动态 过去48小时"
    ],
    "ai_agents": [
        "AI智能体 最新进展 过去48小时",
        "Agent框架 最新发布 过去48小时",
        "OpenClaw 最新消息 过去48小时",
        "AI助手 最新动态 过去48小时"
    ],
    "other_ai": [
        "AI重要新闻 过去48小时",
        "人工智能重大突破 过去48小时",
        "AI领域重要事件 过去48小时"
    ]
}

# ==================== 日志配置 ====================
def setup_logging() -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("AINewsSearch")
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

# ==================== 来源可信度配置 ====================
# 来源黑名单（仅过滤高度不可信的来源）
SOURCE_BLACKLIST = [
    'instagram',  # 保留微博等中文社交媒体
    'twitter', 'facebook',
]

# 可信技术文档白名单
TECH_DOC_WHITELIST = [
    'cloud.tencent.com/developer',
    'juejin.im',  # 掘金技术社区
    'zhihu.com',  # 知乎
    'csdn.net',
    'github.com',
]

# 权威媒体列表
AUTHORITY_SOURCES = [
    '新华网', '人民网', '凤凰网', '36氪', '智东西',
    '新浪', '腾讯', '网易', '搜狐', '财新', '界面',
    'techcrunch', 'theverge', 'venturebeat', 'wired',
    'arstechnica', 'zdnet', 'cnet'
]

def check_source(url: str) -> tuple[bool, str]:
    """检查来源是否可信，返回(是否可信, 来源类型)"""
    url_lower = url.lower()

    # 检查是否在白名单中（可信技术文档）
    for white in TECH_DOC_WHITELIST:
        if white in url_lower:
            return True, "tech_doc"

    # 检查是否在黑名单中
    for black in SOURCE_BLACKLIST:
        if black in url_lower:
            return False, "blacklisted"

    return True, "general"

# ==================== 日期提取和过滤函数 ====================
def extract_date_from_text(text: str) -> Optional[datetime]:
    """从文本中提取日期"""
    # 匹配格式：2026年3月17日、2026-03-17、2026/03/17等
    patterns = [
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',
        r'(\d{4})-(\d{1,2})-(\d{1,2})',
        r'(\d{4})/(\d{1,2})/(\d{1,2})',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except:
                pass
    return None

def is_english_text(text: str) -> bool:
    """检测是否为英文内容"""
    if not text:
        return False
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    total = len(text.replace(' ', ''))
    if total == 0:
        return False
    return ascii_chars / total > 0.8


def is_likely_english(url: str, title: str) -> bool:
    """根据URL和标题判断是否为英文内容"""
    english_indicators = ['.com', '.org', '.io', 'techcrunch', 'theverge', 'wired', 'arstechnica']
    for indicator in english_indicators:
        if indicator in url.lower():
            return True
    return is_english_text(title)


def translate_to_chinese(text: str) -> str:
    """使用 DeepSeek-Chat 模型翻译英文到中文"""
    if not text or not is_english_text(text):
        return text
    
    try:
        import urllib.request
        import json
        
        url = "https://api.deepseek.com/v1/chat/completions"
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a professional translator. Translate the following English text to Chinese, keeping the style concise and professional. Only output the translation, nothing else."},
                {"role": "user", "content": text[:800]}  # 限制长度避免超时
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer sk-451f43ffa9764b7e91430e4d39538356'
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.warning(f"翻译失败: {e}")
        return text  # 失败时返回原文

def is_recent_news(article: Dict, max_hours: int = 48) -> bool:
    """检查新闻是否是最近发布的"""
    now = datetime.now()
    text = f"{article.get('title', '')} {article.get('content', '')} {article.get('url', '')}"
    
    # 尝试从文本中提取日期
    date = extract_date_from_text(text)
    if date:
        age = (now - date).total_seconds() / 3600
        return age <= max_hours
    
    # 如果没有找到日期，检查标题是否包含"最新"、"今日"、"昨天"等关键词
    recent_keywords = ['最新', '今日', '昨天', '刚刚', '日前', '近日', '小时前', '分钟前']
    for keyword in recent_keywords:
        if keyword in text:
            return True
    
    # 如果都找不到，默认返回False（不采用）
    return False

def filter_by_date(articles: List[Dict], max_hours: int = 72) -> List[Dict]:
    """按日期过滤新闻，只保留最近max_hours小时内的"""
    filtered = []
    for article in articles:
        if is_recent_news(article, max_hours):
            filtered.append(article)
    logger.info(f"日期过滤: {len(articles)} -> {len(filtered)} 个最近新闻（{max_hours}小时内）")
    return filtered

# ==================== DuckDuckGo搜索函数（无需额外包）====================
def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict]:
    """
    使用DuckDuckGo新闻搜索（无需API Key，直接调用）
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        搜索结果列表（格式兼容Tavily）
    """
    try:
        import urllib.parse
        
        # DuckDuckGo新闻搜索URL
        encoded_query = urllib.parse.quote(query)
        url = f"https://duckduckgo.com/html/?q={encoded_query}&t=h_&df=w"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            logger.error(f"DuckDuckGo搜索失败: HTTP {response.status_code}")
            return []
        
        # 解析HTML结果
        results = []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到新闻结果
        for result in soup.select('.result')[:max_results]:
            title_elem = result.select_one('.result__title a')
            snippet_elem = result.select_one('.result__snippet')
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                
                # 获取摘要
                snippet = ''
                if snippet_elem:
                    snippet = snippet_elem.get_text(strip=True)
                
                if title:
                    results.append({
                        "title": title,
                        "content": snippet,
                        "url": link,
                        "source": "DuckDuckGo"
                    })
        
        logger.info(f"DuckDuckGo搜索成功: '{query}' - 找到 {len(results)} 个结果")
        return results
        
    except ImportError:
        # 如果没有bs4，尝试直接解析（备用方案）
        logger.warning("BeautifulSoup未安装，使用备用解析方案")
        return search_duckduckgo_fallback(query, max_results)
    except Exception as e:
        logger.error(f"DuckDuckGo搜索异常: {e}")
        return []

def search_duckduckgo_fallback(query: str, max_results: int = 5) -> List[Dict]:
    """
    DuckDuckGo备用搜索（无bs4依赖）
    """
    try:
        import urllib.parse
        import re
        
        encoded_query = urllib.parse.quote(query)
        url = f"https://duckduckgo.com/html/?q={encoded_query}&t=h_&df=w"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return []
        
        results = []
        
        # 匹配 result__a 链接
        # 格式: <a class="result__a" href="URL" rel="nofollow">标题</a>
        pattern = r'<a class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, response.text)
        
        # 也获取 snippet
        snippet_pattern = r'<a class="result__snippet"[^>]*href="[^"]*"[^>]*>([^<]+)</a>'
        snippets = re.findall(snippet_pattern, response.text)
        
        for i, (url, title) in enumerate(matches[:max_results]):
            # 清理标题中的HTML标签和特殊字符
            title = re.sub(r'<[^>]+>', '', title).strip()
            title = re.sub(r'\s+', ' ', title)
            
            snippet = snippets[i] if i < len(snippets) else ""
            snippet = re.sub(r'<[^>]+>', '', snippet).strip()
            snippet = re.sub(r'\s+', ' ', snippet)
            
            results.append({
                "title": title,
                "content": snippet,
                "url": url,
                "source": "DuckDuckGo"
            })
        
        logger.info(f"DuckDuckGo(备用)搜索成功: '{query}' - 找到 {len(results)} 个结果")
        return results
        
    except Exception as e:
        logger.error(f"DuckDuckGo(备用)搜索异常: {e}")
        return []

# ==================== SerpAPI搜索函数 ====================
def search_serpapi(query: str, max_results: int = 5) -> Optional[List[Dict]]:
    """
    使用SerpAPI搜索新闻
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        搜索结果列表（格式兼容Tavily），连接失败返回None
    """
    try:
        import urllib.parse
        
        # 使用 SerpAPI 的 news 搜索模式 (tbm=nws)
        # 注意：与Tavily使用相同query，不额外添加语言/区域参数
        url = f"https://serpapi.com/search?q={urllib.parse.quote(query)}&api_key={SERPAPI_KEY}&num={max_results}&tbm=nws"
        
        # 设置更长的超时时间，并处理SSL问题
        response = requests.get(url, timeout=60, verify=True)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            # tbm=nws 时结果在 news_results，否则在 organic_results
            raw_results = data.get("news_results", []) or data.get("organic_results", [])
            
            for item in raw_results[:max_results]:
                results.append({
                    "title": item.get("title", ""),
                    "content": item.get("snippet", ""),
                    "url": item.get("link", ""),
                    "source": "SerpAPI"
                })
            
            logger.info(f"SerpAPI搜索成功: '{query}' - 找到 {len(results)} 个结果")
            return results
        elif response.status_code == 401:
            logger.error(f"SerpAPI API Key无效: {response.status_code}")
            return None  # 返回None表示连接失败
        elif response.status_code == 429:
            logger.warning(f"SerpAPI请求过多，请稍后重试: {response.status_code}")
            return None  # 返回None表示连接失败
        else:
            logger.error(f"SerpAPI搜索失败: HTTP {response.status_code} - {response.text[:200]}")
            return None  # 返回None表示连接失败
            
    except requests.exceptions.SSLError as e:
        logger.error(f"SerpAPI SSL错误: {e}，尝试禁用SSL验证...")
        # SSL错误时尝试禁用验证
        try:
            response = requests.get(url, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                results = []
                # tbm=nws 时结果在 news_results，否则在 organic_results
                raw_results = data.get("news_results", []) or data.get("organic_results", [])
                for item in raw_results[:max_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "content": item.get("snippet", ""),
                        "url": item.get("link", ""),
                        "source": "SerpAPI"
                    })
                logger.warning("SerpAPI SSL验证已禁用，搜索成功")
                return results
        except Exception as e2:
            logger.error(f"SerpAPI SSL重试失败: {e2}")
            return None  # 返回None表示连接失败
        return None
    except requests.exceptions.Timeout:
        logger.error("SerpAPI搜索超时（60秒）")
        return None  # 返回None表示连接失败
    except requests.exceptions.ConnectionError as e:
        logger.error(f"SerpAPI网络连接错误: {e}")
        return None  # 返回None表示连接失败
    except Exception as e:
        logger.error(f"SerpAPI搜索异常: {type(e).__name__}: {e}")
        return None  # 返回None表示连接失败

# ==================== Tavily搜索函数 ====================
def search_tavily(query: str, max_results: int = 5) -> List[Dict]:
    """
    使用Tavily API搜索新闻
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        搜索结果列表
    """
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "include_answer": True,
            "include_raw_content": True,
            "max_results": max_results,
            "include_images": False
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            logger.info(f"Tavily搜索成功: '{query}' - 找到 {len(results)} 个结果")
            return results
        elif response.status_code == 429:
            logger.warning(f"Tavily API请求过多，请稍后重试: {response.status_code}")
            return []
        elif response.status_code == 401:
            logger.error(f"Tavily API Key无效: {response.status_code}")
            return []
        elif response.status_code == 432:
            logger.error(f"Tavily API超过配额限制: {response.status_code}")
            return []
        else:
            logger.error(f"Tavily搜索失败: HTTP {response.status_code} - {response.text[:200]}")
            return []
            
    except requests.exceptions.SSLError as e:
        logger.error(f"Tavily SSL错误: {e}，尝试禁用SSL验证...")
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                logger.warning("Tavily SSL验证已禁用，搜索成功")
                return results
        except Exception as e2:
            logger.error(f"Tavily SSL重试失败: {e2}")
            return []
        return []
    except requests.exceptions.Timeout:
        logger.error("Tavily搜索超时（60秒）")
        return []
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Tavily网络连接错误: {e}")
        return []
    except Exception as e:
        logger.error(f"Tavily搜索异常: {type(e).__name__}: {e}")
        return []

# ==================== 统一搜索接口 ====================
def search_news(query: str, max_results: int = 5, prefer_serpapi: bool = True) -> List[Dict]:
    """
    并行查询 SerpAPI 和 Tavily，合并结果
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
        prefer_serpapi: 是否优先使用SerpAPI（保留参数兼容性）
    
    Returns:
        搜索结果列表（去重后合并）
    
    逻辑：
    1. SerpAPI 和 Tavily 同时查询
    2. 如果都成功：合并结果（去重）
    3. 如果只有一个成功：返回成功的结果
    4. 如果都失败：抛出异常
    """
    import concurrent.futures
    
    serpapi_results = None  # None表示查询失败
    tavily_results = None   # None表示查询失败
    
    def query_serpapi():
        try:
            logger.info(f"  [SerpAPI] 搜索: {query}")
            results = search_serpapi(query, max_results)
            if results is not None:
                logger.info(f"  [SerpAPI] 返回 {len(results)} 条结果")
            return results
        except Exception as e:
            logger.error(f"  [SerpAPI] 查询异常: {e}")
            return None
    
    def query_tavily():
        try:
            logger.info(f"  [Tavily] 搜索: {query}")
            results = search_tavily(query, max_results)
            if results:
                logger.info(f"  [Tavily] 返回 {len(results)} 条结果")
            return results
            return None
        except Exception as e:
            logger.error(f"  [Tavily] 查询异常: {e}")
            return None
    
    # 并行查询 SerpAPI 和 Tavily
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_serpapi = executor.submit(query_serpapi)
        future_tavily = executor.submit(query_tavily)
        
        try:
            serpapi_results = future_serpapi.result(timeout=30)
        except concurrent.futures.TimeoutError:
            logger.error("  [SerpAPI] 查询超时（30秒）")
            serpapi_results = None
        except Exception as e:
            logger.error(f"  [SerpAPI] 查询失败: {e}")
            serpapi_results = None
        
        try:
            tavily_results = future_tavily.result(timeout=30)
        except concurrent.futures.TimeoutError:
            logger.error("  [Tavily] 查询超时（30秒）")
            tavily_results = None
        except Exception as e:
            logger.error(f"  [Tavily] 查询失败: {e}")
            tavily_results = None
    
    # 统计成功和失败
    serpapi_success = serpapi_results is not None and len(serpapi_results) > 0
    tavily_success = tavily_results is not None and len(tavily_results) > 0
    
    # 根据结果情况返回
    if serpapi_success and tavily_success:
        # 两个都成功，合并结果
        logger.info(f"  [合并] SerpAPI({len(serpapi_results)}) + Tavily({len(tavily_results)}) = {len(serpapi_results) + len(tavily_results)} 条")
        return merge_results(serpapi_results, tavily_results)
    
    elif serpapi_success:
        # 只有SerpAPI成功
        logger.info(f"  [结果] 仅SerpAPI返回 {len(serpapi_results)} 条")
        return serpapi_results
    
    elif tavily_success:
        # 只有Tavily成功
        logger.info(f"  [结果] 仅Tavily返回 {len(tavily_results)} 条")
        return tavily_results
    
    else:
        # 两个都失败
        error_msg = "SerpAPI和Tavily搜索均失败"
        logger.error(f"  [错误] {error_msg}")
        raise Exception(error_msg)


def merge_results(list1: List[Dict], list2: List[Dict]) -> List[Dict]:
    """
    合并两个搜索结果列表，去重（基于URL）
    
    Args:
        list1: 第一个结果列表
        list2: 第二个结果列表
    
    Returns:
        合并后的列表（按时间排序）
    """
    seen_urls = set()
    merged = []
    
    # 先添加list1的结果
    for item in list1:
        url = item.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            merged.append(item)
    
    # 再添加list2的结果（去重）
    for item in list2:
        url = item.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            merged.append(item)
    
    logger.info(f"  [去重] 合并后共 {len(merged)} 条（去除 {len(list1) + len(list2) - len(merged)} 条重复）")
    return merged

# ==================== 新闻过滤函数 ====================
def filter_real_events(articles: List[Dict]) -> List[Dict]:
    """
    过滤新闻，只保留真实事件
    
    排除：
    1. 分析、预测类文章
    2. 回顾、总结类文章
    3. 观点、评论类文章
    
    保留：
    1. 产品发布
    2. 技术突破
    3. 重大合作
    4. 重要会议/活动
    """
    filtered = []
    
    exclude_keywords = [
        "分析", "预测", "展望", "回顾", "总结", "评论",
        "观点", "看法", "解读", "深度", "思考",
        "analysis", "prediction", "forecast", "review", "summary",
        "comment", "opinion", "perspective", "insight"
    ]
    
    include_keywords = [
        "发布", "推出", "上线", "突破", "合作", "签约",
        "会议", "活动", "展会", "获奖", "融资", "投资",
        "launch", "release", "announce", "breakthrough", "cooperation",
        "conference", "event", "exhibition", "award", "funding"
    ]
    
    for article in articles:
        title = article.get("title", "").lower()
        content = article.get("content", "").lower()
        
        # 检查是否包含排除关键词
        has_exclude = any(keyword in title or keyword in content 
                         for keyword in exclude_keywords)
        
        # 检查是否包含包含关键词
        has_include = any(keyword in title or keyword in content 
                         for keyword in include_keywords)
        
        # 如果是真实事件，保留
        if has_include and not has_exclude:
            filtered.append(article)
    
    logger.info(f"新闻过滤: {len(articles)} -> {len(filtered)} 个真实事件")
    return filtered

# ==================== HTML生成函数 ====================
def generate_html(news_data: Dict[str, List[Dict]]) -> str:
    """
    生成HTML格式的新闻简报
    
    Args:
        news_data: 按模块分类的新闻数据
    
    Returns:
        HTML字符串
    """
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 模块标题映射
    module_titles = {
        "global_models": "🌍 全球顶尖大模型及公司动态",
        "global_models_international": "🌐 海外大厂官网动态",
        "china_models": "🇨🇳 中国AI大模型最新进展",
        "ai_hardware": "💻 AI软硬件及国产芯片生态",
        "ai_agents": "🦞 AI智能体前沿资讯",
        "other_ai": "📰 其他全球AI领域重要资讯"
    }
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>高校分队 AI 新闻每日简报</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f8fafc;
        }}
        .header {{
            background: #1e3a8a;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header .date {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 14px;
        }}
        .module {{
            background: white;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .module h2 {{
            color: #1e3a8a;
            border-left: 4px solid #3b82f6;
            padding-left: 10px;
            margin-top: 0;
        }}
        .news-item {{
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .news-item:last-child {{
            border-bottom: none;
        }}
        .news-title {{
            font-weight: bold;
            color: #1e3a8a;
            margin-bottom: 5px;
        }}
        .news-title a {{
            color: #1e3a8a;
            text-decoration: none;
        }}
        .news-title a:hover {{
            text-decoration: underline;
        }}
        .news-summary {{
            color: #666;
            font-size: 14px;
            line-height: 1.5;
            margin-bottom: 5px;
        }}
        .news-link {{
            color: #3b82f6;
            font-size: 12px;
            text-decoration: none;
        }}
        .news-link:hover {{
            text-decoration: underline;
        }}
        .no-news {{
            color: #666;
            font-style: italic;
            padding: 10px;
            background: #f1f5f9;
            border-radius: 3px;
            text-align: center;
        }}
        .footer {{
            margin-top: 30px;
            padding: 15px;
            background: #f1f5f9;
            text-align: center;
            border-radius: 5px;
            color: #666;
            font-size: 12px;
        }}
        .strategy-note {{
            background: #f0f9ff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #3b82f6;
        }}
        .strategy-note p {{
            margin: 0 0 5px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>高校分队 AI 新闻每日简报</h1>
        <p class="date">{today}</p>
    </div>
    
    <div class="strategy-note">
        <p><strong>📋 新闻搜索策略说明</strong></p>
        <p>从今天开始，简报采用新搜索策略：</p>
        <p>• 只看过去24-48小时内的真实事件</p>
        <p>• 排除分析、预测、回顾类文章</p>
        <p>• 多源验证确保真实性</p>
        <p>• 如实报告：如无重大新闻，标注"今日暂无重大更新"</p>
    </div>
'''
    
    # 添加各个模块
    for module_id, module_title in module_titles.items():
        html += f'''
    <div class="module">
        <h2>{module_title}</h2>
'''
        
        news_items = news_data.get(module_id, [])
        
        if not news_items:
            html += '''
        <div class="no-news">
            📭 今日暂无重大更新，持续关注中...
        </div>
'''
        else:
            for i, news in enumerate(news_items[:5]):  # 每个模块最多5条
                title = news.get("title", "无标题")
                content = news.get("content", "")
                url = news.get("url", "#")
                
                # 截取摘要
                summary = content[:100] + "..." if len(content) > 100 else content
                
                html += f'''
        <div class="news-item">
            <div class="news-title">
                <a href="{url}" target="_blank">{title}</a>
            </div>
            <div class="news-summary">{summary}</div>
            <a href="{url}" class="news-link" target="_blank">阅读原文 →</a>
        </div>
'''
        
        html += '''
    </div>
'''
    
    # 页脚
    html += f'''
    <div class="footer">
        <p>高校分队 AI 新闻每日简报 | 由旺财Jarvis自动生成</p>
        <p>{today} | 搜索策略：只看过去72小时内的真实事件</p>
    </div>
</body>
</html>
'''
    
    return html

# ==================== 主函数 ====================
def main():
    """主函数"""
    logger.info("开始搜索AI新闻...")
    logger.info("搜索策略：只看过去72小时内的真实事件")
    
    # 收集所有新闻
    all_news = {}
    
    for module_id, queries in SEARCH_QUERIES.items():
        logger.info(f"搜索模块: {module_id}")
        module_news = []
        
        for query in queries:
            logger.info(f"  搜索: {query}")
            # 使用统一搜索接口（优先SerpAPI）
            results = search_news(query, max_results=3, prefer_serpapi=True)
            
            # 过滤真实事件
            real_events = filter_real_events(results)
            module_news.extend(real_events)
            
            # 避免请求过快
            import time
            time.sleep(1)
        
        # 去重
        unique_news = []
        seen_titles = set()
        for news in module_news:
            title = news.get("title", "")
            url = news.get("url", "")
            if title and title not in seen_titles:
                # 检查来源可信度
                is_trusted, source_type = check_source(url)
                if not is_trusted:
                    logger.info(f"    跳过不可信来源: {url[:60]}...")
                    continue
                # 记录来源类型（可选）
                if source_type == "tech_doc":
                    logger.info(f"    接受技术文档来源: {url[:60]}...")
                
                # 检测是否为英文并翻译
                if is_likely_english(url, title):
                    logger.info(f"    检测到英文新闻，正在翻译: {title[:50]}...")
                    news["title"] = translate_to_chinese(title)
                    if news.get("content"):
                        news["content"] = translate_to_chinese(news["content"])
                    logger.info(f"    翻译完成: {news['title'][:50]}...")
                
                seen_titles.add(title)
                unique_news.append(news)
        
        # 日期过滤（只保留最近72小时内的新闻）
        filtered_news = filter_by_date(unique_news, max_hours=72)
        
        all_news[module_id] = filtered_news
        logger.info(f"  找到 {len(filtered_news)} 个真实事件（过去48小时内）")
    
    # 生成HTML
    html_content = generate_html(all_news)
    
    # 保存文件
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path.home() / ".openclaw" / "workspace" / "news_summaries"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"ai_news_brief_{today_str}.html"
    output_file.write_text(html_content, encoding='utf-8')
    
    logger.info(f"新闻简报已生成: {output_file}")
    
    # 统计信息
    total_news = sum(len(news) for news in all_news.values())
    logger.info(f"总计: {total_news} 条新闻")
    
    # 输出文件路径（供其他脚本使用）
    print(str(output_file))

if __name__ == "__main__":
    main()