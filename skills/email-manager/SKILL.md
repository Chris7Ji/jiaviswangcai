# 📧 邮件管理技能

## 概述
超级助理邮件管理技能，支持QQ邮箱和华为邮箱的IMAP/SMTP管理。

## 功能特性

### ✅ 已实现功能
- 获取未读邮件数量
- 列出最近邮件
- 发送邮件
- 支持多邮箱账户（QQ + 华为）

### 📝 使用方法

#### 1. 检查未读邮件
```bash
python3 skills/email-manager/email_manager.py unread qq
python3 skills/email-manager/email_manager.py unread huawei
```

#### 2. 列出最近邮件
```bash
# 列出最近10封邮件
python3 skills/email-manager/email_manager.py list qq

# 列出最近5封邮件
python3 skills/email-manager/email_manager.py list qq 5
```

#### 3. 发送邮件
```bash
python3 skills/email-manager/email_manager.py send "收件人邮箱" "主题" "正文"
```

### 💬 自然语言指令

可以直接对我说：
- "检查未读邮件"
- "列出最近邮件"
- "发送邮件给xxx"

## 配置说明

### 环境变量
```bash
export QQ_EMAIL_PASSWORD="swqfjvmoupdebhgh"
export HUAWEI_EMAIL_PASSWORD="your_huawei_password"
```

### 邮箱配置

#### QQ邮箱（已配置）
- 邮箱: 86940135@qq.com
- IMAP: imap.qq.com:993
- SMTP: smtp.qq.com:587
- 授权码: 已配置

#### 华为邮箱（待配置）
- 邮箱: jiyingguo@huawei.com
- IMAP: imap.huawei.com:993（待确认）
- SMTP: smtp.huawei.com:587（待确认）
- 密码: 需要提供

## 使用场景

### 场景1: 每日邮件检查
```
用户: 检查今天的邮件
助手: 检查QQ邮箱和华为邮箱的未读邮件...
```

### 场景2: 重要邮件提醒
```
用户: 有没有重要邮件
助手: 检查未读邮件并摘要重要内容...
```

### 场景3: 快速回复
```
用户: 回复这封邮件说"收到，谢谢"
助手: 生成回复并发送...
```

## 待完善功能

- [ ] 邮件智能分类
- [ ] 自动摘要长邮件
- [ ] VIP邮件提醒
- [ ] 批量回复模板
- [ ] 邮件搜索功能

## 更新日志

- 2026-03-07: 初始版本，支持QQ邮箱基本功能
