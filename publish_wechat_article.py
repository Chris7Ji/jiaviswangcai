#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章发布脚本
"""

import os
import json
import requests
import time
from datetime import datetime

class WeChatPublisher:
    """微信公众号发布器"""
    
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self):
        """获取access_token"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "access_token" in data:
                self.access_token = data["access_token"]
                self.token_expires_at = time.time() + data.get("expires_in", 7200) - 300
                print(f"✅ Access Token获取成功")
                return self.access_token
            else:
                error_msg = data.get('errmsg', '未知错误')
                error_code = data.get('errcode', '未知')
                print(f"❌ 获取Token失败: {error_msg} (错误码: {error_code})")
                return None
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return None
    
    def create_draft(self, title, content, author="季", digest=None, show_cover_pic=1):
        """创建草稿"""
        token = self.get_access_token()
        if not token:
            return None
            
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {"access_token": token}
        
        # 准备文章数据
        article = {
            "title": title,
            "author": author,
            "digest": digest or f"{title} - AI助手能力进化分享",
            "content": content,
            "content_source_url": "",
            "show_cover_pic": show_cover_pic,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }
        
        payload = {
            "articles": [article]
        }
        
        try:
            response = requests.post(url, params=params, json=payload, timeout=15)
            data = response.json()
            
            if data.get("errcode") == 0:
                media_id = data.get("media_id")
                print(f"✅ 草稿创建成功")
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
    
    def upload_image(self, image_path):
        """上传图片到微信服务器"""
        token = self.get_access_token()
        if not token:
            return None
            
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        params = {"access_token": token}
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, params=params, files=files, timeout=15)
                data = response.json()
                
                if "url" in data:
                    image_url = data["url"]
                    print(f"✅ 图片上传成功")
                    print(f"   图片URL: {image_url}")
                    return image_url
                else:
                    error_msg = data.get('errmsg', '未知错误')
                    print(f"❌ 图片上传失败: {error_msg}")
                    return None
                    
        except FileNotFoundError:
            print(f"❌ 图片文件不存在: {image_path}")
            return None
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return None

def load_config():
    """加载配置"""
    config_path = "/Users/jiyingguo/.openclaw/workspace/wechat_config.json"
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return {}

def load_article_content():
    """加载文章内容"""
    html_file = "/Users/jiyingguo/.openclaw/workspace/公众号文章_微信公众号格式.html"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文章失败: {e}")
        return None

def main():
    """主函数"""
    print("🚀 微信公众号文章发布工具")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    app_id = config.get("app_id")
    app_secret = config.get("app_secret")
    
    if not app_id or not app_secret:
        print("❌ 配置不完整：缺少AppID或AppSecret")
        print("   请先运行 wechat_publisher.py 进行配置")
        return
    
    print(f"✅ 配置加载成功")
    print(f"   AppID: {app_id[:8]}...{app_id[-4:]}")
    
    # 创建发布器
    publisher = WeChatPublisher(app_id, app_secret)
    
    # 测试API连接
    print("\n🔍 测试API连接...")
    token = publisher.get_access_token()
    
    if not token:
        print("❌ API连接失败，请检查：")
        print("   1. IP白名单是否配置正确")
        print("   2. AppID和AppSecret是否正确")
        print("   3. 公众号是否已认证")
        return
    
    print("✅ API连接测试成功")
    
    # 加载文章内容
    print("\n📝 加载文章内容...")
    article_content = load_article_content()
    
    if not article_content:
        print("❌ 文章内容加载失败")
        return
    
    # 文章信息
    title = "我的AI助手旺财：三天时间构建的四大能力体系"
    author = "季"
    digest = "我的AI助手旺财如何在三天时间里，从一个基础助手进化成拥有四大专业能力的智能伙伴。分享从零到一的AI助手构建经验和技术实现细节。"
    
    print(f"✅ 文章内容加载成功")
    print(f"   标题: {title}")
    print(f"   作者: {author}")
    print(f"   摘要: {digest[:50]}...")
    
    # 创建草稿
    print("\n📄 创建微信公众号草稿...")
    media_id = publisher.create_draft(title, article_content, author, digest)
    
    if media_id:
        print("\n" + "=" * 60)
        print("🎉 草稿创建成功！")
        print("\n📋 下一步操作:")
        print("1. 登录微信公众平台: https://mp.weixin.qq.com/")
        print("2. 进入'素材管理' → '草稿箱'")
        print("3. 找到刚创建的草稿")
        print("4. 添加封面图片（可选）")
        print("5. 点击'群发'确认发布")
        print("\n⏰ 发布建议:")
        print("   - 最佳时间: 工作日 18:00-22:00")
        print("   - 周末时间: 10:00-12:00 或 20:00-22:00")
        print("   - 避开节假日和重大事件")
        
        # 保存发布信息
        publish_info = {
            "title": title,
            "media_id": media_id,
            "author": author,
            "created_at": datetime.now().isoformat(),
            "status": "draft_created",
            "next_steps": [
                "登录公众号后台确认草稿",
                "添加封面图片",
                "设置原创声明（可选）",
                "确认发布"
            ]
        }
        
        info_file = "/Users/jiyingguo/.openclaw/workspace/publish_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(publish_info, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 发布信息已保存: {info_file}")
    else:
        print("\n❌ 草稿创建失败")
        print("\n🔧 故障排除:")
        print("1. 检查文章内容是否包含违规元素")
        print("2. 简化HTML格式，移除复杂样式")
        print("3. 确保文章长度适中（正文不超过2万字）")
        print("4. 检查网络连接和API权限")

if __name__ == "__main__":
    main()