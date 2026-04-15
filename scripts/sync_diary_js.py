#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
js/diary.js 同步工具
从 post.html 提取日记条目并同步到 js/diary.js
"""

import os
import re
import shutil
from datetime import datetime

# 文件路径
WORKSPACE = '/Users/jiyingguo/.openclaw/workspace'
ARCHIVE_DIR = os.path.join(WORKSPACE, 'archive', 'diary_js_backups')
POST_HTML = os.path.join(WORKSPACE, 'jiaviswangcai.ai', 'post.html')
JS_DIARY = os.path.join(WORKSPACE, 'jiaviswangcai.ai', 'js', 'diary.js')


def backup_js_diary():
    """备份 js/diary.js"""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(ARCHIVE_DIR, f'diary.js.backup.{timestamp}')
    shutil.copy2(JS_DIARY, backup_path)
    print(f"✅ 已备份 js/diary.js 到 {backup_path}")


def extract_posts_from_post_html():
    """从 post.html 提取日记条目"""
    with open(POST_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式提取日记条目
    # 匹配 <article id="diary-YYYYMMDD" ...>...</article>
    pattern = r'<article\s+id="diary-(\d+)"[^>]*>.*?<header>.*?<h2[^>]*>(.*?)</h2>.*?<span\s+class="category">\[(.*?)\]</span>.*?<p[^>]*>(.*?)</p>.*?<footer>.*?<div\s+class="tags">(.*?)</div>.*?</footer>.*?</article>'
    
    matches = re.findall(pattern, content, re.DOTALL)
    
    posts = []
    for match in matches:
        post_id, title, category, excerpt, tags_html = match
        
        # 解析分类
        category_map = {
            '工作': 'work',
            '学习': 'study',
            '生活': 'life',
            '投资': 'investment',
            'AI': 'ai',
            '技术': 'tech',
        }
        category_key = category_map.get(category, 'work')
        
        # 解析标签
        tags_pattern = r'<span[^>]*class="tag"[^>]*>(.*?)</span>'
        tags = re.findall(tags_pattern, tags_html)
        
        # 格式化日期
        date_str = f"{post_id[:4]}-{post_id[4:6]}-{post_id[6:8]}"
        
        # 分类标签映射
        category_labels = {
            'work': '💼 工作日记',
            'study': '📚 学习日记',
            'life': '🏠 生活日记',
            'investment': '💰 投资日记',
            'ai': '🤖 AI日记',
            'tech': '💻 技术日记',
        }
        category_label = category_labels.get(category_key, '💼 工作日记')
        
        posts.append({
            'id': post_id,
            'date': date_str,
            'category': category_key,
            'categoryLabel': category_label,
            'title': title.strip(),
            'excerpt': excerpt.strip(),
            'tags': tags,
        })
    
    # 按日期倒序排序
    posts.sort(key=lambda x: x['id'], reverse=True)
    
    print(f"✅ 从 post.html 提取了 {len(posts)} 条日记")
    return posts


def generate_js_entry(post):
    """生成单条日记的 JS 对象字面量"""
    # 处理摘要中的特殊字符
    excerpt = post['excerpt'].replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
    
    # 生成标签数组
    tags_str = ', '.join([f"'{tag}'" for tag in post['tags']])
    
    entry = f"""    {{
        id: '{post['id']}',
        date: '{post['date']}',
        category: '{post['category']}',
        categoryLabel: '{post['categoryLabel']}',
        title: \"{post['title']}\",
        excerpt: \"{excerpt}\",
        tags: [{tags_str}],
        views: 0,
        likes: 0
    }}"""
    
    return entry


def update_diary_js(posts):
    """更新 js/diary.js"""
    with open(JS_DIARY, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到数组的开始和结束位置
    # 使用更健壮的方法：使用括号匹配来找到正确的 ];
    
    # 找到 const allPosts = [ 的位置
    start_marker = "const allPosts = ["
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("❌ 找不到 const allPosts = [")
        return False
    
    # 数组内容开始位置
    array_start = start_idx + len(start_marker)
    
    # 使用括号匹配找到数组的结束位置
    # 从 array_start 开始，计数 [ 和 ] 直到 ] 配平且后面跟着 ;
    bracket_count = 1  # 已经遇到了 [
    search_pos = array_start
    end_idx = None
    
    while search_pos < len(content):
        char = content[search_pos]
        
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
            if bracket_count == 0:
                # 检查后面是否是 ;
                if content[search_pos:search_pos+2] == '];':
                    end_idx = search_pos
                    break
        search_pos += 1
    
    if end_idx is None:
        print("❌ 找不到 allPosts 数组结束标记 ];")
        return False
    
    # end_idx 是 ] 的位置，end_idx + 2 是 ; 后面的位置
    after_array = end_idx + 2  # 指向 ; 后面，这样 ]; 完整保留
    
    # 生成新的数组内容
    entries = []
    for post in posts:
        entries.append(generate_js_entry(post))
    
    new_array_content = "\n" + ",\n".join(entries) + "\n"
    
    # 替换旧数组
    new_content = content[:array_start] + new_array_content + content[after_array:]
    
    # 写回文件
    with open(JS_DIARY, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已更新 js/diary.js，共 {len(posts)} 条日记")
    return True


def main():
    print("=" * 60)
    print("📝 js/diary.js 同步工具")
    print("=" * 60)
    
    # 1. 备份
    print("\n[1/3] 备份 js/diary.js...")
    backup_js_diary()
    
    # 2. 从 post.html 提取日记
    print("\n[2/3] 从 post.html 提取日记条目...")
    posts = extract_posts_from_post_html()
    
    if not posts:
        print("❌ 未找到任何日记条目")
        return
    
    # 3. 更新 js/diary.js
    print("\n[3/3] 更新 js/diary.js...")
    if update_diary_js(posts):
        print(f"\n✅ 同步完成!")
        print(f"   - 共同步 {len(posts)} 条日记")
        print(f"   - 日期范围: {posts[-1]['date']} 到 {posts[0]['date']}")
    else:
        print("\n❌ 同步失败")


if __name__ == '__main__':
    main()
