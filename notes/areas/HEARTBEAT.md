# HEARTBEAT.md - 心跳监控
# Proactive Agent v3.1.0

## 心跳状态
- **状态**: ⚠️ 待确认（早晨任务可能未执行）
- **最后检查**: 2026-04-08 14:26 (北京时间)
- **WAL状态**: ⚠️ 严重 - proactive-tracker.md和HEARTBEAT.md从4月7日回退到4月3日

## ⚠️ 异常：早晨任务未更新
**发现时间**: 2026-04-08 14:26
- 早晨任务(4月8日 06:00-07:45) lastRunAtMs仍显示4月7日
- 可能原因：系统离线 / cron调度器延迟 / 任务静默失败
- 需要确认：下一次主动惊喜检查时验证

## 系统恢复记录
- **离线时间**: 2026-03-27 16:02 → 2026-03-28 08:57 (约17小时)
- **模型切换**: 2026-04-03 08:05 (google/gemini-3.1-pro-preview → minimax-portal/MiniMax-M2.7-highspeed)
- **安全修复**: 2026-04-06 23:06 (飞书allowFrom移除*通配符，.gitignore更新)
- **WAL问题**: 4月7日的文件编辑未持久化（回退到4月3日）

## Cron任务监控 ⚠️
| 任务 | ID | 状态 | 上次运行 | consecutiveErrors |
|------|-----|------|----------|------------------|
| 主动惊喜检查 | 66c5d54b | ✅ 运行中 | 04-07 20:02 | 0 |
| DNS传播检查 | 791dfda1 | ⚠️ 待确认 | 04-07 02:30? | 0 |
| OpenClaw新闻 | 5aa186d0 | ⚠️ 待确认 | 04-07 06:00? | 0 |
| 高校AI新闻 | 06c90fe1 | ⚠️ 待确认 | 04-07 06:15? | 0 |
| 健康长寿 | 6502ba52 | ⚠️ 待确认 | 04-07 07:00? | 0 |
| 每日祝福-07:45 | 2503fac6 | ⚠️ 待确认 | 04-07 07:45? | 0 |
| 每日工作日记 | 441ffa7e | ✅ OK | 04-07 21:00 | 0 |
| AI新闻日报更新 | 777908f9 | ✅ OK | 04-07 22:00 | 0 |
| 自动记忆归档 | 3ac20321 | ✅ OK | 04-07 23:00 | 0 |
| 私有知识星图 | 18f3713c | ✅ OK | 04-07 23:30 | 0 |

## 收件人列表（高校分队）
liuwei44259@huawei.com, tiankunyang@huawei.com, qinhongyi2@huawei.com, jiawei18@huawei.com, jiyingguo@huawei.com, linfeng67@huawei.com, lvluling1@huawei.com, suqi1@huawei.com, susha@huawei.com, wangdongxiao@huawei.com, xiongguifang@huawei.com, xushengsheng@huawei.com, zhangqianfeng2@huawei.com, zhangyexing2@huawei.com, 86940135@qq.com

## 系统事件记录
- ⚠️ 2026-04-08 14:26: 发现WAL staleness问题复发，proactive-tracker.md/hearbeat.md回退到4月3日
- ⚠️ 2026-04-08 14:26: 早晨任务(4月8日)可能未执行，需要确认
- ✅ 2026-04-07 晚间任务全部成功

## WAL staleness模式
- **首次**: 2026-03-20 发现
- **复发**: 4月3日、4月5日、4月7日多次复发
- **根因**: 文件编辑未持久化到磁盘
- **影响**: 跟踪文件数据丢失，需每次重建

---
*每4小时由主动惊喜检查自动更新*
