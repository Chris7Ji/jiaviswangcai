#!/bin/bash

# 安装重试脚本
# 按照时间表重试安装games和joke-teller技能

LOG_FILE="/Users/jiyingguo/.openclaw/workspace/install_retry.log"
RESULT_FILE="/Users/jiyingguo/.openclaw/workspace/install_results.json"
SKILLS=("games" "joke-teller")
SCHEDULE=("09:30" "10:30" "11:30" "14:30" "17:30")

# 初始化日志文件
echo "=== 技能安装重试日志 $(date) ===" > "$LOG_FILE"
echo "[" > "$RESULT_FILE"

# 检查clawhub是否安装
if ! command -v clawhub &> /dev/null; then
    echo "错误: clawhub CLI未安装" | tee -a "$LOG_FILE"
    exit 1
fi

# 函数：尝试安装技能
install_skill() {
    local skill=$1
    local attempt=$2
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    
    echo "[$timestamp] 尝试安装技能: $skill (第$attempt次)" | tee -a "$LOG_FILE"
    
    # 尝试安装
    local output=$(clawhub install "$skill" 2>&1)
    local exit_code=$?
    
    # 记录结果
    local result_entry="{\"timestamp\": \"$timestamp\", \"skill\": \"$skill\", \"attempt\": $attempt, \"success\": $([ $exit_code -eq 0 ] && echo true || echo false), \"output\": \"${output//\"/\\\"}\"}"
    
    echo "$result_entry" >> "$LOG_FILE"
    echo "$result_entry," >> "$RESULT_FILE"
    
    if [ $exit_code -eq 0 ]; then
        echo "[$timestamp] ✓ 成功安装: $skill" | tee -a "$LOG_FILE"
        return 0
    else
        echo "[$timestamp] ✗ 安装失败: $skill" | tee -a "$LOG_FILE"
        echo "错误输出: $output" | tee -a "$LOG_FILE"
        return 1
    fi
}

# 函数：等待到指定时间
wait_until() {
    local target_time=$1
    local current_time=$(date +%H:%M)
    local target_seconds=$(date -j -f "%H:%M" "$target_time" +%s 2>/dev/null || date -d "$target_time" +%s)
    local current_seconds=$(date -j -f "%H:%M" "$current_time" +%s 2>/dev/null || date -d "$current_time" +%s)
    
    if [ "$target_seconds" -gt "$current_seconds" ]; then
        local wait_seconds=$((target_seconds - current_seconds))
        echo "等待 $wait_seconds 秒直到 $target_time..." | tee -a "$LOG_FILE"
        sleep $wait_seconds
    else
        echo "目标时间 $target_time 已过，立即执行..." | tee -a "$LOG_FILE"
    fi
}

# 主循环
attempt_count=0
success_count=0
failed_skills=("${SKILLS[@]}")

for schedule_time in "${SCHEDULE[@]}"; do
    echo "" | tee -a "$LOG_FILE"
    echo "=== 计划执行时间: $schedule_time ===" | tee -a "$LOG_FILE"
    
    # 等待到计划时间
    wait_until "$schedule_time"
    
    # 尝试安装所有未成功的技能
    remaining_skills=()
    for skill in "${failed_skills[@]}"; do
        attempt_count=$((attempt_count + 1))
        if install_skill "$skill" "$attempt_count"; then
            success_count=$((success_count + 1))
            # 从失败列表中移除
            echo "✓ $skill 已成功安装，从重试列表中移除" | tee -a "$LOG_FILE"
        else
            remaining_skills+=("$skill")
        fi
    done
    
    # 更新失败技能列表
    failed_skills=("${remaining_skills[@]}")
    
    # 如果所有技能都安装成功，提前结束
    if [ ${#failed_skills[@]} -eq 0 ]; then
        echo "" | tee -a "$LOG_FILE"
        echo "🎉 所有技能安装成功！" | tee -a "$LOG_FILE"
        echo "总尝试次数: $attempt_count" | tee -a "$LOG_FILE"
        echo "成功技能数: $success_count" | tee -a "$LOG_FILE"
        break
    fi
    
    # 显示进度
    echo "" | tee -a "$LOG_FILE"
    echo "进度报告:" | tee -a "$LOG_FILE"
    echo "- 已成功: $success_count/${#SKILLS[@]}" | tee -a "$LOG_FILE"
    echo "- 仍需重试: ${failed_skills[*]}" | tee -a "$LOG_FILE"
    echo "- 下一个计划时间: $(echo "${SCHEDULE[@]}" | tr ' ' '\n' | grep -A1 "$schedule_time" | tail -n1 || echo "无")" | tee -a "$LOG_FILE"
done

# 最终结果
echo "" | tee -a "$LOG_FILE"
echo "=== 最终结果 ===" | tee -a "$LOG_FILE"
echo "总尝试次数: $attempt_count" | tee -a "$LOG_FILE"
echo "成功安装: $success_count/${#SKILLS[@]}" | tee -a "$LOG_FILE"

if [ ${#failed_skills[@]} -gt 0 ]; then
    echo "安装失败的技能: ${failed_skills[*]}" | tee -a "$LOG_FILE"
fi

# 完成JSON结果文件
sed -i '' '$ s/,$//' "$RESULT_FILE"  # 移除最后一个逗号
echo "]" >> "$RESULT_FILE"

echo "日志文件: $LOG_FILE" | tee -a "$LOG_FILE"
echo "结果文件: $RESULT_FILE" | tee -a "$LOG_FILE"

# 如果有成功安装的技能，发送通知
if [ $success_count -gt 0 ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "📢 准备发送通知到主会话..." | tee -a "$LOG_FILE"
    # 这里可以添加发送通知的代码
fi

exit 0