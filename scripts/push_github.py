#!/usr/bin/env python3
"""
GitHub Push Script for 旺财Jarvis Website
自动推送网站更新到 GitHub
"""
import subprocess
import sys
import os

# 网站仓库路径
WEBSITE_PATH = "/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai"
COMMIT_MESSAGE = "浅色系配色优化 + SVG吉祥物头像"

def run_cmd(cmd, cwd=None, capture=True):
    """执行命令并返回结果"""
    result = subprocess.run(
        cmd, 
        shell=True, 
        cwd=cwd or WEBSITE_PATH,
        capture_output=capture, 
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def push_to_github():
    print("🚀 开始推送网站到 GitHub...")
    print(f"📂 仓库路径: {WEBSITE_PATH}")
    
    # 检查是否是 git 仓库
    rc, stdout, stderr = run_cmd("git status", WEBSITE_PATH)
    if rc != 0:
        print(f"❌ Git 仓库检查失败: {stderr}")
        return False
    
    # 检查远程仓库
    rc, stdout, stderr = run_cmd("git remote -v", WEBSITE_PATH)
    print(f"📡 远程仓库: {stdout.strip()}")
    if not stdout.strip():
        print("📡 添加 GitHub 远程仓库...")
        rc, stdout, stderr = run_cmd(
            "git remote add origin https://github.com/Chris7Ji/jarviswangcai.git", 
            WEBSITE_PATH
        )
        if rc != 0:
            print(f"⚠️  添加远程仓库失败（可能已存在）: {stderr}")
    
    # 需要提交的网站文件
    website_files = [
        "index.html", "about.html", "diary.html", "post.html", "skills.html",
        "README.md", "css/", "js/"
    ]
    
    # 添加网站文件
    print("\n📦 添加网站文件...")
    for f in website_files:
        rc, stdout, stderr = run_cmd(f"git add {f}", WEBSITE_PATH)
        if rc != 0:
            print(f"⚠️  添加 {f} 失败: {stderr}")
    
    # 检查状态
    rc, stdout, stderr = run_cmd("git status", WEBSITE_PATH)
    print(f"📊 Git 状态:\n{stdout}")
    
    # 检查是否有更改
    if "nothing to commit" in stdout:
        print("📝 没有需要推送的更改")
        return True
    
    # 提交
    print(f"\n💾 提交更改: {COMMIT_MESSAGE}")
    rc, stdout, stderr = run_cmd(f'git commit -m "{COMMIT_MESSAGE}"', WEBSITE_PATH)
    if rc != 0:
        print(f"❌ Git commit 失败: {stderr}")
        return False
    print(f"✅ 提交成功")
    
    # 设置上游分支并推送
    print("\n🚀 推送到 GitHub...")
    rc, stdout, stderr = run_cmd("git branch -M main", WEBSITE_PATH)
    if rc != 0:
        print(f"⚠️  设置分支失败: {stderr}")
    
    rc, stdout, stderr = run_cmd("git push -u origin main --force", WEBSITE_PATH)
    if rc != 0:
        print(f"❌ Git push 失败: {stderr}")
        return False
    
    print("✅ 推送成功!")
    print(stdout)
    return True

if __name__ == "__main__":
    success = push_to_github()
    sys.exit(0 if success else 1)
