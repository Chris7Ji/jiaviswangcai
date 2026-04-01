# 自建网站统计方案（UV/PV Analytics）

> 来源：sanwan.ai skill-tools.html（三万经验）
> 学习日期：2026-03-29
> 状态：待实施（老板搭建网站后使用）

---

## 📋 需求确认
- 老板有计划搭建自己的网站
- 搭建完成后需要统计功能
- 优先使用自建方案，不依赖第三方

---

## 🎯 目标
统计网站的用户访问数据：
- **UV**（Unique Visitor）：独立访客数
- **PV**（Page View）：页面浏览量
- **来源分析**：用户从哪个页面/外部链接来
- **热门内容**：哪些文章/页面最受欢迎

---

## 🏗️ 方案设计

### 架构概览
```
用户浏览器
    ↓ 访问网站，加载隐藏追踪像素
Nginx 服务器（记录访问日志）
    ↓ 定时读取
Python 脚本（解析日志，计算UV/PV）
    ↓ 输出结果
心跳检查时查询统计结果
```

### 组件清单

| 组件 | 作用 | 备注 |
|------|------|------|
| 追踪像素 | 1x1隐藏图片，触发记录 | `<img src="/track.png" width="1" height="1">` |
| Nginx 日志 | 记录所有请求 | 已有，只需配置 |
| Python 脚本 | 解析日志，计算统计 | 需开发 |
| JSONL 数据文件 | 存储每日统计结果 | 需开发，加保护机制 |
| 保护脚本 | 防止数据被误删 | 重要！参考三万的教训 |

---

## 📝 实施步骤（网站搭建后）

### Step 1: Nginx 配置
在 nginx 配置文件中添加追踪路径：
```nginx
location /track.png {
    access_log /var/log/nginx/analytics.log;
    # 1x1透明GIF图片
    return 200 "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b";
}
```

### Step 2: 网站页面埋点
在需要统计的页面加入：
```html
<img src="/track.png" width="1" height="1" style="display:none">
```

### Step 3: Python 分析脚本
```python
# 读取 /var/log/nginx/analytics.log
# 解析：时间、IP、User-Agent
# 计算：
#   - PV = 总请求数
#   - UV = 独立IP去重数
#   - 来源 = 分析 Referer 头
# 输出到 JSONL 文件
```

### Step 4: 数据保护机制（重要！）
```python
# 防止 analytics.jsonl 被误删/覆盖
# 每次写入前检查：
# 1. 文件是否存在
# 2. 文件大小是否正常（> 100 bytes）
# 3. 是否有备份
```

### Step 5: 心跳集成
在 HEARTBEAT.md 的心跳检查中加入：
```
[ ] 查询 analytics.jsonl
[ ] 报告今日 UV/PV
[ ] 如有异常（如UV骤降）则告警
```

---

## ⚠️ 踩坑记录（来自三万）

| 问题 | 教训 | 预防措施 |
|------|------|----------|
| analytics 文件被 reset 归零 | cron 任务误删数据 | 加保护脚本，检查文件大小 |
| Bing IndexNow key 配置错误 | 用错 key 2周无效 | 配置后双重验证 |

---

## 🔗 相关文档
- 原始教程：https://sanwan.ai/skill-tools.html
- 配套心跳机制：https://sanwan.ai/skill-heartbeat.html

---

## 📌 待办
- [ ] 老板搭建网站
- [ ] 部署追踪像素
- [ ] 开发分析脚本
- [ ] 配置数据保护
- [ ] 集成到心跳检查

---

*最后更新：2026-03-29*
