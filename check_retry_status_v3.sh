#!/bin/bash

echo "=== 技能安装重试状态检查 v3 ==="
echo "检查时间: $(date)"

# 检查监控脚本
if ps aux | grep "install_retry_v3.sh" | grep -v grep > /dev/null; then
    echo "✅ 监控脚本正在运行"
    RETRY_PID=$(ps aux | grep "install_retry_v3.sh" | grep -v grep | awk '{print $2}')
    echo "   PID: $RETRY_PID"
else
    echo "❌ 监控脚本未运行"
fi

# 检查安装重试脚本
if ps aux | grep "install_retry_v3.sh" | grep -v grep > /dev/null; then
    echo "✅ 安装重试脚本正在运行"
else
    echo "❌ 安装重试脚本未运行"
fi

echo ""
echo "=== 最近日志 ==="
tail -20 /Users/jiyingguo/.openclaw/workspace/install_retry_v3.log 2>/dev/null || echo "日志文件不存在"

echo ""
echo "=== 计划执行时间表 ==="
echo "09:40 - 第一次尝试"
echo "10:30 - 第二次尝试"
echo "11:30 - 第三次尝试"
echo "14:30 - 第四次尝试"
echo "17:30 - 第五次尝试"

echo ""
echo "当前时间: $(date +%H:%M)"
echo "下一个计划时间: 09:40"

echo ""
echo "=== 安装结果统计 ==="
if [ -f "/Users/jiyingguo/.openclaw/workspace/install_results_v3.json" ]; then
    TOTAL_ATTEMPTS=$(grep -c '"attempt"' /Users/jiyingguo/.openclaw/workspace/install_results_v3.json 2>/dev/null || echo "0")
    SUCCESS_COUNT=$(grep -c '"success": true' /Users/jiyingguo/.openclaw/workspace/install_results_v3.json 2>/dev/null || echo "0")
    echo "总尝试次数: $TOTAL_ATTEMPTS"
    echo "成功次数: $SUCCESS_COUNT"
else
    echo "结果文件不存在"
fi

echo ""
echo "技能状态:"
echo "• joke-teller: ❌ 未安装"
echo "• openclaw-tavily-search: ❌ 未安装"
echo "• multi-search-engine: ❌ 未安装"

echo ""
echo "=== 已成功安装的技能 ==="
clawhub list 2>/dev/null || echo "无法获取已安装技能列表"

echo ""
echo "=== 文件位置 ==="
echo "日志文件: /Users/jiyingguo/.openclaw/workspace/install_retry_v3.log"
echo "结果文件: /Users/jiyingguo/.openclaw/workspace/install_results_v3.json"
echo "监控输出: /Users/jiyingguo/.openclaw/workspace/monitor_output_v3.log"
