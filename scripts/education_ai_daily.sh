#!/bin/bash
# 教育行业AI资讯日报定时任务脚本
# 每天早上8点执行

# 设置环境变量
export TAVILY_API_KEY="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"

# 执行Python脚本
python3 /Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.py >> /tmp/education_ai_cron.log 2>&1

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 教育AI日报任务执行成功" >> /tmp/education_ai_cron.log
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 教育AI日报任务执行失败" >> /tmp/education_ai_cron.log
fi