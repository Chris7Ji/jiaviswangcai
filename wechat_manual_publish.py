#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章发布助手 - 手动发布版
由于API限制，提供优化的复制粘贴方案
"""

import pyperclip
import re

def clean_article_for_wechat():
    """清理文章格式，优化为微信公众号编辑器友好的格式"""
    
    # 读取文章
    with open("/Users/jiyingguo/.openclaw/workspace/wechat_article_openclaw.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取标题
    lines = content.split('\n')
    title = ""
    for line in lines:
        if line.startswith('# ') and not title:
            title = line.replace('# ', '').strip()
            break
    
    # 清理内容（移除不适合微信的部分）
    cleaned_lines = []
    in_table = False
    
    for line in lines:
        # 跳过标题行
        if line.startswith('# ') and not cleaned_lines:
            continue
        
        # 跳过备选标题部分
        if '备选标题' in line:
            continue
        if line.strip().startswith('1. **《') or line.strip().startswith('2. **《') or line.strip().startswith('3. **《'):
            continue
        
        # 跳过配图建议表格
        if '| 章节 | 配图建议 |' in line:
            in_table = True
            continue
        if in_table:
            if line.strip() and not line.startswith('|'):
                in_table = False
            else:
                continue
        
        # 跳过摘要部分
        if line.startswith('## 摘要'):
            break
        
        cleaned_lines.append(line)
    
    # 处理Markdown格式为微信友好的格式
    result = '\n'.join(cleaned_lines)
    
    # 转换格式
    result = result.replace('---', '')  # 移除分隔线
    result = re.sub(r'\*\*(.+?)\*\*', r'\1', result)  # 移除粗体标记（微信编辑器可以手动设置）
    result = result.replace('• ', '● ')  # 统一列表符号
    
    return title, result

def main():
    print("=" * 60)
    print("微信公众号文章发布助手")
    print("=" * 60)
    
    print("\n⚠️  API自动发布遇到限制")
    print("📝  切换到手动发布辅助模式\n")
    
    # 清理文章
    print("🧹 清理文章格式...")
    title, content = clean_article_for_wechat()
    
    print(f"\n✅ 文章已优化")
    print(f"   标题: {title}")
    print(f"   字数: {len(content)} 字符")
    
    # 复制到剪贴板
    print("\n📋 正在复制到剪贴板...")
    
    # 分段复制（避免剪贴板过大）
    full_text = f"{title}\n\n{content}"
    
    try:
        pyperclip.copy(full_text)
        print("✅ 已复制到剪贴板！")
    except Exception as e:
        print(f"⚠️  自动复制失败: {e}")
        print("   请手动复制以下内容：\n")
        print("=" * 60)
        print(full_text[:2000])  # 显示前2000字符
        print("...")
        print("=" * 60)
    
    print("\n" + "=" * 60)
    print("📱 手动发布步骤")
    print("=" * 60)
    print("""
1. 登录微信公众平台: https://mp.weixin.qq.com/

2. 点击左侧菜单: "内容与互动" → "图文消息" → "新建图文消息"

3. 粘贴内容:
   - 标题已复制，直接粘贴到标题栏
   - 正文已复制，粘贴到编辑器

4. 格式调整:
   - 小标题设置为"标题"格式（H2）
   - 重点文字设置为"粗体"
   - 列表使用编辑器列表功能

5. 上传封面图片:
   - 建议尺寸: 900×383 像素
   - 建议使用OpenClaw Logo或GitHub Stars截图

6. 设置摘要:
   一个开源AI助手项目，三个月斩获30万Star。
   它凭什么让开发者疯狂？本文揭秘OpenClaw的崛起之路。

7. 预览并发布:
   - 点击"预览"发送到手机查看效果
   - 确认无误后点击"群发"

8. 推荐发布时间:
   - 工作日晚 8:00-10:00
   - 或周末早 10:00-12:00
""")
    
    # 保存优化后的文章
    output_path = "/Users/jiyingguo/.openclaw/workspace/wechat_article_optimized.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"\n💾 优化后的文章已保存到:")
    print(f"   {output_path}")
    print(f"\n您也可以直接打开此文件复制内容")
    
    print("\n" + "=" * 60)
    print("✅ 准备就绪！请按照上述步骤发布")
    print("=" * 60)

if __name__ == "__main__":
    main()