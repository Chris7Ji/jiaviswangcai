#!/bin/bash

# 监控脚本 v2 - 启动安装重试并监控进度

echo "🚀 启动技能安装重试监控系统 v2"
echo "=========================================="

# 检查是否已有实例在运行
if ps aux | grep "install_retry_v2.sh" | grep -v grep > /dev/null; then
    echo "⚠️  检测到已有重试脚本在运行"
    read -p "是否停止现有实例并重新启动? (y/n): " choice
    if [ "$choice" != "y" ]; then
        echo "取消操作"
        exit 0
    fi
    pkill -f "install_retry_v2.sh"
    sleep 2
fi

# 设置日志文件
MONITOR_LOG="/Users/jiyingguo/.openclaw/workspace/monitor_output.log"
echo "=== 监控启动时间: $(date) ===" > "$MONITOR_LOG"

# 显示要安装的技能
echo "" | tee -a "$MONITOR_LOG"
echo "📋 本次重试安装的技能:" | tee -a "$MONITOR_LOG"
echo "1. games - 游戏娱乐功能" | tee -a "$MONITOR_LOG"
echo "2. joke-teller - 笑话生成器" | tee -a "$MONITOR_LOG"
echo "3. openclaw-tavily-search - Tavily搜索 (备选: tavily-tool)" | tee -a "$MONITOR_LOG"

# 显示执行计划
echo "" | tee -a "$MONITOR_LOG"
echo "⏰ 执行计划时间表:" | tee -a "$MONITOR_LOG"
echo "09:30 - 第一次尝试" | tee -a "$MONITOR_LOG"
echo "10:30 - 第二次尝试" | tee -a "$MONITOR_LOG"
echo "11:30 - 第三次尝试" | tee -a "$MONITOR_LOG"
echo "14:30 - 第四次尝试" | tee -a "$MONITOR_LOG"
echo "17:30 - 第五次尝试" | tee -a "$MONITOR_LOG"

# 启动重试脚本（后台运行）
echo "" | tee -a "$MONITOR_LOG"
echo "🚀 启动安装重试脚本..." | tee -a "$MONITOR_LOG"
nohup bash /Users/jiyingguo/.openclaw/workspace/install_retry_v2.sh >> "$MONITOR_LOG" 2>&1 &
RETRY_PID=$!

echo "✅ 重试脚本已启动 (PID: $RETRY_PID)" | tee -a "$MONITOR_LOG"
echo "📁 监控日志: $MONITOR_LOG" | tee -a "$MONITOR_LOG"
echo "📁 安装日志: /Users/jiyingguo/.openclaw/workspace/install_retry.log" | tee -a "$MONITOR_LOG"
echo "📁 结果文件: /Users/jiyingguo/.openclaw/workspace/install_results.json" | tee -a "$MONITOR_LOG"

# 显示当前状态
echo "" | tee -a "$MONITOR_LOG"
echo "📊 当前状态:" | tee -a "$MONITOR_LOG"
echo "- 脚本PID: $RETRY_PID" | tee -a "$MONITOR_LOG"
echo "- 开始时间: $(date)" | tee -a "$MONITOR_LOG"
echo "- 下一个计划时间: 09:30" | tee -a "$MONITOR_LOG"

# 创建状态检查脚本
cat > /Users/jiyingguo/.openclaw/workspace/check_retry_status_v2.sh << 'EOF'
#!/bin/bash

echo "=== 技能安装重试状态检查 v2 ==="
echo "检查时间: $(date)"

# 检查监控脚本
if ps aux | grep "install_retry_v2.sh" | grep -v grep > /dev/null; then
    echo "✅ 监控脚本正在运行"
    RETRY_PID=$(ps aux | grep "install_retry_v2.sh" | grep -v grep | awk '{print $2}')
    echo "   PID: $RETRY_PID"
else
    echo "❌ 监控脚本未运行"
fi

# 检查安装重试脚本
if ps aux | grep "install_retry_v2.sh" | grep -v grep > /dev/null; then
    echo "✅ 安装重试脚本正在运行"
else
    echo "❌ 安装重试脚本未运行"
fi

echo ""
echo "=== 最近日志 ==="
tail -20 /Users/jiyingguo/.openclaw/workspace/install_retry.log 2>/dev/null || echo "日志文件不存在"

echo ""
echo "=== 计划执行时间表 ==="
echo "09:30 - 第一次尝试"
echo "10:30 - 第二次尝试"
echo "11:30 - 第三次尝试"
echo "14:30 - 第四次尝试"
echo "17:30 - 第五次尝试"

echo ""
echo "当前时间: $(date +%H:%M)"
echo "下一个计划时间: 09:30"

echo ""
echo "=== 安装结果统计 ==="
if [ -f "/Users/jiyingguo/.openclaw/workspace/install_results.json" ]; then
    TOTAL_ATTEMPTS=$(grep -c '"attempt"' /Users/jiyingguo/.openclaw/workspace/install_results.json 2>/dev/null || echo "0")
    SUCCESS_COUNT=$(grep -c '"success": true' /Users/jiyingguo/.openclaw/workspace/install_results.json 2>/dev/null || echo "0")
    echo "总尝试次数: $TOTAL_ATTEMPTS"
    echo "成功次数: $SUCCESS_COUNT"
else
    echo "结果文件不存在"
fi

echo ""
echo "技能状态:"
echo "• games: ❌ 未安装"
echo "• joke-teller: ❌ 未安装"
echo "• openclaw-tavily-search: ❌ 未安装"

echo ""
echo "=== 文件位置 ==="
echo "日志文件: /Users/jiyingguo/.openclaw/workspace/install_retry.log"
echo "结果文件: /Users/jiyingguo/.openclaw/workspace/install_results.json"
echo "监控输出: /Users/jiyingguo/.openclaw/workspace/monitor_output.log"
EOF

chmod +x /Users/jiyingguo/.openclaw/workspace/check_retry_status_v2.sh

echo "" | tee -a "$MONITOR_LOG"
echo "📝 状态检查命令:" | tee -a "$MONITOR_LOG"
echo "bash /Users/jiyingguo/.openclaw/workspace/check_retry_status_v2.sh" | tee -a "$MONITOR_LOG"

echo "" | tee -a "$MONITOR_LOG"
echo "🎯 系统已启动完成!" | tee -a "$MONITOR_LOG"
echo "系统将在今天内自动重试安装所有技能。" | tee -a "$MONITOR_LOG"
echo "任何成功安装都会生成通知。" | tee -a "$MONITOR_LOG"

# 等待一段时间显示初始状态
sleep 3
echo "" | tee -a "$MONITOR_LOG"
echo "=== 初始状态检查 ===" | tee -a "$MONITOR_LOG"
bash /Users/jiyingguo/.openclaw/workspace/check_retry_status_v2.sh | tee -a "$MONITOR_LOG"

exit 0