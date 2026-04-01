#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试多种方法安装技能
"""

import subprocess
import time
import json
import os
import sys

def run_cmd(cmd, description):
    """运行命令并返回结果"""
    print(f"\n🔧 {description}")
    print(f"📝 命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        print(f"📤 输出: {result.stdout[:200]}...")
        if result.stderr:
            print(f"❌ 错误: {result.stderr[:200]}")
        
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print("⏰ 命令超时")
        return False, "", "Timeout"
    except Exception as e:
        print(f"💥 异常: {e}")
        return False, "", str(e)

def method1_direct_install(skill_name):
    """方法1：直接安装"""
    cmd = f"clawhub install {skill_name}"
    return run_cmd(cmd, f"直接安装 {skill_name}")

def method2_delayed_install(skill_name, delay_seconds=60):
    """方法2：延迟安装"""
    print(f"\n⏳ 等待 {delay_seconds} 秒后重试...")
    time.sleep(delay_seconds)
    return method1_direct_install(skill_name)

def method3_alternative_skill(skill_name, alternatives):
    """方法3：尝试替代技能"""
    results = []
    for alt in alternatives:
        success, stdout, stderr = method1_direct_install(alt)
        results.append((alt, success))
        if success:
            print(f"✅ 成功安装替代技能: {alt}")
            return True, f"使用替代技能: {alt}"
        time.sleep(10)  # 避免速率限制
    return False, "所有替代技能安装失败"

def method4_check_existing():
    """方法4：检查现有技能"""
    print("\n🔍 检查现有已安装技能...")
    success, stdout, stderr = run_cmd("clawhub list", "列出已安装技能")
    if success and stdout.strip():
        print(f"📋 已安装技能:\n{stdout}")
        return True, "有已安装技能"
    else:
        print("📭 没有已安装技能")
        return False, "没有已安装技能"

def method5_create_skill_guide(skill_name, skill_type):
    """方法5：创建技能使用指南"""
    print(f"\n📝 为 {skill_name} 创建临时使用指南")
    
    guide_content = f"""# {skill_name} 技能临时使用指南

由于clawhub API速率限制，{skill_name}技能暂时无法安装。以下是临时解决方案：

## 功能描述
{skill_type}

## 临时替代方案

### 1. 使用现有相关技能
- 检查已安装的52个技能中是否有类似功能
- 使用clawhub search查找相关技能

### 2. 手动实现核心功能
- 告诉我具体需求，我可以手动实现类似功能
- 创建临时脚本或工作流

### 3. 等待安装
- 明天再尝试安装，避免速率限制
- 设置定时任务自动重试

## 具体需求收集
请告诉我您想用 {skill_name} 做什么具体任务，我可以：
1. 推荐现有替代方案
2. 创建临时解决方案
3. 记录需求，优先安装

---
**状态**: 等待clawhub速率限制解除
**最后尝试**: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    guide_file = f"/tmp/{skill_name.replace('-', '_')}_guide.md"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ 指南已保存到: {guide_file}")
    return True, f"指南文件: {guide_file}"

def main():
    print("🚀 开始尝试多种方法安装技能")
    print("=" * 60)
    
    # 要尝试的技能
    skills_to_try = [
        {
            "name": "games",
            "type": "游戏娱乐功能 (Fun Skills)",
            "alternatives": ["chess", "clawland", "clawzone"]
        },
        {
            "name": "office-xyz", 
            "type": "办公自动化 (Office Automation)",
            "alternatives": ["office-document-specialist-suite", "office-secretary", "tiangong-wps-word-automation"]
        }
    ]
    
    all_results = []
    
    for skill in skills_to_try:
        print(f"\n{'='*60}")
        print(f"🎯 处理技能: {skill['name']} ({skill['type']})")
        print(f"{'='*60}")
        
        skill_results = []
        
        # 方法1：直接安装
        success, stdout, stderr = method1_direct_install(skill["name"])
        skill_results.append(("直接安装", success))
        
        if not success and "Rate limit exceeded" in stderr:
            print("⚠️ 检测到速率限制，尝试其他方法...")
            
            # 方法2：延迟安装
            success2, stdout2, stderr2 = method2_delayed_install(skill["name"], 30)
            skill_results.append(("延迟安装", success2))
            
            # 方法3：替代技能
            success3, msg3 = method3_alternative_skill(skill["name"], skill["alternatives"])
            skill_results.append(("替代技能", success3))
            
            # 方法4：检查现有
            success4, msg4 = method4_check_existing()
            skill_results.append(("检查现有", success4))
            
            # 方法5：创建指南
            success5, msg5 = method5_create_skill_guide(skill["name"], skill["type"])
            skill_results.append(("创建指南", success5))
        
        # 汇总结果
        all_results.append({
            "skill": skill["name"],
            "type": skill["type"],
            "results": skill_results
        })
        
        # 技能间等待
        if skill != skills_to_try[-1]:
            print(f"\n⏳ 技能间等待10秒...")
            time.sleep(10)
    
    # 输出总结
    print(f"\n{'='*60}")
    print("📊 安装尝试总结")
    print(f"{'='*60}")
    
    for result in all_results:
        print(f"\n🔹 {result['skill']} ({result['type']}):")
        for method_name, success in result["results"]:
            status = "✅ 成功" if success else "❌ 失败"
            print(f"  {method_name}: {status}")
    
    # 总体建议
    print(f"\n{'='*60}")
    print("💡 总体建议")
    print(f"{'='*60}")
    
    print("""
1. **clawhub速率限制严格** - 所有安装方法都受限制
2. **最佳方案** - 明天再尝试安装
3. **临时方案** - 使用现有技能或创建指南
4. **长期方案** - 联系clawhub支持或使用其他技能源

## 立即可用的替代方案：
- **Fun Skills** → 使用现有技能：weather, summarize, video-frames等
- **Office Automation** → 使用现有技能：nano-pdf, 或手动Office文件处理

告诉我具体需求，我可以提供更精准的替代方案！
""")
    
    return all_results

if __name__ == "__main__":
    results = main()
    
    # 保存结果到文件
    result_file = "/tmp/skill_install_attempts.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 详细结果已保存到: {result_file}")