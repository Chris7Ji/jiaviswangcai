#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试Tavily API密钥
"""

import requests
import json

def test_key_directly(api_key):
    """直接测试Tavily API密钥"""
    print(f"测试密钥: {api_key}")
    print(f"密钥长度: {len(api_key)}")
    print(f"密钥前缀: {api_key[:9] if len(api_key) >= 9 else '太短'}")
    
    if len(api_key) >= 9:
        key_part = api_key[9:]
        print(f"密钥部分: {key_part}")
        print(f"密钥部分长度: {len(key_part)}")
        
        # 检查字符
        print("字符分析:")
        for i, char in enumerate(key_part):
            if char.isdigit():
                print(f"  位置{i}: '{char}' - 数字")
            elif 'a' <= char <= 'f':
                print(f"  位置{i}: '{char}' - 小写十六进制")
            elif 'A' <= char <= 'F':
                print(f"  位置{i}: '{char}' - 大写十六进制（应该小写）")
            elif 'g' <= char <= 'z' or 'G' <= char <= 'Z':
                print(f"  位置{i}: '{char}' - 非十六进制字母（无效）")
            else:
                print(f"  位置{i}: '{char}' - 特殊字符（无效）")
    
    # 测试API
    print("\n测试API连接...")
    url = "https://api.tavily.com/search"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "query": "test",
        "max_results": 1,
        "include_answer": False
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API连接成功！密钥有效！")
            return True
        elif response.status_code == 401:
            print("❌ 401未授权：密钥无效或格式错误")
            print(f"响应: {response.text[:200]}")
        elif response.status_code == 403:
            print("❌ 403禁止访问：密钥可能已过期或限制使用")
        else:
            print(f"❌ 错误: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
    
    return False

def main():
    """主函数"""
    # 用户提供的密钥
    original_key = "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"
    
    print("=" * 60)
    print("🔧 Tavily API密钥调试")
    print("=" * 60)
    
    print("\n1. 测试原始密钥:")
    test_key_directly(original_key)
    
    print("\n" + "=" * 60)
    print("\n2. 尝试修正版本:")
    
    # 可能的修正
    corrections = [
        ("全小写", "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"),
        ("数字1替代l", "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"),
        ("修正常见OCR错误", "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"),
        ("尝试不同组合", "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"),
    ]
    
    for name, key in corrections:
        print(f"\n尝试: {name}")
        print(f"密钥: {key}")
        if test_key_directly(key):
            print(f"🎉 找到有效密钥: {key}")
            break
    
    print("\n" + "=" * 60)
    print("💡 建议:")
    print("1. 请确认密钥完全正确（区分大小写）")
    print("2. 检查密钥是否已过期")
    print("3. 访问 https://tavily.com/ 查看密钥状态")
    print("4. 可能需要生成新的API密钥")

if __name__ == "__main__":
    main()