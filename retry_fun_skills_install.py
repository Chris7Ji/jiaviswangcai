#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时重试安装Fun Skills脚本
今天内尝试多次安装娱乐技能
"""

import subprocess
import time
import sys
from datetime import datetime

# 重试时间表（小时:分钟）
RETRY_SCHEDULE = [
    "09:30",
    "10:30", 
    "11:30",
    "14:30",
    "17:30"
]

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def try_install(skill_name):
    """尝试安装一个技能"""
    log(f"尝试安装 {skill_name}...")
    
    # 尝试使用--force参数
    cmd = f"cd /Users/jiyingguo/.openclaw/workspace && clawhub install {skill_name} --force"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        log(f"✅ 成功安装 {skill_name}!")
        return True, result.stdout.strip()
    else:
        error = result.stderr.strip() if result.stderr else result.stdout.strip()
        log(f"❌ 安装失败 {skill_name}: {error[:100]}")
        return False, error

def wait_until(target_time):
    """等待到目标时间"""
    now = datetime.now()
    target = datetime.strptime(target_time, "%H:%M")
    target = target.replace(year=now.year, month=now.month, day=now.day)
    
    if target < now:
        # 如果目标时间已过，改为明天
        from datetime import timedelta
        target += timedelta(days=1)
    
    wait_seconds = (target - now).total_seconds()
    
    if wait_seconds > 0:
        log(f"等待 {wait_seconds/60:.1f} 分钟直到 {target_time}...")
        time.sleep(wait_seconds)
        return True
    else:
        return True

def main():
    """主函数"""
    log("🚀 开始定时重试安装Fun Skills")
    log(f"重试时间表: {', '.join(RETRY_SCHEDULE)}")
    log("目标技能: games, joke-teller")
    log("=" * 50)
    
    # 记录安装结果
    results = []
    installed_skills = []
    
    for schedule_time in RETRY_SCHEDULE:
        log(f"\n⏰ 计划重试时间: {schedule_time}")
        
        # 等待到目标时间
        if not wait_until(schedule_time):
            log("跳过已过时的计划")
            continue
        
        # 尝试安装games
        log(f"\n🔄 第{RETRY_SCHEDULE.index(schedule_time)+1}次重试开始")
        
        success_games, detail_games = try_install("games")
        if success_games:
            installed_skills.append("games")
            results.append({
                "time": schedule_time,
                "skill": "games",
                "success": True,
                "detail": "安装成功"
            })
            # 成功安装一个后继续尝试另一个
            time.sleep(5)  # 短暂等待
            
            success_joke, detail_joke = try_install("joke-teller")
            if success_joke:
                installed_skills.append("joke-teller")
                results.append({
                    "time": schedule_time,
                    "skill": "joke-teller",
                    "success": True,
                    "detail": "安装成功"
                })
            else:
                results.append({
                    "time": schedule_time,
                    "skill": "joke-teller",
                    "success": False,
                    "detail": detail_joke[:100]
                })
            
            # 如果成功安装至少一个，考虑停止
            if len(installed_skills) >= 1:
                log(f"✅ 成功安装 {len(installed_skills)} 个技能，继续后续重试...")
        else:
            results.append({
                "time": schedule_time,
                "skill": "games",
                "success": False,
                "detail": detail_games[:100]
            })
            
            # 即使games失败，也尝试joke-teller
            time.sleep(5)
            success_joke, detail_joke = try_install("joke-teller")
            if success_joke:
                installed_skills.append("joke-teller")
                results.append({
                    "time": schedule_time,
                    "skill": "joke-teller",
                    "success": True,
                    "detail": "安装成功"
                })
            else:
                results.append({
                    "time": schedule_time,
                    "skill": "joke-teller",
                    "success": False,
                    "detail": detail_joke[:100]
                })
        
        # 检查是否应该提前结束
        if len(installed_skills) >= 2:
            log("🎉 已成功安装所有目标技能！")
            break
    
    # 生成最终报告
    log("\n" + "=" * 50)
    log("📊 定时重试最终报告")
    log(f"总重试次数: {len(RETRY_SCHEDULE)}")
    log(f"成功安装技能数: {len(installed_skills)}")
    
    if installed_skills:
        log(f"✅ 已安装技能: {', '.join(installed_skills)}")
        log("\n🎉 原版技能安装成功！")
        log("建议：现在可以使用原版技能，本地集成版作为备用")
    else:
        log("❌ 所有重试均失败")
        log("\n💡 建议：")
        log("1. 继续使用本地集成版Fun Skills技能")
        log("2. 明天再尝试安装原版技能")
        log("3. 本地技能位置: /Users/jiyingguo/.openclaw/workspace/fun-skills/")
    
    # 保存结果到文件
    report_file = "/Users/jiyingguo/.openclaw/workspace/fun_skills_install_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Fun Skills 安装重试报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 重试时间表\n")
        f.write("- " + "\n- ".join(RETRY_SCHEDULE) + "\n\n")
        f.write("## 安装结果\n")
        for r in results:
            status = "✅ 成功" if r["success"] else "❌ 失败"
            f.write(f"- **{r['time']}** - {r['skill']}: {status}\n")
            if not r["success"]:
                f.write(f"  错误: {r['detail']}\n")
    
    log(f"\n📄 详细报告已保存: {report_file}")
    
    # 返回成功状态
    return len(installed_skills) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)