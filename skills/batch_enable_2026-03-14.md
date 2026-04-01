# 批量技能启用配置
# 生成时间: 2026-03-14 03:34
# 启用技能总数: 9个

## 搜索类（4个）

### 1. ✅ Tavily Search
- **状态**: 已启用
- **API**: 已配置
- **使用**: `./skills/search.sh "关键词" tavily`

### 2. ✅ Multi Search Engine
- **状态**: 已启用
- **引擎**: 17个（8国内+9国际）
- **使用**: `./skills/search.sh "关键词" multi`

### 3. ✅ DuckDuckGo Search
- **状态**: 已启用
- **特点**: 隐私保护
- **使用**: `./skills/search.sh "关键词" duckduckgo`

### 4. ⚠️ SerpAPI
- **状态**: 已启用（需API Key）
- **说明**: 需要SerpAPI密钥才能使用
- **获取**: https://serpapi.com/
- **配置**: `export SERPAPI_API_KEY=your_key`

---

## 内容生成类（2个）

### 5. ✅ Nano Banana Pro
- **状态**: 已启用
- **功能**: Gemini 3 Pro Image 图像生成/编辑
- **分辨率**: 1K/2K/4K
- **使用**: 
  ```bash
  uv run skills/nano-banana-pro/scripts/generate_image.py \
    --prompt "描述" --filename "output.png" --resolution 4K
  ```
- **API**: 使用GEMINI_API_KEY（已配置）

### 6. ✅ Nano Banana 2
- **状态**: 已启用
- **功能**: Gemini 3.1 Flash Image Preview
- **特点**: 更快的图像生成
- **使用**:
  ```bash
  infsh app run google/gemini-3-1-flash-image-preview \
    --input '{"prompt": "描述"}'
  ```
- **依赖**: 需要安装infsh CLI

---

## 办公/生产力类（3个）

### 7. ✅ Office
- **状态**: 已启用
- **功能**: Excel/Word/PowerPoint/Google Workspace
- **涵盖**:
  - 电子表格：公式、透视表、VLOOKUP
  - 文档：格式化、邮件合并、目录
  - 演示：幻灯片、动画、演讲者视图
  - 办公管理：供应商、设施、空间规划

### 8. ⚠️ Office-xyz
- **状态**: 已启用（需配置）
- **功能**: 2D虚拟办公平台，AI代理协作
- **配置**: 需要注册office.xyz账号
- **使用**: 通过API进行任务管理、文件共享、会议

### 9. ⚠️ Obsidian Ontology Sync
- **状态**: 已启用（需配置）
- **功能**: Obsidian笔记 ↔ 结构化本体图 双向同步
- **配置**: 需要设置Obsidian仓库路径
- **自动**: 每3小时同步一次（通过cron）

---

## 启用总结

| 类别 | 技能数 | 状态 |
|------|--------|------|
| 搜索类 | 4个 | 3个立即可用，1个需API Key |
| 内容生成 | 2个 | 1个立即可用，1个需infsh CLI |
| 办公/生产力 | 3个 | 1个立即可用，2个需配置 |
| **总计** | **9个** | **全部已启用** |

---

## 下一步配置（可选）

1. **SerpAPI**: 获取API Key以启用Google/Bing搜索
2. **Nano Banana 2**: 安装 `curl -fsSL https://cli.inference.sh | sh`
3. **Office-xyz**: 注册 https://office.xyz 获取agent handle
4. **Obsidian Sync**: 配置Obsidian仓库路径

---

*启用时间: 2026-03-14*
*Proactive Agent 批量启用*
