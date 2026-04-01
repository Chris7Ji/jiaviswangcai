#!/usr/bin/env python3
"""
修复 exec 白名单 - 添加 git 命令支持
"""
import json
import os
import subprocess

CONFIG_PATH = "/Users/jiyingguo/.openclaw/openclaw.json"

def main():
    print("🔧 开始修复 exec 白名单...")
    
    # 读取配置
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    
    # 检查 tools.alsoAllow 是否存在
    if 'tools' not in config:
        print("❌ 配置中找不到 tools 部分")
        return 1
    
    tools = config['tools']
    if 'alsoAllow' not in tools:
        print("❌ 配置中找不到 tools.alsoAllow")
        return 1
    
    # 当前的 alsoAllow 列表
    also_allow = tools['alsoAllow']
    print(f"📋 当前 alsoAllow 列表 ({len(also_allow)} 项):")
    for item in also_allow:
        print(f"   - {item}")
    
    # 要添加的 git 相关条目
    git_entries = [
        "git",
        "git -C",
    ]
    
    # 检查是否已经添加
    for entry in git_entries:
        if entry in also_allow:
            print(f"✅ {entry} 已在白名单中")
        else:
            print(f"➕ 添加 {entry} 到白名单...")
            also_allow.append(entry)
    
    # 写回配置
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("\n✅ 配置已更新!")
    print("📋 新的 alsoAllow 列表:")
    for item in also_allow:
        print(f"   - {item}")
    
    print("\n🔄 需要重启 OpenClaw Gateway 使配置生效...")
    print("   运行: openclaw gateway restart")
    
    return 0

if __name__ == "__main__":
    exit(main())
