#!/bin/bash
# 每日工作成长日记生成 + js/diary.js 同步脚本
# 此脚本应在每日cron任务中运行，先执行日记生成，再同步diary.js

SCRIPT_DIR="/Users/jiyingguo/.openclaw/workspace/scripts"
WEBSITE_DIR="/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai"

echo "========== $(date) =========="
echo "📝 开始生成每日成长日记..."

# 说明：这里的日记生成逻辑由OpenClaw cron任务触发
# 此脚本主要用于在日记生成后同步 js/diary.js

# 步骤1: 同步 js/diary.js (从 post.html 读取最新日记)
echo "[1/1] 同步 js/diary.js..."
python3 "$SCRIPT_DIR/sync_diary_js.py"

# 步骤2: 提交并推送更改
echo "[2/2] 提交并推送更改..."
cd "$WEBSITE_DIR" || exit 1
git add js/diary.js
git commit -m "fix: 自动同步 js/diary.js (由 run_daily_diary.sh 自动执行)" || echo "没有新内容需要提交"
git push

echo "✅ 每日成长日记同步完成!"
