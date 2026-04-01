# 华为邮箱兼容的AI新闻简报定时任务配置

## 任务名称
高校分队-AI新闻每日简报（华为邮箱兼容版）

## 执行时间
每天 06:15 (北京时间)

## 任务内容
```bash
# 1. 生成AI新闻简报HTML
# 2. 使用华为邮箱兼容脚本发送
python3 /Users/jiyingguo/.openclaw/workspace/scripts/huawei_compatible_sender.py < /Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_brief_$(date +%Y-%m-%d).html
```

## 邮件格式要求
1. **主题格式**：`[日期] 高校分队- AI 新闻每日简报：[最重磅新闻标题]`
2. **HTML格式**：
   - 无emoji
   - 纯色背景
   - 简洁CSS
   - 无渐变色、阴影、动画
3. **收件人**：
   - jiyingguo@huawei.com
   - xushengsheng@huawei.com
   - 86940135@qq.com

## 验证方法
1. 检查华为邮箱是否收到邮件
2. 检查邮件是否在垃圾邮件箱
3. 确认邮件格式正确（无emoji）

## 问题排查
如果华为邮箱仍收不到邮件：
1. 检查华为邮箱白名单设置
2. 联系华为邮箱管理员
3. 尝试纯文本格式邮件