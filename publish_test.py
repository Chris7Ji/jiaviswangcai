#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json

APP_ID = "wx3107689f438ee0d0"
APP_SECRET = "c56cc59e9be8c9ccb2a78dd4d226eee5"

# 获取token
url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
resp = requests.get(url)
token = resp.json().get("access_token")

if not token:
    print("获取token失败")
    exit(1)

print(f"Token: {token[:20]}...")

# 读取文章
with open("/Users/jiyingguo/.openclaw/workspace/wechat_article_openclaw.md", "r") as f:
    content = f.read()

# 提取标题
lines = content.split('\n')
title = ""
for line in lines:
    if line.startswith('# ') and not title:
        title = line.replace('# ', '').strip()
        break

print(f"标题: {title}")

# 简化HTML转换 - 只保留基本格式
html_content = content.replace('\n\n', '</p><p>').replace('\n', '<br>')
html_content = f'<p>{html_content}</p>'

# 创建草稿
url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
data = {
    "articles": [{
        "title": title,
        "content": html_content[:20000],  # 限制长度
        "author": "季",
        "digest": "一个开源AI助手项目，三个月斩获30万Star。",
        "show_cover_pic": 0,
        "need_open_comment": 1
    }]
}

resp = requests.post(url, json=data)
result = resp.json()

print(f"结果: {result}")

if "media_id" in result:
    print(f"✅ 成功！Media ID: {result['media_id']}")
else:
    print(f"❌ 失败: {result}")