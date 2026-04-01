#!/bin/bash
# 第3天安装脚本

echo "========================================"
echo "📅 第3天安装 (10个技能)"
echo "========================================"

SKILLS=(typescript firebase feishu audio-processing notes react vue webpack jest eslint)
DELAY=30
LOG_FILE="/Users/jiyingguo/.openclaw/workspace/logs/day3_$(date '+%Y%m%d_%H%M%S').log"

echo "开始时间: $(date)" | tee -a "$LOG_FILE"
echo "技能列表: ${SKILLS[*]}" | tee -a "$LOG_FILE"
echo "=" * 50 | tee -a "$LOG_FILE"

for i in "${!SKILLS[@]}"; do
    skill="${SKILLS[$i]}"
    echo "[$((i+1))/${#SKILLS[@]}] 安装: $skill" | tee -a "$LOG_FILE"
    
    # 检查是否已安装
    if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/$skill" ]; then
        echo "✅ $skill 已安装，跳过" | tee -a "$LOG_FILE"
        continue
    fi
    
    # 安装技能
    if clawhub install "$skill" 2>&1 | tee -a "$LOG_FILE"; then
        echo "✅ $skill 安装成功" | tee -a "$LOG_FILE"
    else
        echo "❌ $skill 安装失败" | tee -a "$LOG_FILE"
        echo "错误信息已记录到日志" | tee -a "$LOG_FILE"
    fi
    
    # 不是最后一个技能则等待
    if [ $i -lt $((${#SKILLS[@]}-1)) ]; then
        echo "等待 ${DELAY}秒避免速率限制..." | tee -a "$LOG_FILE"
        sleep $DELAY
    fi
done

echo "=" * 50 | tee -a "$LOG_FILE"
echo "第3天安装完成" | tee -a "$LOG_FILE"
echo "完成时间: $(date)" | tee -a "$LOG_FILE"

# 生成报告
INSTALLED_COUNT=$(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ | wc -l)
echo "当前技能总数: $INSTALLED_COUNT" | tee -a "$LOG_FILE"
echo "距离100目标还差: $((100 - INSTALLED_COUNT))" | tee -a "$LOG_FILE"
