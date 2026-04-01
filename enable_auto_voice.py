#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启用OpenClaw自动语音回复配置
"""

import json
import os
import sys
import shutil
from datetime import datetime

CONFIG_PATH = "/Users/jiyingguo/.openclaw/openclaw.json"
BACKUP_PATH = "/Users/jiyingguo/.openclaw/openclaw.json.backup"

def enable_auto_voice_reply():
    """启用自动语音回复配置"""
    
    # 备份原配置
    if os.path.exists(CONFIG_PATH):
        shutil.copy2(CONFIG_PATH, BACKUP_PATH)
        print(f"✅ 已备份原配置到: {BACKUP_PATH}")
    
    # 读取配置
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 确保channels.feishu存在
    if "channels" not in config:
        config["channels"] = {}
    
    if "feishu" not in config["channels"]:
        print("❌ 配置中未找到feishu配置")
        return False
    
    # 添加自动语音回复配置
    feishu_config = config["channels"]["feishu"]
    
    # 添加配置项
    feishu_config["auto_voice_reply"] = True
    feishu_config["tts_enabled"] = True
    feishu_config["voice_reply_format"] = "mp3"
    
    # 添加注释
    config["_comment"] = f"自动语音回复已启用 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # 写回配置
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ 已启用自动语音回复配置")
    print("📋 修改内容:")
    print(f"  - auto_voice_reply: {feishu_config.get('auto_voice_reply')}")
    print(f"  - tts_enabled: {feishu_config.get('tts_enabled')}")
    print(f"  - voice_reply_format: {feishu_config.get('voice_reply_format')}")
    
    # 显示需要重启的提示
    print("\n⚠️  需要重启OpenClaw网关使配置生效:")
    print("  openclaw gateway restart")
    
    return True

def check_current_config():
    """检查当前配置"""
    print("🔍 检查当前配置...")
    
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ 配置文件不存在: {CONFIG_PATH}")
        return
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 检查feishu配置
    feishu_config = config.get("channels", {}).get("feishu", {})
    
    print("📋 当前feishu配置:")
    for key, value in feishu_config.items():
        if key not in ["appSecret"]:  # 跳过敏感信息
            print(f"  - {key}: {value}")
    
    # 检查自动语音回复相关配置
    auto_voice = feishu_config.get("auto_voice_reply")
    tts_enabled = feishu_config.get("tts_enabled")
    
    print(f"\n🎯 自动语音回复状态:")
    print(f"  - auto_voice_reply: {'✅ 已启用' if auto_voice else '❌ 未启用'}")
    print(f"  - tts_enabled: {'✅ 已启用' if tts_enabled else '❌ 未启用'}")

def main():
    """主函数"""
    print("=" * 60)
    print("OpenClaw 自动语音回复配置工具")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_current_config()
        return
    
    # 检查当前配置
    check_current_config()
    
    print("\n" + "=" * 60)
    choice = input("是否启用自动语音回复? (y/n): ").strip().lower()
    
    if choice == 'y':
        print("\n🔄 正在启用自动语音回复...")
        if enable_auto_voice_reply():
            print("\n🎉 配置更新成功!")
            print("请运行: openclaw gateway restart")
        else:
            print("\n❌ 配置更新失败")
    else:
        print("\n⏹️  已取消操作")

if __name__ == "__main__":
    main()