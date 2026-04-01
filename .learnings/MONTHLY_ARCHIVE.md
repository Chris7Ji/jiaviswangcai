# 每月归档检查清单
# 执行频率: 每月最后一天
# 执行者: AI助理旺财
# 指示来源: 老板（季）

## 📦 每月归档任务

### 1. 月度学习记录归档
- [ ] 将当月所有学习记录归档到 `archive/monthly/`
- [ ] 生成月度学习摘要
- [ ] 提取月度核心模式（出现5次以上的）

### 2. 月度错误记录归档
- [ ] 将当月所有错误记录归档到 `archive/monthly/`
- [ ] 生成月度错误分析报告
- [ ] 识别系统性问题

### 3. 清理活跃记录
- [ ] 确保LEARNINGS.md ≤ 10条活跃记录
- [ ] 确保ERRORS.md ≤ 10条活跃记录
- [ ] 保留最重要的近期记录

### 4. 生成月度报告
创建月度总结报告，包含：
- 本月学习总量
- 错误类型分布
- 改进趋势分析
- 下月建议

## 📊 归档文件命名规范

```
archive/monthly/
  ├── learnings_2026-03.md    # 3月学习记录归档
  ├── errors_2026-03.md        # 3月错误记录归档
  └── summary_2026-03.md       # 3月总结报告
```

## 🎯 执行命令

```bash
# 创建月度归档
cd ~/.openclaw/workspace/.learnings

# 归档学习记录
cat LEARNINGS.md >> archive/monthly/learnings_$(date +%Y-%m).md

# 清空活跃记录（保留模板）
echo "# 学习记录" > LEARNINGS.md

# 同样处理错误记录
cat ERRORS.md >> archive/monthly/errors_$(date +%Y-%m).md
echo "# 错误记录" > ERRORS.md
```