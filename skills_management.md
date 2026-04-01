# 技能管理文档
创建时间: 2026-03-19
最后更新: 2026-03-19

## 📊 技能概览
- 总技能数: 44
- 正常: 42
- 有问题: 2
- 版本过低: 3

## 🚨 问题技能

### 1. Google Gemini 相关（受地理限制）
| 技能名称 | 版本 | 状态 | 建议 |
|----------|------|------|------|
| nano-banana-pro | 1.0.1 | ❌ 不可用 | 禁用或寻找替代 |
| nano-banana-2 | 0.1.1 | ❌ 不可用 | 禁用或寻找替代 |

### 2. 版本过旧
| 技能名称 | 版本 | 建议 |
|----------|------|------|
| find-skills-robin | 0.1.0 | 检查更新 |
| reminder | 0.1.1 | 检查更新 |
| twitter-operations | 1.0.0 | 检查功能是否正常 |

### 3. 功能重叠
| 技能组 | 技能1 | 技能2 | 建议 |
|--------|-------|-------|------|
| 股票监控 | stock-monitor (1.3.0) | stock-monitor-hkus (1.1.0) | 考虑合并 |
| 竞品分析 | competitor-analysis (3.0.0) | competitor-research (1.0.0) | 明确分工 |
| Office相关 | office (1.0.0) | office-xyz (1.0.0) | 检查差异 |

## 🛠️ 管理操作记录

### 2026-03-19
- ✅ 修复 exec 权限问题，添加 clawhub 到允许列表
- 🔍 完成技能清单检查
- 📋 创建本管理文档

## 📈 使用建议

### 高频使用技能（建议保持启用）
1. **summarize** - 内容摘要
2. **daily-report-skill** - 日报生成  
3. **weekly-report** - 周报生成
4. **github** - GitHub 操作
5. **multi-search-engine** - 多源搜索
6. **proactive-agent** - 主动代理
7. **self-improving-agent** - 自我改进

### 低频使用技能（可考虑禁用）
1. **games** - 游戏相关
2. **evolink-music** - 音乐生成
3. **evolink-video** - 视频生成
4. **distil** - 蒸馏相关
5. **tophot-chinese** - 热门内容

## 🔧 维护计划

### 每周维护
- [ ] 检查技能更新
- [ ] 验证问题技能状态
- [ ] 清理技能缓存

### 每月维护  
- [ ] 运行安全审计 (mayguard)
- [ ] 更新技能管理文档
- [ ] 评估技能使用情况

### 每季度维护
- [ ] 清理未使用技能
- [ ] 整合相似功能技能
- [ ] 优化技能配置

## 📞 支持信息

### 技能问题排查
1. 检查技能目录: `ls ~/.openclaw/workspace/skills/`
2. 查看技能列表: `clawhub list`
3. 检查技能状态: 查看各技能目录下的 SKILL.md

### 紧急处理
1. 禁用问题技能: 移动到 `_disabled_` 前缀目录
2. 恢复技能: 从 `_disabled_` 目录移回
3. 完全删除: `clawhub uninstall <技能名>`

---

**备注**: 本文档应定期更新，反映技能状态变化。