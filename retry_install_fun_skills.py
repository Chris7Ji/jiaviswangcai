#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重试安装Fun Skills脚本
尝试多种手段安装娱乐技能
"""

import subprocess
import time
import json
import os
import sys
from datetime import datetime

# 要尝试的技能列表
SKILLS_TO_TRY = [
    "games",           # 游戏系统
    "joke-teller",     # 讲笑话
    "chess",           # 下棋
    "clawland",        # 娱乐平台
]

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def try_install_skill(skill_name):
    """尝试安装一个技能"""
    log(f"尝试安装技能: {skill_name}")
    
    # 方法1: 使用clawhub install
    cmd = f"cd /Users/jiyingguo/.openclaw/workspace && clawhub install {skill_name}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        log(f"✅ 成功安装 {skill_name}")
        return True, "clawhub install"
    else:
        error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
        log(f"❌ 安装失败 {skill_name}: {error_msg[:100]}")
        return False, error_msg

def try_inspect_skill(skill_name):
    """查看技能信息（不安装）"""
    log(f"查看技能信息: {skill_name}")
    cmd = f"cd /Users/jiyingguo/.openclaw/workspace && clawhub inspect {skill_name}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        log(f"✅ 可查看 {skill_name}")
        return True, result.stdout.strip()
    else:
        return False, None

def search_github_for_skill(skill_name):
    """在GitHub上搜索技能源码"""
    log(f"在GitHub上搜索: {skill_name}")
    
    # 尝试多个搜索关键词
    search_queries = [
        f"clawhub {skill_name} skill",
        f"openclaw {skill_name} skill",
        f"{skill_name}-skill",
    ]
    
    for query in search_queries:
        cmd = f'''curl -s "https://api.github.com/search/repositories?q={query}&per_page=2"'''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                if data.get("items"):
                    repo = data["items"][0]
                    return True, {
                        "name": repo["full_name"],
                        "url": repo["html_url"],
                        "description": repo.get("description", ""),
                    }
            except:
                pass
    
    return False, None

def create_temp_fun_skill():
    """创建临时娱乐技能"""
    log("创建临时娱乐技能...")
    
    temp_skill_dir = "/Users/jiyingguo/.openclaw/workspace/temp_fun_skill"
    os.makedirs(temp_skill_dir, exist_ok=True)
    
    # 创建SKILL.md
    skill_content = """---
name: temp-fun-skill
description: Temporary fun skills collection with jokes, games, and entertainment. Use when you need quick entertainment, jokes, or simple games.
---

# Temporary Fun Skills

由于clawhub速率限制，这是一个临时娱乐技能集合。

## 可用功能

### 1. 讲笑话
```bash
python3 -c "import random; jokes=['为什么程序员讨厌自然？因为太多bugs！','为什么AI不会打架？因为它们总是神经网络！']; print(random.choice(jokes))"
```

### 2. 猜数字游戏
```bash
python3 -c "import random; number=random.randint(1,10); print('猜一个1-10的数字！'); guess=int(input('你的猜测: ')); print('正确！' if guess==number else f'不对，数字是{number}')"
```

### 3. 硬币翻转
```bash
python3 -c "import random; result='正面' if random.random()>0.5 else '反面'; print(f'硬币翻转结果: {result}')"
```

## 使用方式

直接运行上述Python代码，或让我帮您执行。
"""
    
    with open(os.path.join(temp_skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_content)
    
    log(f"✅ 临时技能创建在: {temp_skill_dir}")
    return temp_skill_dir

def main():
    """主函数"""
    log("🚀 开始尝试多种手段安装Fun Skills")
    log("=" * 50)
    
    # 记录尝试结果
    results = []
    
    # 手段1: 尝试直接安装
    log("🎯 手段1: 尝试直接安装")
    for skill in SKILLS_TO_TRY:
        success, detail = try_install_skill(skill)
        results.append({
            "skill": skill,
            "method": "clawhub install",
            "success": success,
            "detail": detail,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        
        # 如果成功，停止尝试
        if success:
            log(f"🎉 成功安装 {skill}，停止尝试")
            break
        
        # 等待5秒再试下一个
        time.sleep(5)
    
    # 检查是否有成功安装
    installed = any(r["success"] for r in results)
    
    if installed:
        log("✅ 至少成功安装一个技能")
        # 生成报告
        report = "## 安装结果报告\n\n"
        for r in results:
            status = "✅ 成功" if r["success"] else "❌ 失败"
            report += f"- **{r['skill']}** ({r['method']}): {status}\n"
            if not r["success"] and r["detail"]:
                report += f"  错误: {r['detail'][:100]}\n"
        
        log(report)
        return True
    
    # 手段2: 查看技能信息
    log("\n🎯 手段2: 查看技能信息（确认可用性）")
    for skill in SKILLS_TO_TRY[:2]:  # 只查看前两个
        success, info = try_inspect_skill(skill)
        if success and info:
            log(f"📋 {skill} 信息:\n{info[:200]}...")
    
    # 手段3: 搜索GitHub源码
    log("\n🎯 手段3: 搜索GitHub源码")
    for skill in SKILLS_TO_TRY[:2]:
        success, repo_info = search_github_for_skill(skill)
        if success:
            log(f"🔍 找到 {skill} 的GitHub仓库:")
            log(f"   名称: {repo_info['name']}")
            log(f"   URL: {repo_info['url']}")
            log(f"   描述: {repo_info['description'][:100] if repo_info['description'] else '无'}")
        else:
            log(f"🔍 未找到 {skill} 的GitHub仓库")
    
    # 手段4: 创建临时技能
    log("\n🎯 手段4: 创建临时娱乐技能")
    temp_skill_path = create_temp_fun_skill()
    
    # 生成最终报告
    log("\n" + "=" * 50)
    log("📊 最终尝试结果:")
    
    installed_count = sum(1 for r in results if r["success"])
    log(f"✅ 成功安装: {installed_count} 个技能")
    log(f"❌ 安装失败: {len(results) - installed_count} 个技能")
    
    if installed_count == 0:
        log("💡 建议:")
        log("1. 等待几小时后重试（clawhub速率限制）")
        log("2. 使用临时娱乐技能: " + temp_skill_path)
        log("3. 尝试其他非clawhub源的技能")
    
    return installed_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)