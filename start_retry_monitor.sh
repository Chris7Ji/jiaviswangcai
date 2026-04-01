#!/bin/bash

# 监控脚本 - 启动安装重试并在完成后发送通知

SCRIPT_DIR="/Users/jiyingguo/.openclaw/workspace"
RETRY_SCRIPT="$SCRIPT_DIR/install_retry.sh"
LOG_FILE="$SCRIPT_DIR/install_retry.log"
PID_FILE="$SCRIPT_DIR/retry_monitor.pid"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
        echo "监控脚本已在运行 (PID: $pid)"
        exit 0
    else
        echo "发现旧的PID文件，清理..."
        rm "$PID_FILE"
    fi
fi

# 启动安装重试脚本
echo "启动技能安装重试监控..."
echo "当前时间: $(date)"
echo "计划执行时间: 09:30, 10:30, 11:30, 14:30, 17:30"
echo "目标技能: games, joke-teller"
echo "日志文件: $LOG_FILE"
echo ""

# 在后台运行安装重试脚本
nohup "$RETRY_SCRIPT" > "$SCRIPT_DIR/retry_output.log" 2>&1 &
RETRY_PID=$!

# 保存PID
echo $RETRY_PID > "$PID_FILE"
echo "安装重试脚本已启动 (PID: $RETRY_PID)"

# 等待进程结束
wait $RETRY_PID
RETRY_EXIT=$?

# 清理PID文件
rm -f "$PID_FILE"

echo ""
echo "安装重试脚本执行完成，退出码: $RETRY_EXIT"
echo ""

# 检查结果并准备通知
if [ -f "$SCRIPT_DIR/install_results.json" ]; then
    echo "分析安装结果..."
    
    # 使用Python解析JSON结果
    python3 << 'EOF'
import json
import os
import sys

result_file = "/Users/jiyingguo/.openclaw/workspace/install_results.json"
if not os.path.exists(result_file):
    print("结果文件不存在")
    sys.exit(1)

with open(result_file, 'r') as f:
    try:
        results = json.load(f)
    except json.JSONDecodeError:
        print("无法解析JSON文件")
        sys.exit(1)

# 统计结果
total_attempts = len(results)
successful_installs = {}
failed_skills = set()

for result in results:
    skill = result.get('skill', 'unknown')
    if result.get('success', False):
        successful_installs[skill] = successful_installs.get(skill, 0) + 1
    else:
        failed_skills.add(skill)

# 生成摘要
print("=== 安装结果摘要 ===")
print(f"总尝试次数: {total_attempts}")
print(f"成功安装的技能: {list(successful_installs.keys())}")
print(f"失败的技能: {list(failed_skills)}")

# 生成通知消息
notification = "📢 技能安装重试完成\n\n"
notification += f"📊 统计信息:\n"
notification += f"• 总尝试次数: {total_attempts}\n"
notification += f"• 成功安装: {len(successful_installs)}/2\n"

if successful_installs:
    notification += f"\n✅ 成功安装的技能:\n"
    for skill, count in successful_installs.items():
        notification += f"• {skill} (尝试{count}次)\n"

if failed_skills:
    notification += f"\n❌ 安装失败的技能:\n"
    for skill in failed_skills:
        notification += f"• {skill}\n"

notification += f"\n📋 详细日志: {result_file}"

print("\n=== 通知消息 ===")
print(notification)

# 保存通知消息到文件
with open("/Users/jiyingguo/.openclaw/workspace/notification.txt", "w") as f:
    f.write(notification)
EOF

    echo ""
    echo "通知消息已保存到: $SCRIPT_DIR/notification.txt"
    
    # 这里可以添加发送通知的代码
    # 例如: message send --channel "主会话" --message "$(cat $SCRIPT_DIR/notification.txt)"
    
else
    echo "未找到结果文件，无法生成通知"
fi

echo ""
echo "监控脚本执行完成"