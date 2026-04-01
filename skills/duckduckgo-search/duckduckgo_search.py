#!/usr/bin/env python3
"""
DuckDuckGo 搜索工具 - 使用网页抓取方式
无需API Key，无需安装额外包
"""

import sys
import json
import urllib.request
import urllib.parse
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """提取HTML中的文本内容"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style', 'nav', 'footer']:
            self.skip = True
            
    def handle_endtag(self, tag):
        if tag in ['script', 'style', 'nav', 'footer']:
            self.skip = False
            
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)
            
    def get_text(self):
        return ' '.join(self.text)

def search_duckduckgo_simple(query, max_results=10):
    """
    使用DuckDuckGo HTML搜索
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数量
    
    Returns:
        list: 搜索结果列表
    """
    try:
        # 构建搜索URL
        encoded_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        
        # 解析搜索结果
        results = []
        
        # 提取搜索结果
        # DuckDuckGo HTML版本的搜索结果结构
        result_blocks = re.findall(
            r'<div class="result[^"]*"[^>]*>.*?<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?<a[^>]*class="result__url"[^>]*href="[^"]*"[^>]*>(.*?)</a>.*?<div class="result__snippet"[^>]*>(.*?)</div>.*?</div>',
            html, re.DOTALL
        )
        
        for i, (href, title, display_url, snippet) in enumerate(result_blocks[:max_results]):
            # 清理HTML标签
            title = re.sub(r'<[^>]+>', '', title)
            snippet = re.sub(r'<[^>]+>', '', snippet)
            display_url = re.sub(r'<[^>]+>', '', display_url)
            
            # 处理重定向URL
            if href.startswith('/'):
                href = 'https://duckduckgo.com' + href
            
            results.append({
                'title': title.strip(),
                'href': href.strip(),
                'url': display_url.strip(),
                'body': snippet.strip()
            })
        
        return results
        
    except Exception as e:
        print(f"搜索出错: {e}")
        return []

def format_results(results):
    """格式化搜索结果"""
    if not results:
        return "未找到结果"
    
    output = []
    for i, r in enumerate(results, 1):
        title = r.get('title', '无标题')
        href = r.get('href', '')
        body = r.get('body', '')[:200]
        
        output.append(f"{i}. {title}")
        output.append(f"   URL: {href}")
        output.append(f"   {body}...")
        output.append("")
    
    return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 duckduckgo_search.py <搜索关键词>")
        print("示例: python3 duckduckgo_search.py 'OpenClaw 最新版本'")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    print(f"🔍 搜索: {query}")
    print("=" * 50)
    
    results = search_duckduckgo_simple(query)
    
    if results:
        print(format_results(results))
        
        # 同时输出JSON格式供程序使用
        print("\n" + "=" * 50)
        print("JSON格式输出:")
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("搜索失败或未找到结果")
        sys.exit(1)

if __name__ == "__main__":
    main()
