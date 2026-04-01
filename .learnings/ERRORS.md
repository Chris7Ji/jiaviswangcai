# 错误记录

## 2026-03-10 14:00:00
**ID**: error-001
**优先级**: HIGH
**错误类型**: Command Execution
**命令**: `npx clawhub@latest install systematic-debugging`
**错误信息**: Skill not found
**根本原因**: 技能名称不正确或已不存在于ClawHub仓库
**环境信息**:
- 系统: macOS
- Node版本: v22.22.0
- ClawHub版本: latest
- 时间: 2026-03-10 13:54
**解决方案**: 
1. 使用 `clawhub search debugging` 搜索正确的技能名称
2. 检查已安装技能中是否有类似功能（发现已有debug-checklist）
3. 使用现有技能或寻找替代方案
**预防措施**:
1. 安装技能前先搜索确认名称
2. 检查是否已有类似功能的技能
3. 考虑功能相似的替代方案
**状态**: ✅ 已解决（使用debug-checklist作为替代）
