#!/bin/bash

# 状态检查脚本

SCRIPT_DIR="/Users/jiyingguo/.openclaw/workspace"
LOG_FILE="$SCRIPT_DIR/install_retry.log"
PID_FILE="$SCRIPT_DIR/retry_monitor.pid"
RESULT_FILE="$SCRIPT_DIR/install_results.json"

echo "=== 技能安装重试状态检查 ==="
echo "检查时间: $(date)"
echo ""

# 检查进程状态
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
        echo "✅ 监控脚本正在运行 (PID: $pid)"
        
        # 检查安装重试脚本
        retry_pid=$(ps aux | grep install_retry.sh | grep -v grep | awk '{print $2}')
        if [ -n "$retry_pid" ]; then
            echo "✅ 安装重试脚本正在运行 (PID: $retry_pid)"
        else
            echo "❌ 安装重试脚本未运行"
        fi
    else
        echo "❌ PID文件存在但进程未运行"
        rm -f "$PID_FILE"
    fi
else
    echo "❌ 监控脚本未运行"
fi

echo ""

# 显示日志最后几行
if [ -f "$LOG_FILE" ]; then
    echo "=== 最近日志 ==="
    tail -20 "$LOG_FILE"
else
    echo "日志文件不存在"
fi

echo ""

# 显示计划时间
echo "=== 计划执行时间表 ==="
echo "09:30 - 第一次尝试"
echo "10:30 - 第二次尝试"
echo "11:30 - 第三次尝试"
echo "14:30 - 第四次尝试"
echo "17:30 - 第五次尝试"

echo ""

# 显示当前时间
current_time=$(date +%H:%M)
echo "当前时间: $current_time"

# 计算到下一个计划时间
schedule_times=("09:30" "10:30" "11:30" "14:30" "17:30")
next_time=""

for time in "${schedule_times[@]}"; do
    if [[ "$time" > "$current_time" ]]; then
        next_time="$time"
        break
    fi
done

if [ -n "$next_time" ]; then
    # 计算等待时间
    current_seconds=$(date -j -f "%H:%M" "$current_time" +%s)
    next_seconds=$(date -j -f "%H:%M" "$next_time" +%s)
    wait_seconds=$((next_seconds - current_seconds))
    wait_minutes=$((wait_seconds / 60))
    
    echo "下一个计划时间: $next_time (约${wait_minutes}分钟后)"
else
    echo "所有计划时间已过"
fi

echo ""

# 检查结果文件
if [ -f "$RESULT_FILE" ]; then
    echo "=== 安装结果统计 ==="
    
    # 简单统计
    total=$(grep -c '"skill"' "$RESULT_FILE" 2>/dev/null || echo "0")
    success=$(grep -c '"success": true' "$RESULT_FILE" 2>/dev/null || echo "0")
    
    echo "总尝试次数: $total"
    echo "成功次数: $success"
    
    # 显示技能状态
    echo ""
    echo "技能状态:"
    if grep -q '"skill": "games"' "$RESULT_FILE" && grep -q '"skill": "games".*"success": true' "$RESULT_FILE"; then
        echo "• games: ✅ 已安装"
    else
        echo "• games: ❌ 未安装"
    fi
    
    if grep -q '"skill": "joke-teller"' "$RESULT_FILE" && grep -q '"skill": "joke-teller".*"success": true' "$RESULT_FILE"; then
        echo "• joke-teller: ✅ 已安装"
    else
        echo "• joke-teller: ❌ 未安装"
    fi
fi

echo ""
echo "=== 文件位置 ==="
echo "日志文件: $LOG_FILE"
echo "结果文件: $RESULT_FILE"
echo "监控输出: $SCRIPT_DIR/monitor_output.log"