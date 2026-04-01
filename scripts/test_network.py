#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络连接诊断脚本
用于测试 SerpAPI 和 Tavily API 的网络连通性
"""

import sys
import os
import json

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_serpapi():
    """测试 SerpAPI 连接"""
    print("=" * 60)
    print("测试 1: SerpAPI 连接")
    print("=" * 60)
    
    SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f")
    
    try:
        import urllib.parse
        import requests
        
        query = "AI news today"
        url = f"https://serpapi.com/search?q={urllib.parse.quote(query)}&api_key={SERPAPI_KEY}&num=1"
        
        print(f"  请求URL: {url[:80]}...")
        print(f"  超时设置: 30秒")
        
        response = requests.get(url, timeout=30)
        print(f"  响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("organic_results", [])
            print(f"  ✅ SerpAPI 连接成功! 找到 {len(results)} 条结果")
            return True
        else:
            print(f"  ❌ SerpAPI 返回错误状态: {response.status_code}")
            print(f"  响应内容: {response.text[:200]}")
            return False
            
    except ImportError as e:
        print(f"  ❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"  ❌ SerpAPI 连接失败: {type(e).__name__}: {e}")
        return False

def test_tavily():
    """测试 Tavily API 连接"""
    print("\n" + "=" * 60)
    print("测试 2: Tavily API 连接")
    print("=" * 60)
    
    TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "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")
    
    try:
        import requests
        
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": "AI news today",
            "max_results": 1,
        }
        
        headers = {"Content-Type": "application/json"}
        
        print(f"  请求URL: {url}")
        print(f"  超时设置: 30秒")
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"  响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            print(f"  ✅ Tavily 连接成功! 找到 {len(results)} 条结果")
            return True
        else:
            print(f"  ❌ Tavily 返回错误状态: {response.status_code}")
            print(f"  响应内容: {response.text[:200]}")
            return False
            
    except ImportError as e:
        print(f"  ❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Tavily 连接失败: {type(e).__name__}: {e}")
        return False

def test_dns():
    """测试 DNS 解析"""
    print("\n" + "=" * 60)
    print("测试 3: DNS 解析测试")
    print("=" * 60)
    
    hosts_to_test = [
        ("serpapi.com", "SerpAPI"),
        ("api.tavily.com", "Tavily"),
        ("api.deepseek.com", "DeepSeek"),
    ]
    
    import socket
    
    for host, name in hosts_to_test:
        try:
            ip = socket.gethostbyname(host)
            print(f"  ✅ {name} ({host}) -> {ip}")
        except socket.gaierror as e:
            print(f"  ❌ {name} ({host}) DNS解析失败: {e}")
        except Exception as e:
            print(f"  ❌ {name} ({host}) 错误: {e}")

def test_ssl():
    """测试 SSL 证书"""
    print("\n" + "=" * 60)
    print("测试 4: SSL 证书验证")
    print("=" * 60)
    
    import ssl
    import socket
    import certifi
    
    print(f"  certifi 路径: {certifi.where()}")
    print(f"  SSL 默认上下文: {ssl.create_default_context()}")
    
    # 测试 HTTPS 连接
    test_hosts = [
        ("serpapi.com", 443),
        ("api.tavily.com", 443),
    ]
    
    for host, port in test_hosts:
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            with socket.create_connection((host, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    print(f"  ✅ {host} SSL 连接成功")
        except Exception as e:
            print(f"  ❌ {host} SSL 连接失败: {type(e).__name__}: {e}")

def main():
    print("\n" + "=" * 60)
    print("AI 新闻搜索 - 网络连接诊断工具")
    print("=" * 60)
    print()
    
    test_dns()
    test_ssl()
    
    serpapi_ok = test_serpapi()
    tavily_ok = test_tavily()
    
    print("\n" + "=" * 60)
    print("诊断总结")
    print("=" * 60)
    print(f"  SerpAPI: {'✅ 正常' if serpapi_ok else '❌ 失败'}")
    print(f"  Tavily:  {'✅ 正常' if tavily_ok else '❌ 失败'}")
    
    if not serpapi_ok and not tavily_ok:
        print("\n⚠️  两个API都连接失败，可能是网络环境问题")
        print("   - 检查 cron 任务的执行环境")
        print("   - 检查代理设置")
        print("   - 检查防火墙规则")
    elif not serpapi_ok:
        print("\n⚠️  SerpAPI 连接失败，可能需要检查网络或API配额")
    elif not tavily_ok:
        print("\n⚠️  Tavily 连接失败，可能超过配额限制")
    
    return 0 if (serpapi_ok or tavily_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
