#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微信公众号API连接
"""

import os
import json
import requests
import time

def test_wechat_api():
    """测试微信公众号API连接"""
    print("🔍 测试微信公众号API连接")
    print("=" * 50)
    
    # 读取配置
    config_path = "/Users/jiyingguo/.openclaw/workspace/wechat_config.json"
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        app_id = config.get('app_id')
        app_secret = config.get('app_secret')
        
        if not app_id or not app_secret:
            print("❌ 配置不完整：缺少AppID或AppSecret")
            return False
        
        print(f"✅ 配置读取成功")
        print(f"   AppID: {app_id[:8]}...{app_id[-4:]}")
        print(f"   AppSecret: {app_secret[:8]}...{app_secret[-4:]}")
        
        # 测试获取Access Token
        print("\n🔄 测试获取Access Token...")
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
                access_token = data["access_token"]
                expires_in = data.get("expires_in", 7200)
                
                print(f"✅ Access Token获取成功！")
                print(f"   Token: {access_token[:20]}...")
                print(f"   有效期: {expires_in}秒 ({expires_in/3600:.1f}小时)")
                
                # 测试获取公众号信息
                print("\n🔄 测试获取公众号信息...")
                info_url = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info"
                info_params = {"access_token": access_token}
                
                info_response = requests.get(info_url, params=info_params, timeout=10)
                info_data = info_response.json()
                
                if "is_menu_open" in info_data:
                    print(f"✅ 公众号信息获取成功")
                    print(f"   菜单状态: {'已开启' if info_data['is_menu_open'] == 1 else '未开启'}")
                    return True
                else:
                    print(f"⚠️  公众号信息获取受限: {info_data.get('errmsg', '未知错误')}")
                    print(f"   但Access Token有效，可以创建草稿")
                    return True
                    
            else:
                error_msg = data.get('errmsg', '未知错误')
                error_code = data.get('errcode', '未知')
                print(f"❌ 获取Token失败: {error_msg} (错误码: {error_code})")
                
                if error_code == 40164:
                    print("   原因: IP地址不在白名单中")
                    print("   解决: 在公众号后台添加IP白名单")
                elif error_code == 40013:
                    print("   原因: AppID或AppSecret错误")
                elif error_code == 40125:
                    print("   原因: AppSecret错误")
                
                return False
                
        except requests.exceptions.Timeout:
            print("❌ 请求超时：请检查网络连接")
            return False
        except requests.exceptions.ConnectionError:
            print("❌ 连接失败：无法连接到微信服务器")
            return False
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False
            
    except FileNotFoundError:
        print(f"❌ 配置文件不存在: {config_path}")
        return False
    except json.JSONDecodeError:
        print(f"❌ 配置文件格式错误")
        return False
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")
        return False

if __name__ == "__main__":
    success = test_wechat_api()
    print("\n" + "=" * 50)
    if success:
        print("🎉 API测试完成：配置有效，可以发布文章")
    else:
        print("❌ API测试失败：请检查配置")