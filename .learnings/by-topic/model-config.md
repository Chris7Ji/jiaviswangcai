# 模型配置相关学习记录
# 分类: 大模型切换和配置
# 创建: 2026-03-10

## 2026-03-10 22:36:00
**ID**: learn-004
**优先级**: HIGH
**类别**: config
**摘要**: 全部默认模型切换为Kimi K2.5
**场景**: 老板要求将全省（全部）默认模型切换为Kimi K2.5
**执行内容**:
1. 修改agents.defaults.model.primary为moonshot/kimi-k2.5
2. 修改所有8个Agent的model字段为moonshot/kimi-k2.5
3. 调整fallbacks顺序
**涉及文件**: ~/.openclaw/openclaw.json
**模型变更历史**:
- 之前: minimax-cn/MiniMax-M2.5
- 中间: deepseek/deepseek-chat
- 现在: moonshot/kimi-k2.5
**Kimi K2.5优势**:
- 上下文窗口: 256k tokens
- 支持多模态: 文本+图像
- 成本: 免费
- 中文能力: 优秀
**状态**: ✅ 已验证（当前正在使用）

## 2026-03-10 13:54:00
**ID**: learn-005
**优先级**: MEDIUM
**类别**: config
**摘要**: 模型切换原因分析
**场景**: 老板询问为什么要从minimax切换到deepseek
**分析原因**:
1. 成本优化: Deepseek Chat免费，minimax有使用成本
2. 技术栈统一: 其他子agent已使用Deepseek生态
3. 性能平衡: Deepseek Chat在通用任务上表现良好
4. API兼容性: Deepseek使用OpenAI格式，兼容性更好
**结论**: minimax保留为fallback选项
**状态**: ✅ 已分析