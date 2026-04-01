#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tavily API密钥测试脚本
测试密钥格式和有效性
"""

import re
import requests
import sys

def validate_tavily_key_format(api_key):
    """验证Tavily API密钥格式"""
    # Tavily密钥格式: tvly-dev-后面跟着32个十六进制字符
    pattern = r'^tvly-dev-[a-fA-F0-9]{32}$'
    
    if re.match(pattern, api_key):
        return {
            "valid": True,
            "length": len(api_key),
            "expected_length": 41,
            "prefix": api_key[:9],
            "key_part": api_key[9:],
            "key_part_length": len(api_key[9:]),
            "message": "✅ 密钥格式正确"
        }
    else:
        # 分析问题
        issues = []
        
        # 检查前缀
        if not api_key.startswith('tvly-dev-'):
            issues.append(f"前缀错误: 应以'tvly-dev-'开头，实际是'{api_key[:min(9, len(api_key))]}'")
        
        # 检查总长度
        expected_length = 41
        actual_length = len(api_key)
        if actual_length != expected_length:
            issues.append(f"长度错误: 应为{expected_length}字符，实际{actual_length}字符")
        
        # 检查密钥部分
        if api_key.startswith('tvly-dev-'):
            key_part = api_key[9:]
            if not re.match(r'^[a-fA-F0-9]*$', key_part):
                issues.append("密钥部分包含非十六进制字符")
            if len(key_part) != 32:
                issues.append(f"密钥部分应为32字符，实际{len(key_part)}字符")
        
        return {
            "valid": False,
            "length": actual_length,
            "expected_length": expected_length,
            "issues": issues,
            "message": "❌ 密钥格式错误"
        }

def test_tavily_api(api_key):
    """测试Tavily API连接"""
    try:
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
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "✅ API连接成功"
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": "❌ 认证失败：无效的API密钥"
            }
        elif response.status_code == 403:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": "❌ 权限不足：密钥可能已过期或限制访问"
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": f"❌ API错误：{response.status_code}",
                "response_text": response.text[:200]
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "❌ 连接超时"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": "❌ 连接错误：无法连接到Tavily API"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ 测试异常：{str(e)}"
        }

def suggest_corrections(api_key):
    """根据常见错误建议修正"""
    suggestions = []
    
    # 常见OCR识别错误
    common_ocr_errors = {
        '0': 'O', 'O': '0',
        '1': 'I', 'I': '1',
        '5': 'S', 'S': '5',
        '8': 'B', 'B': '8',
        '2': 'Z', 'Z': '2'
    }
    
    # 检查长度
    if len(api_key) < 41:
        missing = 41 - len(api_key)
        suggestions.append(f"密钥太短，缺失{missing}个字符")
    
    if len(api_key) > 41:
        extra = len(api_key) - 41
        suggestions.append(f"密钥太长，多出{extra}个字符")
    
    # 检查字符
    if api_key.startswith('tvly-dev-'):
        key_part = api_key[9:]
        for i, char in enumerate(key_part):
            if not char.isalnum():
                suggestions.append(f"位置{9+i+1}的字符'{char}'不是字母数字")
            elif char.isalpha() and char.isupper():
                # Tavily密钥通常是小写十六进制
                suggestions.append(f"位置{9+i+1}的字符'{char}'可能是小写")
    
    return suggestions

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python test_tavily_key.py <API密钥>")
        print("示例: python test_tavily_key.py tvly-dev-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    print("=" * 60)
    print("🔑 Tavily API密钥测试")
    print("=" * 60)
    print(f"密钥: {api_key}")
    print(f"长度: {len(api_key)} 字符")
    print("")
    
    # 1. 验证格式
    print("1. 验证密钥格式...")
    format_result = validate_tavily_key_format(api_key)
    
    if format_result["valid"]:
        print(format_result["message"])
        print(f"   长度: {format_result['length']}/{format_result['expected_length']}")
        print(f"   前缀: {format_result['prefix']}")
        print(f"   密钥部分: {format_result['key_part']} ({format_result['key_part_length']}字符)")
    else:
        print(format_result["message"])
        for issue in format_result.get("issues", []):
            print(f"   • {issue}")
    
    print("")
    
    # 2. 建议修正
    if not format_result["valid"]:
        print("2. 修正建议...")
        suggestions = suggest_corrections(api_key)
        if suggestions:
            for suggestion in suggestions:
                print(f"   • {suggestion}")
        else:
            print("   ✅ 无具体修正建议")
        
        print("")
        print("💡 常见OCR识别问题:")
        print("   • 数字0 vs 字母O")
        print("   • 数字1 vs 字母I")
        print("   • 数字5 vs 字母S")
        print("   • 数字8 vs 字母B")
        print("   • 字母大小写混淆")
    
    print("")
    
    # 3. 测试API连接（如果格式正确）
    if format_result["valid"]:
        print("3. 测试API连接...")
        api_result = test_tavily_api(api_key)
        print(api_result["message"])
        if not api_result["success"]:
            print(f"   状态码: {api_result.get('status_code', 'N/A')}")
            if 'response_text' in api_result:
                print(f"   响应: {api_result['response_text']}")
    else:
        print("3. 跳过API测试（格式不正确）")
    
    print("")
    print("=" * 60)
    print("📋 测试完成")
    print("=" * 60)
    
    # 总结
    if format_result["valid"]:
        print("✅ 密钥格式正确")
        # 如果有API测试结果
        if 'api_result' in locals() and api_result.get("success"):
            print("✅ API连接成功")
            print("🎉 密钥完全有效，可以配置使用!")
        elif 'api_result' in locals():
            print("⚠️  API连接失败，但格式正确")
            print("   可能是密钥已过期或网络问题")
        else:
            print("⚠️  未进行API测试")
    else:
        print("❌ 密钥格式错误，需要修正")
        print("💡 请检查原图片确认完整正确的密钥")

if __name__ == "__main__":
    main()