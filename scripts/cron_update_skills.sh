#!/bin/bash
# 每天下午18点更新网站的全局状态与技能页面
cd /Users/jiyingguo/.openclaw/workspace

# 执行全局数据同步（包含更新技能树、运行天数、日志篇数、团队人数同步）
/usr/bin/env python3 /Users/jiyingguo/.openclaw/workspace/scripts/sync_site_data.py

cd /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai
git add .
git commit -m "Auto-sync site data (skills, posts, days) via cron"
git push
