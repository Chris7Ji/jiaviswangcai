# 教育行业AI资讯日报 - 定时任务配置指南

## 📋 任务说明

**任务名称**：教育行业AI资讯日报  
**执行时间**：每天早上8:00  
**任务内容**：
1. 搜集中国教育部、教育行业AI教育教学相关内容
2. 精选10条重要资讯
3. 验证真实性和有效性
4. 整理成摘要报告
5. 发送到QQ邮箱、华为邮箱

---

## 🚀 配置步骤

### 步骤1：确认文件已创建

已创建以下文件：
- ✅ Python脚本：`/Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.py`
- ✅ Shell脚本：`/Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.sh`
- ✅ 配置指南：`/Users/jiyingguo/.openclaw/workspace/scripts/cron_setup.txt`

### 步骤2：手动执行测试

**请先测试脚本是否正常工作**：

```bash
# 设置环境变量
export TAVILY_API_KEY="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"

# 执行脚本
python3 /Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.py
```

### 步骤3：配置定时任务

**方法A：使用crontab（推荐）**

```bash
# 编辑crontab
crontab -e

# 添加以下行（每天早上8点执行）
0 8 * * * /Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.sh

# 保存退出
```

**方法B：使用launchd（macOS推荐）**

创建plist文件：
```bash
cat > ~/Library/LaunchAgents/com.openclaw.education-ai.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.education-ai</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/education_ai_out.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/education_ai_err.log</string>
</dict>
</plist>
EOF

# 加载任务
launchctl load ~/Library/LaunchAgents/com.openclaw.education-ai.plist

# 查看任务状态
launchctl list | grep com.openclaw.education-ai
```

### 步骤4：验证配置

```bash
# 查看crontab
crontab -l

# 手动触发测试
/Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.sh

# 查看日志
tail -f /tmp/education_ai_cron.log
```

---

## 📊 任务功能

### 搜索范围
- 中国教育部官网
- 教育行业权威媒体
- AI教育相关政策
- K12人工智能课程
- 智慧教育应用

### 验证标准
- ✅ 来源权威性（政府网站、权威媒体）
- ✅ 内容时效性（24小时内）
- ✅ 信息准确性（交叉验证）
- ✅ 相关性（AI教育主题）

### 输出格式
- 精选10条重要资讯
- 每条包含：标题、摘要、来源链接
- 可信度标记
- 行业洞察和趋势分析

### 发送渠道
- 📧 QQ邮箱：86940135@qq.com
- 📧 华为邮箱：jiyingguo@huawei.com

---

## 🔧 管理任务

### 查看任务状态
```bash
# crontab方式
crontab -l

# launchd方式
launchctl list | grep education-ai
```

### 删除任务
```bash
# crontab方式
crontab -e
# 删除对应行

# launchd方式
launchctl unload ~/Library/LaunchAgents/com.openclaw.education-ai.plist
rm ~/Library/LaunchAgents/com.openclaw.education-ai.plist
```

### 修改执行时间
```bash
# crontab方式（编辑crontab修改时间）
crontab -e

# launchd方式（编辑plist文件）
# 修改Hour和Minute值
```

---

## 📁 文件位置

| 文件 | 路径 |
|------|------|
| Python脚本 | `/Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.py` |
| Shell脚本 | `/Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.sh` |
| 日志文件 | `/tmp/education_ai_cron.log` |
| 日报输出 | `/tmp/education_ai_news_YYYY-MM-DD.md` |

---

## ⚠️ 注意事项

1. **API配额**：Tavily免费版每月1000次搜索，每日约30次
2. **网络连接**：需要稳定的网络连接
3. **邮箱配置**：确保QQ邮箱授权码有效
4. **日志查看**：定期检查日志排查问题

---

## 🆘 故障排查

### 任务未执行
1. 检查crontab/launchd配置是否正确
2. 查看日志文件：`tail /tmp/education_ai_cron.log`
3. 手动执行测试：`bash /Users/jiyingguo/.openclaw/workspace/scripts/education_ai_daily.sh`

### 邮件未发送
1. 检查QQ邮箱授权码是否过期
2. 检查网络连接
3. 查看邮件发送日志

### 搜索结果为空
1. 检查TAVILY_API_KEY是否有效
2. 检查API配额是否用完
3. 调整搜索关键词

---

**配置完成时间**：2026年3月18日  
**配置者**：旺财Jarvis