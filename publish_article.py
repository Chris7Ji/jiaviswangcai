#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布OpenClaw文章到微信公众号
"""

import os
import sys
import json
from wechat_publisher import WeChatOfficialAccount

def load_article():
    """加载文章文件"""
    article_path = os.path.expanduser("~/.openclaw/workspace/wechat_article_openclaw.md")
    
    if not os.path.exists(article_path):
        print(f"❌ 文章文件不存在: {article_path}")
        return None
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content


def load_config():
    """加载微信配置"""
    config_path = os.path.expanduser("~/.openclaw/workspace/wechat_config.json")
    
    if not os.path.exists(config_path):
        print(f"❌ 配置文件不存在，请先运行: python3 wechat_publisher.py")
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def markdown_to_html(markdown_text):
    """
    简单的Markdown转HTML
    微信公众号支持有限的HTML标签
    """
    import re
    
    html = markdown_text
    
    # 处理标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 处理粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 处理斜体
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 处理段落
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        
        # 如果已经是HTML标签，不再包裹
        if p.startswith('<h') or p.startswith('<') and p.endswith('>'):
            html_paragraphs.append(p)
        else:
            # 处理换行
            p = p.replace('\n', '<br>')
            html_paragraphs.append(f'<p>{p}</p>')
    
    return '\n'.join(html_paragraphs)


def extract_title_and_content(article_text):
    """从文章中提取标题和正文"""
    lines = article_text.split('\n')
    
    title = ""
    content_lines = []
    
    # 查找主标题（通常是第一个#开头的行）
    for i, line in enumerate(lines):
        if line.startswith('# ') and not title:
            title = line.replace('# ', '').strip()
            content_lines = lines[i+1:]
            break
    
    if not title:
        # 如果没有找到，使用默认标题
        title = "OpenClaw：重新定义AI助手"
        content_lines = lines
    
    # 清理内容
    # 移除备选标题部分
    cleaned_lines = []
    skip_until = 0
    
    for i, line in enumerate(content_lines):
        if i < skip_until:
            continue
        
        # 跳过"备选标题"部分
        if '备选标题' in line:
            # 跳过接下来的几行（通常是3个标题）
            skip_until = i + 4
            continue
        
        # 跳过"配图建议"表格
        if '| 章节 | 配图建议 |' in line:
            # 跳过整个表格
            skip_until = i + 10
            continue
        
        # 跳过摘要部分
        if line.startswith('## 摘要'):
            skip_until = i + 3
            continue
        
        cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    return title, content


def main():
    """主函数"""
    print("=" * 60)
    print("发布文章到微信公众号")
    print("=" * 60)
    
    # 加载配置
    print("\n📋 加载配置...")
    config = load_config()
    if not config:
        return False
    
    # 加载文章
    print("📄 加载文章...")
    article_text = load_article()
    if not article_text:
        return False
    
    # 提取标题和内容
    print("✂️  处理文章内容...")
    title, content = extract_title_and_content(article_text)
    
    print(f"\n📝 文章信息:")
    print(f"   标题: {title}")
    print(f"   字数: {len(content)} 字符")
    
    # 转换为HTML
    print("🔄 转换为HTML格式...")
    html_content = markdown_to_html(content)
    
    # 创建微信客户端
    print("\n🔗 连接微信公众号API...")
    wechat = WeChatOfficialAccount(config["app_id"], config["app_secret"])
    
    # 测试连接
    token = wechat.get_access_token()
    if not token:
        print("❌ 连接失败，请检查配置")
        return False
    
    print("\n💡 准备发布:")
    print("   由于微信公众号API限制，我们需要:")
    print("   1. 先创建草稿")
    print("   2. 您在微信公众平台确认")
    print("   3. 正式发布")
    
    # 自动确认创建草稿
    print("\n✅ 自动创建草稿...")
    choice = 'y'
    
    # 创建草稿
    print("\n📝 创建草稿...")
    
    # 构建文章数据
    articles = [{
        "title": title,
        "content": html_content,
        "author": "季",
        "digest": "一个开源AI助手项目，三个月斩获30万Star。它凭什么让开发者疯狂？本文揭秘OpenClaw的崛起之路。",
        "show_cover_pic": 0,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]
    
    import requests
    access_token = wechat.get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    try:
        response = requests.post(url, json={"articles": articles}, timeout=30)
        result = response.json()
        
        if "media_id" in result:
            media_id = result["media_id"]
            print(f"\n✅ 草稿创建成功！")
            print(f"   Media ID: {media_id}")
            print(f"\n📱 下一步:")
            print(f'   1. 登录微信公众平台: https://mp.weixin.qq.com/')
            print(f'   2. 进入"内容与互动" → "草稿箱"')
            print(f'   3. 找到草稿: {title}')
            print(f'   4. 编辑封面图片，确认无误后发布')
            return True
        else:
            print(f"❌ 草稿创建失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False
    
    if media_id:
        print(f"\n✅ 草稿创建成功！")
        print(f"   Media ID: {media_id}")
        print(f"\n📱 下一步:")
        print(f"   1. 登录微信公众平台: https://mp.weixin.qq.com/")
        print(f'   2. 进入"内容与互动" → "草稿箱"')
        print(f"   3. 找到草稿: {title}")
        print(f"   4. 编辑封面图片，确认无误后发布")
        
        # 保存发布信息
        publish_info = {
            "media_id": media_id,
            "title": title,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        info_path = os.path.expanduser("~/.openclaw/workspace/publish_info.json")
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(publish_info, f, ensure_ascii=False, indent=2)
        
        return True
    else:
        print("❌ 草稿创建失败")
        return False


if __name__ == "__main__":
    import time
    success = main()
    sys.exit(0 if success else 1)