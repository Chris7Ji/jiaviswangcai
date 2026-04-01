#!/usr/bin/env python3
import requests

# 配置
APP_ID = "wx3107689f438ee0d0"
APP_SECRET = "c56cc59e9be8c9ccb2a78dd4d226eee5"

# 获取token
token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
token_resp = requests.get(token_url).json()
access_token = token_resp.get("access_token")

if not access_token:
    print(f"获取token失败: {token_resp}")
    exit(1)

print(f"✅ Token获取成功")

# 读取文章
with open("/Users/jiyingguo/.openclaw/workspace/wechat_article_openclaw.md", "r") as f:
    md_content = f.read()

# 提取标题
lines = md_content.split('\n')
title = ""
for line in lines:
    if line.startswith('# ') and not title:
        title = line.replace('# ', '').strip()
        break

print(f"标题: {title}")

# 准备内容（简化HTML）
content_lines = []
for line in lines[1:]:  # 跳过标题
    if '备选标题' in line:
        continue
    if line.strip().startswith(('1. **《', '2. **《', '3. **《')):
        continue
    if '| 章节 | 配图建议 |' in line:
        break
    if line.startswith('## 摘要'):
        break
    content_lines.append(line)

html_content = '<p>' + '</p><p>'.join(['<br>'.join(p.split('\n')) for p in '\n'.join(content_lines).split('\n\n') if p.strip()]) + '</p>'

# 创建草稿
draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"

payload = {
    "articles": [{
        "title": title,
        "content": html_content,
        "author": "季",
        "digest": "一个开源AI助手项目，三个月斩获30万Star。它凭什么让开发者疯狂？",
        "show_cover_pic": 0,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]
}

resp = requests.post(draft_url, json=payload).json()
print(f"API响应: {resp}")

if "media_id" in resp:
    print(f"\n✅ 草稿创建成功!")
    print(f"Media ID: {resp['media_id']}")
    
    # 立即发布
    publish_url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
    pub_resp = requests.post(publish_url, json={"media_id": resp['media_id']}).json()
    print(f"发布响应: {pub_resp}")
    
    if pub_resp.get("errcode") == 0:
        print(f"\n🎉 文章发布成功!")
        print(f"Publish ID: {pub_resp.get('publish_id')}")
    else:
        print(f"\n⚠️  发布失败: {pub_resp}")
        print("请手动在微信公众平台发布")
else:
    print(f"\n❌ 草稿创建失败: {resp}")
    print("错误码说明: https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Global_Return_Code.html")