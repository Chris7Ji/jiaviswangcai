# Workspace 脚本快捷调用参考
# 用于在移除裸命令后的安全脚本调用

## 调试与临时执行

# 快速运行Python代码
bash /Users/jiyingguo/.openclaw/workspace/scripts/run_python.sh "print('hello')"
bash /Users/jiyingguo/.openclaw/workspace/scripts/run_python.sh "import json; d={'a':1}; print(json.dumps(d, ensure_ascii=False))"

## 12306火车票查询

# 完整命令（需用完整路径）
node /Users/jiyingguo/.openclaw/workspace/skills/12306/scripts/query.mjs 上海 北京 2026-04-30

# 快捷脚本
bash /Users/jiyingguo/.openclaw/workspace/scripts/12306.sh 上海 北京 2026-04-30

## 常用脚本调用

# 发送AI新闻
python3 /Users/jiyingguo/.openclaw/workspace/scripts/send_daily_ai_news_real.py

# 每日祝福
bash /Users/jiyingguo/.openclaw/workspace/scripts/daily_blessing.sh

# Git推送网站
git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai status
git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai add .
git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai commit -m "更新"
git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai push

# 健康日报
python3 /Users/jiyingguo/.openclaw/workspace/scripts/health_longevity_monitor.sh

# GitHub操作
git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai push

## 重要路径速查

WORKSPACE=/Users/jiyingguo/.openclaw/workspace
WEBSITE=/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai
SCRIPTS=/Users/jiyingguo/.openclaw/workspace/scripts
SKILLS=/Users/jiyingguo/.openclaw/workspace/skills
NEWS=/Users/jiyingguo/.openclaw/workspace/news_data
