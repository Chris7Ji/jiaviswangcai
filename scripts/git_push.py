#!/usr/bin/env python3
"""
Git自动推送脚本
用法: python3 git_push.py [commit-message]
默认提交信息: "自动更新"
"""
import subprocess
import sys
import os

REPO_PATH = "/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai"

def run_git(*args):
    """运行git命令"""
    cmd = ["git", "-C", REPO_PATH] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "自动更新"
    
    print("=" * 50)
    print("Git 自动推送脚本")
    print("=" * 50)
    
    # 1. 检查状态
    print("\n📊 检查Git状态...")
    result = run_git("status", "--porcelain")
    if result.returncode != 0:
        print(f"❌ Git状态检查失败: {result.stderr}")
        return 1
    
    output = result.stdout.strip()
    if not output:
        print("✅ 没有需要提交的更改")
        return 0
    
    print(f"📝 有更改需要提交:")
    print(output)
    
    # 2. 添加所有更改
    print("\n📦 添加文件...")
    result = run_git("add", "-A")
    if result.returncode != 0:
        print(f"❌ Git add失败: {result.stderr}")
        return 1
    print("✅ 文件已添加")
    
    # 3. 提交
    print(f"\n💾 提交更改: {commit_msg}")
    result = run_git("commit", "-m", commit_msg)
    if result.returncode != 0:
        print(f"❌ Git commit失败: {result.stderr}")
        return 1
    print("✅ 提交成功")
    
    # 4. 推送
    print("\n🚀 推送到GitHub...")
    result = run_git("push", "-u", "origin", "main", "--force")
    if result.returncode != 0:
        print(f"❌ Git push失败: {result.stderr}")
        return 1
    print("✅ 推送成功!")
    print(result.stdout)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
