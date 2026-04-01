# 技能查找指南（临时方案）

由于"find-skills"技能安装遇到速率限制，以下是临时解决方案：

## 1. 使用clawhub CLI搜索技能

### 基本搜索
```bash
# 搜索关键词
clawhub search "pdf"
clawhub search "weather"
clawhub search "github"

# 限制结果数量
clawhub search "ai" --limit 10
```

### 查看已安装技能
```bash
clawhub list
```

## 2. 通过旺财（我）搜索技能

您可以：
1. 告诉我您需要的功能
2. 我帮您搜索相关技能
3. 提供技能描述和安装建议

## 3. 现有52个技能分类参考

### 办公与生产力
- **gog** - Google Workspace集成
- **apple-reminders** - Apple提醒事项
- **github** - GitHub操作
- **gh-issues** - GitHub Issue管理

### 内容处理
- **summarize** - 内容摘要
- **nano-pdf** - PDF编辑
- **video-frames** - 视频帧提取

### 通信集成
- **wacli** - WhatsApp集成
- **discord** - Discord集成

### 系统工具
- **healthcheck** - 系统安全检查
- **1password** - 密码管理
- **camsnap** - 摄像头快照

### 技能管理
- **clawhub** - 技能搜索/安装
- **skill-creator** - 技能创建

## 4. 热门技能推荐

### 最常用技能
1. **weather** - 天气查询（完全可用）
2. **summarize** - 内容摘要（完全可用）
3. **github** - GitHub操作（完全可用）
4. **gog** - Google Workspace（完全可用）

### 特色技能
1. **gifgrep** - GIF搜索（部分可用，需要网络）
2. **nano-pdf** - PDF自然语言编辑（完全可用）
3. **camsnap** - 摄像头快照（完全可用）

## 5. 安装"find-skills"的计划

### 当前状态
- ❌ 安装失败：clawhub API速率限制
- ✅ 搜索功能：clawhub search可用
- ✅ 替代方案：现有clawhub技能提供核心功能

### 后续计划
1. **等待重试**：明天再次尝试安装
2. **手动安装**：如果急需，尝试从源码安装
3. **功能替代**：使用现有工具满足需求

## 6. 快速查找示例

### 如果您需要：
- **PDF处理** → 搜索"pdf"或使用"nano-pdf"技能
- **天气查询** → 使用"weather"技能
- **内容摘要** → 使用"summarize"技能
- **GitHub操作** → 使用"github"或"gh-issues"技能
- **Google集成** → 使用"gog"技能

## 7. 联系支持

如果找不到所需技能：
1. 告诉我具体需求
2. 我帮您搜索或推荐替代方案
3. 记录需求，后续优先安装相关技能

---
**最后更新**：2026-03-02
**状态**：等待clawhub速率限制解除后重试安装"find-skills"