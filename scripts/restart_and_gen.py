#!/usr/bin/env python3
"""修复 OpenClaw 配置并重启 Gateway"""

import json
import subprocess
import time
import os

# 读取当前配置
config_path = "/Users/jiyingguo/.openclaw/openclaw.json"
with open(config_path, 'r') as f:
    config = json.load(f)

print("当前 alsoAllow:")
print(json.dumps(config.get('tools', {}).get('alsoAllow', []), indent=2))

# 修复 alsoAllow 列表，添加更多命令
correct_alsoAllow = [
    # Python 和脚本路径
    "python3 /Users/jiyingguo/.openclaw/workspace/scripts/",
    "python3 /Users/jiyingguo/.openclaw/workspace/skills/",
    # Bash 脚本
    "bash /Users/jiyingguo/.openclaw/workspace/scripts/",
    "bash /Users/jiyingguo/.openclaw/workspace/skills/",
    # UV 图片生成
    "uv run /Users/jiyingguo/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py",
    "uv run /Users/jiyingguo/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py --",
    # Node
    "node",
    "node /Users/jiyingguo/.openclaw/workspace/skills/12306/scripts/query.mjs",
    # 添加 openclaw 命令
    "openclaw",
    "openclaw gateway restart",
    "openclaw gateway",
    # 常用系统命令
    "launchctl",
    "kill",
    "launchd",
]

# 更新配置
config['tools']['alsoAllow'] = correct_alsoAllow

# 写回配置
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("\n新 alsoAllow:")
print(json.dumps(config['tools']['alsoAllow'], indent=2))
print("\n配置已更新！")
