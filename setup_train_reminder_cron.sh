#!/bin/bash
# 火车票购买提醒 Cron 设置脚本
# 提醒时间: 2026-03-30 10:00, 12:00, 15:00, 18:00

SCRIPT_PATH="/Users/jiyingguo/.openclaw/workspace/send_train_ticket_reminder.py"
WORKSPACE="/Users/jiyingguo/.openclaw/workspace"
PYTHON_PATH="/usr/bin/python3"

# 日志文件
LOG_DIR="/Users/jiyingguo/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

echo "🚄 火车票购买提醒 Cron 设置"
echo "================================"
echo "提醒时间表:"
echo "  1. 2026-03-30 10:00 - 购买火车票"
echo "  2. 2026-03-30 12:00 - 购买火车票"
echo "  3. 2026-03-30 15:00 - 购买火车票"
echo "  4. 2026-03-30 18:00 - 购买火车票"
echo ""

# 先删除旧的火车票提醒 cron 条目（如果存在）
crontab -l 2>/dev/null | grep -v "train_ticket_reminder" > /tmp/current_cron.tmp

# 添加新的 cron 条目
# 格式: minute hour day-of-month month day-of-week command

# 2026-03-30 10:00
echo "0 10 30 3 * cd $WORKSPACE && $PYTHON_PATH $SCRIPT_PATH \"10:00\" >> $LOG_DIR/train_reminder_10_00.log 2>&1" >> /tmp/current_cron.tmp

# 2026-03-30 12:00
echo "0 12 30 3 * cd $WORKSPACE && $PYTHON_PATH $SCRIPT_PATH \"12:00\" >> $LOG_DIR/train_reminder_12_00.log 2>&1" >> /tmp/current_cron.tmp

# 2026-03-30 15:00
echo "0 15 30 3 * cd $WORKSPACE && $PYTHON_PATH $SCRIPT_PATH \"15:00\" >> $LOG_DIR/train_reminder_15_00.log 2>&1" >> /tmp/current_cron.tmp

# 2026-03-30 18:00
echo "0 18 30 3 * cd $WORKSPACE && $PYTHON_PATH $SCRIPT_PATH \"18:00\" >> $LOG_DIR/train_reminder_18_00.log 2>&1" >> /tmp/current_cron.tmp

# 安装新的 crontab
crontab /tmp/current_cron.tmp
rm /tmp/current_cron.tmp

echo "✅ Cron 任务已设置!"
echo ""
echo "当前 Cron 条目:"
crontab -l | grep "train_ticket_reminder"
echo ""
echo "日志将保存到: $LOG_DIR/train_reminder_*.log"
