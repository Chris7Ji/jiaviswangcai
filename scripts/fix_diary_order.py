#!/usr/bin/env python3
"""
修复 diary.js 和 post.html 中的日记条目顺序
1. 解析所有条目
2. 按日期降序排列（最新在前）
3. 重新生成两个文件
4. 同时同步 post.html 中缺失的条目（从 diary.js 补充）
"""
import re, os, shutil
from datetime import datetime

WEBSITE_DIR = '/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai'
JS_DIARY = os.path.join(WEBSITE_DIR, 'js', 'diary.js')
POST_HTML = os.path.join(WEBSITE_DIR, 'post.html')

def backup(path):
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    bp = path + f'.backup_reorder_{ts}'
    shutil.copy2(path, bp)
    print(f"  📦 备份: {bp}")

def parse_allposts(content, label="file"):
    """解析 allPosts 数组中的所有条目"""
    # 找到 allPosts 数组
    m = re.search(r'const allPosts = \[([\s\S]*?)\];', content)
    if not m:
        print(f"  ❌ {label}: 找不到 allPosts 数组")
        return []
    
    body = m.group(1)
    # 提取每个条目的完整文本
    entries = []
    # 匹配每个 {...} 对象
    depth = 0
    start = -1
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start >= 0:
                entry_text = body[start:i+1]
                # 提取 id
                id_m = re.search(r"id:\s*'(\d+)'", entry_text)
                if id_m:
                    entries.append(entry_text.strip())
                start = -1
        i += 1
    
    print(f"  📊 {label}: 解析到 {len(entries)} 条日记")
    return entries

def extract_id(entry):
    m = re.search(r"id:\s*'(\d+)'", entry)
    return m.group(1) if m else "00000000"

def fix_diary_js():
    """修复 diary.js 中的条目顺序"""
    print("\n=== 修复 diary.js ===")
    backup(JS_DIARY)
    
    with open(JS_DIARY, 'r') as f:
        content = f.read()
    
    # 解析所有条目
    entries = parse_allposts(content, "diary.js")
    
    # 按日期降序排序（最新在前）
    entries.sort(key=extract_id, reverse=True)
    sorted_ids = [extract_id(e) for e in entries]
    print(f"  📋 排序后: {sorted_ids[:5]} ... {sorted_ids[-5:]}")
    
    # 重新构建数组
    new_array = "const allPosts = [\n" + ",\n".join(entries) + "\n];"
    
    # 替换原来的数组（用字符串切片，避免正则模板转义问题）
    start_marker = 'const allPosts = ['
    end_marker = '];'
    start_idx = content.index(start_marker)
    # 从起始位置找到第一个 ];（数组结束）
    end_idx = content.index(end_marker, start_idx + len(start_marker)) + len(end_marker)
    new_content = content[:start_idx] + new_array + content[end_idx:]
    
    with open(JS_DIARY, 'w') as f:
        f.write(new_content)
    
    print(f"  ✅ diary.js: {len(entries)} 条日记已按日期排序")

def fix_post_html():
    """修复 post.html 中的条目顺序，并从 diary.js 补充缺失条目"""
    print("\n=== 修复 post.html ===")
    backup(POST_HTML)
    
    with open(POST_HTML, 'r') as f:
        content = f.read()
    
    # 解析 post.html 的当前条目
    post_entries = parse_allposts(content, "post.html")
    post_ids = {extract_id(e) for e in post_entries}
    
    # 从 diary.js 读取完整条目列表
    with open(JS_DIARY, 'r') as f:
        diary = f.read()
    diary_entries = parse_allposts(diary, "diary.js (for sync)")
    diary_entries_by_id = {extract_id(e): e for e in diary_entries}
    
    # 检查哪些条目在 diary.js 有但 post.html 没有
    missing = [eid for eid in diary_entries_by_id if eid not in post_ids]
    if missing:
        print(f"  ⚠️ post.html 缺失 {len(missing)} 条: {sorted(missing)}")
        # 补充缺失条目
        for mid in sorted(missing, reverse=True):
            entry = diary_entries_by_id[mid]
            post_entries.append(entry)
        print(f"  ✅ 已补充 {len(missing)} 条")
    
    # 按日期降序排序
    post_entries.sort(key=extract_id, reverse=True)
    sorted_ids = [extract_id(e) for e in post_entries]
    print(f"  📋 排序后 post.html: {len(post_entries)} 条")
    
    # 重新构建数组
    new_array = "const allPosts = [\n" + ",\n".join(post_entries) + "\n];"
    
    # 替换（用字符串切片，避免正则模板转义问题）
    start_marker = 'const allPosts = ['
    end_marker = '];'
    start_idx = content.index(start_marker)
    end_idx = content.index(end_marker, start_idx + len(start_marker)) + len(end_marker)
    new_content = content[:start_idx] + new_array + content[end_idx:]
    
    with open(POST_HTML, 'w') as f:
        f.write(new_content)
    
    print(f"  ✅ post.html: {len(post_entries)} 条日记已排序并补全")

if __name__ == '__main__':
    print("🔧 日记条目顺序修复工具")
    print("=" * 50)
    fix_diary_js()
    fix_post_html()
    print("\n" + "=" * 50)
    print("✅ 修复完成！")
    
    # 验证
    with open(JS_DIARY) as f:
        ids1 = re.findall(r"id:\s*'(\d+)'", f.read())
    with open(POST_HTML) as f:
        ids2 = re.findall(r"id:\s*'(\d+)'", f.read())
    
    print(f"\n📊 最终统计:")
    print(f"  diary.js: {len(ids1)} 条 (最新: {ids1[0]}, 最早: {ids1[-1]})")
    print(f"  post.html: {len(ids2)} 条 (最新: {ids2[0]}, 最早: {ids2[-1]})")
    
    # 检查排序是否正确
    for i in range(len(ids1)-1):
        if ids1[i] < ids1[i+1]:
            print(f"  ❌ diary.js 排序错误: {ids1[i]} < {ids1[i+1]}")
            break
    else:
        print(f"  ✅ diary.js 排序正确（降序）")
    
    for i in range(len(ids2)-1):
        if ids2[i] < ids2[i+1]:
            print(f"  ❌ post.html 排序错误: {ids2[i]} < {ids2[i+1]}")
            break
    else:
        print(f"  ✅ post.html 排序正确（降序）")
