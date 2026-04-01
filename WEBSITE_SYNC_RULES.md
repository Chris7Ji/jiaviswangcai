# 网站数据同步全局法则 (Global Website Sync Rule)

**最后更新**: 2026-03-31 02:56 GMT+8

## 核心原则
在每天 **18:00、21:00、22:00** 的任务中，**全站数据牵一发而动全身**，必须遵循以下联动规则！

## 一、 最新日志动态联动 (Top 6 规则)
1. 首页 (`index.html`) 不再需要手动维护最新日志内容！
2. 它的数据源已强绑定到 `js/diary.js` 中的 `allPosts` 数组。
3. `js/main.js` 会自动提取 `allPosts` 的**前 6 条 (Top 6)** 进行首页展示，超出的老日志会自动在首页隐藏。
4. **只要更新了 `js/diary.js`，首页的 "最新日志" 板块会自动且仅展示最新的 6 篇。** 访客点击 "查看全部" 即可跳转到 `diary.html` 看完整版。

## 二、 全局统计数字同步
在自动化增加日志、技能或修改网站内容之后，**必须在最后步骤执行以下命令进行全局数字校准同步，并一起 push 到 GitHub**：

```bash
python3 /Users/jiyingguo/.openclaw/workspace/scripts/sync_site_data.py
```

该脚本会自动重新计算并更新：
- `main.js` 中的 `postsCount`（总日志数）、`daysOnline`（运行天数）、`skillsCount`（技能总数）
- `skills.html` 里面的分类生成与数目统计
