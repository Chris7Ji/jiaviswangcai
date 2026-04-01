#!/usr/bin/env python3
"""
每日工作日报生成任务
每天早上9点生成昨日工作日报
"""
import os
import sys
import json
from datetime import datetime, timedelta

def generate_daily_report():
    """生成工作日报"""
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y年%m月%d日")
    today = datetime.now().strftime("%Y年%m月%d日")
    
    report = f"""# 📋 每日工作日报

> **日期**：{yesterday}  
> **生成时间**：{today} 09:00  
> **生成者**：旺财Jarvis

---

## 📊 昨日工作概览

### ✅ 已完成任务
- [待从session历史中提取]

### 📚 学习收获
- [待从对话记录中提取]

### 🔍 复盘反思
- [待分析]

### 💡 建议反馈
- [待生成]

---

## 📈 数据统计

| 指标 | 数值 |
|------|------|
| 完成任务数 | - |
| 学习时长 | - |
| 新技能掌握 | - |

---

## 🎯 今日计划

- [ ] 待制定

---

*本报告由OpenClaw大龙虾智能助手自动生成*  
*数据来源：Session历史记录*
"""
    
    return report

def send_report():
    """发送日报"""
    report = generate_daily_report()
    
    # 保存文件
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"/tmp/daily_report_{today}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 日报已生成: {filename}")
    print("⚠️ 注意：此为基础模板，需要从session历史中提取实际工作内容")
    
    return filename

if __name__ == "__main__":
    send_report()