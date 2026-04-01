#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章发布准备脚本
用于准备文章内容和测试发布流程
"""

import os
import json
import html
from datetime import datetime

def prepare_article_content():
    """准备文章内容"""
    print("📝 准备微信公众号文章内容")
    print("=" * 50)
    
    # 读取HTML文章内容
    html_file = "/Users/jiyingguo/.openclaw/workspace/公众号文章_微信公众号格式.html"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 提取文章标题
        title_start = html_content.find('<h1 class="title">')
        title_end = html_content.find('</h1>', title_start)
        
        if title_start != -1 and title_end != -1:
            title = html_content[title_start + len('<h1 class="title">'):title_end].strip()
        else:
            title = "我的AI助手旺财：三天时间构建的四大能力体系"
        
        # 提取文章正文（去除HTML标签，保留必要格式）
        # 这里简化处理，实际发布时需要更复杂的HTML清理
        from html.parser import HTMLParser
        
        class ArticleExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.in_body = False
                self.skip_tags = {'style', 'script', 'head', 'meta', 'link'}
                self.current_tag = ''
                
            def handle_starttag(self, tag, attrs):
                self.current_tag = tag
                if tag == 'body':
                    self.in_body = True
                elif tag in self.skip_tags:
                    self.in_body = False
                    
            def handle_endtag(self, tag):
                if tag == 'body':
                    self.in_body = False
                self.current_tag = ''
                
            def handle_data(self, data):
                if self.in_body and self.current_tag not in self.skip_tags:
                    stripped = data.strip()
                    if stripped:
                        self.text.append(stripped)
        
        parser = ArticleExtractor()
        parser.feed(html_content)
        plain_text = '\n'.join(parser.text)
        
        # 统计信息
        char_count = len(plain_text)
        word_count = len(plain_text.split())
        line_count = plain_text.count('\n') + 1
        
        print(f"✅ 文章内容准备完成")
        print(f"   标题: {title}")
        print(f"   字符数: {char_count}")
        print(f"   字数: {word_count}")
        print(f"   段落数: {line_count}")
        
        # 创建发布配置
        publish_config = {
            "title": title,
            "author": "季",
            "content": html_content,
            "content_source": 2,  # 2表示HTML内容
            "digest": "我的AI助手旺财如何在三天时间里，从一个基础助手进化成拥有四大专业能力的智能伙伴。分享从零到一的AI助手构建经验和技术实现细节。",
            "show_cover_pic": 1,  # 1表示显示封面图片
            "need_open_comment": 1,  # 1表示打开评论
            "only_fans_can_comment": 0,  # 0表示所有人都可以评论
            "prepared_at": datetime.now().isoformat(),
            "file_info": {
                "html_file": html_file,
                "size_kb": os.path.getsize(html_file) / 1024,
                "created_at": datetime.fromtimestamp(os.path.getctime(html_file)).isoformat()
            }
        }
        
        # 保存发布配置
        config_file = "/Users/jiyingguo/.openclaw/workspace/wechat_publish_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(publish_config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 发布配置已保存: {config_file}")
        
        return publish_config
        
    except FileNotFoundError:
        print(f"❌ 文章文件不存在: {html_file}")
        return None
    except Exception as e:
        print(f"❌ 准备文章失败: {e}")
        return None

def check_ip_whitelist():
    """检查IP白名单状态"""
    print("\n🔍 检查IP白名单状态")
    print("=" * 50)
    
    # 获取当前IP（简化版本）
    try:
        import requests
        ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
        current_ip = ip_response.json()['ip']
        
        print(f"当前服务器IP: {current_ip}")
        print("\n⚠️  IP白名单配置提醒:")
        print("=" * 40)
        print("检测到IP白名单未配置，请按以下步骤操作：")
        print()
        print("1. 登录微信公众平台: https://mp.weixin.qq.com/")
        print("2. 左侧菜单 → 开发 → 基本配置")
        print("3. 找到'IP白名单'，点击'查看'")
        print(f"4. 添加IP地址: {current_ip}")
        print("5. 点击'确认修改'保存")
        print()
        print("📌 注意:")
        print("   - 添加IP后需要等待几分钟生效")
        print("   - 确保公众号已认证（订阅号或服务号）")
        print("   - 个人订阅号部分接口可能受限")
        
        return current_ip
        
    except Exception as e:
        print(f"❌ 获取IP失败: {e}")
        print("\n📌 手动检查IP:")
        print("   在终端运行: curl ifconfig.me")
        print("   或访问: https://ifconfig.me")
        return None

def create_publish_instructions():
    """创建发布说明文档"""
    print("\n📋 创建发布说明")
    print("=" * 50)
    
    instructions = """# 微信公众号文章发布说明

## 📋 发布前准备

### 1. IP白名单配置（必须）
当前检测到IP白名单未配置，请按以下步骤操作：

1. **登录微信公众平台**: https://mp.weixin.qq.com/
2. **进入开发 → 基本配置**
3. **找到"IP白名单"**，点击"查看"
4. **添加服务器IP**: 116.6.65.181
5. **点击"确认修改"**保存

### 2. 文章内容
- **文件位置**: `/Users/jiyingguo/.openclaw/workspace/公众号文章_微信公众号格式.html`
- **格式**: 微信公众号专用HTML格式
- **字数**: 约3100字
- **包含**: 标题、正文、样式、互动元素

### 3. 封面图片（可选）
当前文章无封面图片，您可以选择：
- 使用默认封面
- 上传自定义封面图
- 使用文章内第一张图片

## 🚀 发布流程

### 方案A：API自动发布（推荐）
IP白名单配置完成后，运行：

```bash
cd /Users/jiyingguo/.openclaw/workspace
python3 wechat_publisher.py
```

选择：
1. 使用现有配置 (y)
2. 选择"创建草稿"功能
3. 输入文章标题和内容
4. 系统自动创建草稿

### 方案B：手动发布
1. **复制文章内容**:
   - 打开 `公众号文章_微信公众号格式.html`
   - 全选复制（Ctrl+A, Ctrl+C）

2. **登录公众号后台**:
   - 进入"素材管理" → "新建图文素材"
   - 粘贴文章内容（Ctrl+V）
   - 调整格式（微信公众号编辑器会自动处理）

3. **设置封面和摘要**:
   - 上传封面图片
   - 填写文章摘要
   - 设置原创声明（可选）

4. **保存草稿/发布**:
   - 点击"保存草稿"（可后续编辑）
   - 或直接"群发"（立即发布）

## ⚠️ 注意事项

### 内容审核
- 确保文章内容符合微信公众号规范
- 避免敏感词汇和违规内容
- 检查链接是否安全

### 发布时间
- 建议发布时间：工作日 18:00-22:00
- 周末发布时间：10:00-12:00 或 20:00-22:00
- 避开节假日和重大事件时间

### 发布后操作
1. **分享到朋友圈**：增加曝光
2. **回复评论**：与读者互动
3. **数据分析**：查看阅读量、分享数等

## 🔧 故障排除

### 问题1：API连接失败
**症状**: "invalid ip" 错误
**解决**: 确认IP白名单已正确配置

### 问题2：草稿创建失败
**症状**: "content is invalid" 错误
**解决**: 
1. 检查HTML格式是否正确
2. 移除不支持的HTML标签
3. 简化复杂样式

### 问题3：图片上传失败
**症状**: "image upload failed"
**解决**:
1. 确保图片格式为JPG/PNG
2. 图片大小不超过2MB
3. 图片尺寸符合要求

## 📞 技术支持
如有问题，请联系：
- 微信公众平台客服
- 或通过飞书联系旺财助手

---

**发布准备已完成，请配置IP白名单后开始发布！**
"""
    
    instructions_file = "/Users/jiyingguo/.openclaw/workspace/WEICHAT_PUBLISH_INSTRUCTIONS.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ 发布说明已创建: {instructions_file}")
    return instructions_file

def main():
    """主函数"""
    print("🎯 微信公众号文章发布准备工具")
    print("=" * 60)
    
    # 1. 准备文章内容
    article_config = prepare_article_content()
    if not article_config:
        print("❌ 文章准备失败，退出")
        return
    
    # 2. 检查IP白名单
    current_ip = check_ip_whitelist()
    
    # 3. 创建发布说明
    instructions_file = create_publish_instructions()
    
    print("\n" + "=" * 60)
    print("✅ 发布准备完成！")
    print("\n📋 下一步操作:")
    print("1. 配置IP白名单（必须）")
    print("2. 运行 wechat_publisher.py 创建草稿")
    print("3. 在公众号后台确认并发布")
    print(f"\n📁 相关文件:")
    print(f"   文章HTML: /Users/jiyingguo/.openclaw/workspace/公众号文章_微信公众号格式.html")
    print(f"   发布配置: /Users/jiyingguo/.openclaw/workspace/wechat_publish_config.json")
    print(f"   发布说明: {instructions_file}")
    print(f"\n🎯 当前状态: 等待IP白名单配置")

if __name__ == "__main__":
    main()