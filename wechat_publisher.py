#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号API配置和文章发布工具
"""

import os
import json
import requests
import time
from datetime import datetime

class WeChatOfficialAccount:
    """微信公众号API客户端"""
    
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self):
        """获取access_token"""
        # 检查token是否过期
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
        url = f"https://api.weixin.qq.com/cgi-bin/token"
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
                # token有效期7200秒，提前300秒刷新
                self.token_expires_at = time.time() + data.get("expires_in", 7200) - 300
                print(f"✅ Access Token获取成功")
                return self.access_token
            else:
                print(f"❌ 获取Token失败: {data}")
                return None
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return None
    
    def upload_image(self, image_path):
        """上传图片到微信服务器，获取media_id"""
        access_token = self.get_access_token()
        if not access_token:
            return None
            
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        params = {"access_token": access_token}
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, params=params, files=files, timeout=30)
                data = response.json()
                
                if "url" in data:
                    print(f"✅ 图片上传成功: {data['url']}")
                    return data['url']
                else:
                    print(f"❌ 图片上传失败: {data}")
                    return None
                    
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return None
    
    def draft_article(self, title, content, thumb_media_id=None, author="", digest=""):
        """
        创建图文消息素材（草稿）
        
        Args:
            title: 标题
            content: 图文消息的具体内容，支持HTML标签
            thumb_media_id: 图文消息的封面图片素材id
            author: 作者
            digest: 图文消息的摘要，仅有单图文消息才有摘要，多图文此处为空
        """
        access_token = self.get_access_token()
        if not access_token:
            return None
            
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {"access_token": access_token}
        
        # 构造图文消息
        articles = [{
            "title": title,
            "content": content,
            "author": author,
            "digest": digest,
            "show_cover_pic": 1,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }]
        
        if thumb_media_id:
            articles[0]["thumb_media_id"] = thumb_media_id
            
        data = {"articles": articles}
        
        try:
            response = requests.post(
                url, 
                params=params, 
                json=data,
                timeout=30
            )
            result = response.json()
            
            if "media_id" in result:
                print(f"✅ 草稿创建成功: {result['media_id']}")
                return result["media_id"]
            else:
                print(f"❌ 草稿创建失败: {result}")
                return None
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return None
    
    def publish_article(self, media_id):
        """
        发布图文消息（正式发送给所有用户）
        
        Args:
            media_id: 草稿的media_id
        """
        access_token = self.get_access_token()
        if not access_token:
            return False
            
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit"
        params = {"access_token": access_token}
        
        data = {"media_id": media_id}
        
        try:
            response = requests.post(
                url,
                params=params,
                json=data,
                timeout=30
            )
            result = response.json()
            
            if result.get("errcode") == 0:
                print(f"✅ 文章发布成功！")
                print(f"   publish_id: {result.get('publish_id')}")
                return True
            else:
                print(f"❌ 发布失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return False
    
    def get_publish_status(self, publish_id):
        """查询发布状态"""
        access_token = self.get_access_token()
        if not access_token:
            return None
            
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/get"
        params = {"access_token": access_token}
        
        data = {"publish_id": publish_id}
        
        try:
            response = requests.post(
                url,
                params=params,
                json=data,
                timeout=10
            )
            return response.json()
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return None


def load_config():
    """加载配置文件"""
    config_path = os.path.expanduser("~/.openclaw/workspace/wechat_config.json")
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_config(config):
    """保存配置文件"""
    config_path = os.path.expanduser("~/.openclaw/workspace/wechat_config.json")
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置已保存到: {config_path}")


def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号API配置工具")
    print("=" * 60)
    
    # 加载现有配置
    config = load_config()
    
    if config.get("app_id") and config.get("app_secret"):
        print(f"\n📋 已有配置:")
        print(f"   AppID: {config['app_id']}")
        print(f"   AppSecret: {'*' * len(config['app_secret'])}")
        
        choice = input("\n是否使用现有配置? (y/n): ").strip().lower()
        if choice == 'y':
            app_id = config["app_id"]
            app_secret = config["app_secret"]
        else:
            app_id = input("请输入AppID: ").strip()
            app_secret = input("请输入AppSecret: ").strip()
    else:
        print("\n📝 请输入微信公众号配置:")
        app_id = input("AppID: ").strip()
        app_secret = input("AppSecret: ").strip()
    
    if not app_id or not app_secret:
        print("❌ AppID和AppSecret不能为空")
        return
    
    # 保存配置
    config = {
        "app_id": app_id,
        "app_secret": app_secret,
        "updated_at": datetime.now().isoformat()
    }
    save_config(config)
    
    # 测试连接
    print("\n🔄 测试API连接...")
    wechat = WeChatOfficialAccount(app_id, app_secret)
    token = wechat.get_access_token()
    
    if token:
        print("✅ API连接测试成功！")
        print("\n💡 现在可以使用以下功能:")
        print("   1. 上传图片")
        print("   2. 创建草稿")
        print("   3. 发布文章")
    else:
        print("❌ API连接失败，请检查:")
        print("   - AppID和AppSecret是否正确")
        print("   - 公众号是否已认证")
        print("   - IP白名单是否已配置")


if __name__ == "__main__":
    main()