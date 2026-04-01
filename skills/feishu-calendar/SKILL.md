# 📅 飞书日历管理技能

## 概述
超级助理飞书日历技能，支持查询、创建、修改日历事件。

## 功能特性

### ✅ 已实现功能
- 列出日历事件
- 查看今天/明天的日程
- 创建新事件
- 删除事件
- 自动获取飞书访问令牌

### 📝 使用方法

#### 1. 列出最近日程
```bash
# 列出最近10个事件
python3 skills/feishu-calendar/feishu_calendar.py list

# 列出最近5个事件
python3 skills/feishu-calendar/feishu_calendar.py list 5
```

#### 2. 查看今天日程
```bash
python3 skills/feishu-calendar/feishu_calendar.py today
```

#### 3. 创建事件
```bash
python3 skills/feishu-calendar/feishu_calendar.py create \
  "项目会议" \
  "2026-03-07T15:00:00" \
  "2026-03-07T16:00:00" \
  "讨论项目进度"
```

#### 4. 删除事件
```bash
python3 skills/feishu-calendar/feishu_calendar.py delete <事件ID>
```

### 💬 自然语言指令

可以直接对我说：
- "今天有什么会"
- "明天下午有什么安排"
- "帮我创建一个会议"
- "取消明天的会"

## 配置说明

### 飞书应用配置（已配置）
- **App ID**: cli_a9f596118438dcef
- **App Secret**: 已配置
- **接收人Open ID**: ou_b6c7778820b20031cd97bdc45d1cd9fa

### 所需权限
需要以下飞书应用权限：
- `calendar:calendar:readonly` - 读取日历
- `calendar:calendar` - 创建/修改日历
- `calendar:calendar.event:readonly` - 读取事件
- `calendar:calendar.event` - 创建/修改事件

## 使用场景

### 场景1: 每日日程播报
```
用户: 今天有什么安排
助手: 查看今天的飞书日历...
```

### 场景2: 会议协调
```
用户: 约市场部的会
助手: 查找空闲时间并创建会议...
```

### 场景3: 行程规划
```
用户: 下周出差安排
助手: 查看下周日程并检查冲突...
```

## 待完善功能

- [ ] 自动查找参会人空闲时间
- [ ] 会议提醒功能
- [ ] 重复事件管理
- [ ] 会议邀请发送
- [ ] 日程冲突检测

## 更新日志

- 2026-03-07: 初始版本，支持基本日历操作
