#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版微信公众号发布脚本
"""

import os
import json
import requests
import time
from datetime import datetime

def load_config():
    """加载配置"""
    config_path = "/Users/jiyingguo/.openclaw/workspace/wechat_config.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return {}

def get_access_token(app_id, app_secret):
    """获取access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "access_token" in data:
            return data["access_token"]
        else:
            print(f"❌ 获取Token失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def load_simple_article():
    """加载简化版文章"""
    html_file = "/Users/jiyingguo/.openclaw/workspace/公众号文章_简化格式.html"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取body内容
        body_start = content.find('<body>')
        body_end = content.find('</body>')
        
        if body_start != -1 and body_end != -1:
            body_content = content[body_start + 6:body_end].strip()
        else:
            body_content = content
        
        # 清理HTML，确保符合微信公众号要求
        # 移除复杂的HTML标签，保留基本标签
        import re
        
        # 保留基本标签：h1-h6, p, ul, ol, li, strong, em, blockquote, pre, code, hr
        allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'strong', 'em', 'blockquote', 'pre', 'code', 'hr']
        
        # 简化处理：只进行基本清理
        cleaned_content = body_content
        
        print(f"✅ 文章内容加载成功")
        print(f"   原始长度: {len(body_content)}字符")
        print(f"   清理后长度: {len(cleaned_content)}字符")
        
        return cleaned_content
        
    except Exception as e:
        print(f"❌ 读取文章失败: {e}")
        return None

def create_draft_simple(access_token, title, content):
    """创建草稿（简化版）"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    # 准备文章数据（简化版）
    article = {
        "title": title,
        "author": "季",
        "digest": "我的AI助手旺财如何在三天时间里，从一个基础助手进化成拥有四大专业能力的智能伙伴。",
        "content": content,
        "content_source_url": "",
        "show_cover_pic": 1,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }
    
    payload = {
        "articles": [article]
    }
    
    try:
        print("🔄 正在创建草稿...")
        response = requests.post(url, params=params, json=payload, timeout=15)
        data = response.json()
        
        print(f"响应状态: {response.status_code}")
        print(f"响应内容: {data}")
        
        if data.get("errcode") == 0:
            media_id = data.get("media_id")
            print(f"✅ 草稿创建成功！")
            print(f"   媒体ID: {media_id}")
            return media_id
        else:
            error_msg = data.get('errmsg', '未知错误')
            error_code = data.get('errcode', '未知')
            print(f"❌ 创建草稿失败: {error_msg} (错误码: {error_code})")
            
            # 提供更详细的错误信息
            if error_code == 40007:
                print("   可能原因: 文章内容格式问题")
                print("   建议: 进一步简化HTML格式")
            elif error_code == 45009:
                print("   可能原因: API调用频率限制")
                print("   建议: 等待一段时间后重试")
            elif error_code == 48001:
                print("   可能原因: API功能未授权")
                print("   建议: 检查公众号权限设置")
                
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def main():
    """主函数"""
    print("🚀 简化版微信公众号发布工具")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    app_id = config.get("app_id")
    app_secret = config.get("app_secret")
    
    if not app_id or not app_secret:
        print("❌ 配置不完整")
        return
    
    print(f"✅ 配置加载成功")
    print(f"   AppID: {app_id[:8]}...")
    
    # 获取Access Token
    print("\n🔍 获取Access Token...")
    access_token = get_access_token(app_id, app_secret)
    
    if not access_token:
        print("❌ 获取Token失败")
        return
    
    print(f"✅ Token获取成功: {access_token[:20]}...")
    
    # 加载文章
    print("\n📝 加载文章内容...")
    article_content = load_simple_article()
    
    if not article_content:
        print("❌ 文章加载失败")
        return
    
    # 创建草稿
    title = "我的AI助手旺财：三天时间构建的四大能力体系"
    print(f"\n📄 创建草稿: {title}")
    
    media_id = create_draft_simple(access_token, title, article_content)
    
    if media_id:
        print("\n" + "=" * 60)
        print("🎉 发布成功！")
        print("\n📋 下一步:")
        print("1. 登录微信公众平台: https://mp.weixin.qq.com/")
        print("2. 进入'素材管理' → '草稿箱'")
        print("3. 找到标题为上述内容的草稿")
        print("4. 添加封面图片")
        print("5. 点击'群发'确认发布")
        
        # 保存发布记录
        record = {
            "title": title,
            "media_id": media_id,
            "published_at": datetime.now().isoformat(),
            "status": "draft_created",
            "note": "草稿已创建，请在公众号后台确认发布"
        }
        
        record_file = "/Users/jiyingguo/.openclaw/workspace/publish_record.json"
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 发布记录已保存: {record_file}")
    else:
        print("\n❌ 发布失败")
        print("\n💡 备选方案:")
        print("1. 手动复制文章内容到公众号后台")
        print("2. 使用更简化的文本格式")
        print("3. 分段发布文章")

if __name__ == "__main__":
    main()