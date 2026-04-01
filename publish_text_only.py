#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯文本微信公众号发布脚本
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

def load_text_article():
    """加载纯文本文章"""
    text_file = "/Users/jiyingguo/.openclaw/workspace/公众号文章_纯文本.txt"
    
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ 纯文本文章加载成功")
        print(f"   字符数: {len(content)}")
        
        # 将纯文本转换为简单的HTML
        html_content = convert_text_to_simple_html(content)
        print(f"   HTML转换后: {len(html_content)}字符")
        
        return html_content
        
    except Exception as e:
        print(f"❌ 读取文章失败: {e}")
        return None

def convert_text_to_simple_html(text):
    """将纯文本转换为最简单的HTML"""
    # 基本转换：段落和换行
    lines = text.split('\n')
    html_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 判断标题
        if line.startswith('我的AI助手旺财：'):
            html_lines.append(f'<h1>{line}</h1>')
        elif line.startswith('一、') or line.startswith('二、') or line.startswith('三、') or line.startswith('四、') or line.startswith('五、') or line.startswith('六、') or line.startswith('七、') or line.startswith('八、'):
            html_lines.append(f'<h2>{line}</h2>')
        elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. ') or line.startswith('案例'):
            html_lines.append(f'<h3>{line}</h3>')
        elif line.startswith('🎯'):
            html_lines.append(f'<h4>{line}</h4>')
        elif line.startswith('- ') or line.startswith('❌') or line.startswith('✅'):
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith('"'):
            html_lines.append(f'<blockquote>{line}</blockquote>')
        elif line.startswith('---'):
            html_lines.append('<hr>')
        elif line.startswith('作者：') or line.startswith('时间：') or line.startswith('工具：'):
            html_lines.append(f'<p><strong>{line}</strong></p>')
        else:
            html_lines.append(f'<p>{line}</p>')
    
    # 添加基本HTML结构
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>我的AI助手旺财：三天时间构建的四大能力体系</title>
</head>
<body>
{''.join(html_lines)}
</body>
</html>"""
    
    return html

def create_draft_text_only(access_token, title, content):
    """创建草稿（纯文本版）"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    # 准备文章数据
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
        print("🔄 正在创建草稿（纯文本版）...")
        response = requests.post(url, params=params, json=payload, timeout=15)
        data = response.json()
        
        print(f"响应状态: {response.status_code}")
        
        if data.get("errcode") == 0:
            media_id = data.get("media_id")
            print(f"✅ 草稿创建成功！")
            print(f"   媒体ID: {media_id}")
            return media_id
        else:
            error_msg = data.get('errmsg', '未知错误')
            error_code = data.get('errcode', '未知')
            print(f"❌ 创建草稿失败: {error_msg} (错误码: {error_code})")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def main():
    """主函数"""
    print("🚀 纯文本微信公众号发布工具")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    app_id = config.get("app_id")
    app_secret = config.get("app_secret")
    
    if not app_id or not app_secret:
        print("❌ 配置不完整")
        return
    
    print(f"✅ 配置加载成功")
    
    # 获取Access Token
    print("\n🔍 获取Access Token...")
    access_token = get_access_token(app_id, app_secret)
    
    if not access_token:
        print("❌ 获取Token失败")
        return
    
    print(f"✅ Token获取成功")
    
    # 加载并转换文章
    print("\n📝 加载并转换文章...")
    article_content = load_text_article()
    
    if not article_content:
        print("❌ 文章加载失败")
        return
    
    # 创建草稿
    title = "我的AI助手旺财：三天时间构建的四大能力体系"
    print(f"\n📄 创建草稿: {title}")
    
    media_id = create_draft_text_only(access_token, title, article_content)
    
    if media_id:
        print("\n" + "=" * 60)
        print("🎉 发布成功！")
        print("\n📋 手动发布步骤:")
        print("1. 登录微信公众平台")
        print("2. 进入'素材管理' → '草稿箱'")
        print("3. 找到刚创建的草稿")
        print("4. 添加封面图片")
        print("5. 点击'群发'确认发布")
        
        # 保存成功记录
        success_file = "/Users/jiyingguo/.openclaw/workspace/publish_success.json"
        with open(success_file, 'w', encoding='utf-8') as f:
            json.dump({
                "title": title,
                "media_id": media_id,
                "time": datetime.now().isoformat(),
                "status": "draft_created"
            }, f, indent=2)
        
        print(f"\n✅ 发布记录: {success_file}")
    else:
        print("\n❌ 发布失败，使用备选方案")
        
        # 提供手动发布指南
        print("\n📋 手动发布指南:")
        print("1. 打开文件: 公众号文章_纯文本.txt")
        print("2. 复制全部内容")
        print("3. 登录微信公众平台")
        print("4. 新建图文素材，粘贴内容")
        print("5. 添加封面，设置摘要，发布")

if __name__ == "__main__":
    main()