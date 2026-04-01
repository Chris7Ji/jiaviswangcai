#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tavily搜索脚本 - 用于OpenClaw新闻监控
"""

import sys
import os
import json
from datetime import datetime, timedelta

# 激活虚拟环境
venv_path = "/Users/jiyingguo/.openclaw/workspace/venv_tavily"
activate_script = os.path.join(venv_path, "bin", "activate_this.py")

if os.path.exists(activate_script):
    exec(open(activate_script).read(), {'__file__': activate_script})

from tavily import TavilyClient

# API密钥
API_KEY = "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"

def search_openclaw_news(query, search_depth="advanced", max_results=10, include_domains=None):
    """搜索OpenClaw相关新闻"""
    
    client = TavilyClient(api_key=API_KEY)
    
    search_params = {
        "query": query,
        "search_depth": search_depth,
        "max_results": max_results,
        "include_answer": True,
        "include_raw_content": False,
    }
    
    if include_domains:
        search_params["include_domains"] = include_domains
    
    try:
        response = client.search(**search_params)
        return response
    except Exception as e:
        print(f"搜索错误: {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) < 2:
        print("用法: python tavily_search.py '<搜索关键词>' [中文|英文]")
        sys.exit(1)
    
    query = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "中文"
    
    # 根据语言设置优先域名
    if lang == "中文":
        include_domains = [
            "github.com",
            "juejin.cn",
            "csdn.net",
            "zhihu.com",
            "v2ex.com",
            "oschina.net"
        ]
    else:
        include_domains = [
            "github.com",
            "news.ycombinator.com",
            "reddit.com",
            "openclaw.ai",
            "docs.openclaw.ai"
        ]
    
    print(f"正在搜索: {query}")
    print(f"语言: {lang}")
    print("-" * 50)
    
    result = search_openclaw_news(query, include_domains=include_domains)
    
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("搜索失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
