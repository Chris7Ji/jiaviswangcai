# 昇腾生态平台 - 设计系统

> 基于 ui-ux-pro-max 生成的专属设计系统
> 生成时间: 2026-03-26
> 适用: AI计算平台、开发者工具、华为昇腾生态产品

---

## 🎯 产品定位

- **产品类型**: AI Computing Platform / Developer Tool
- **目标用户**: 开发者、AI从业者、企业用户
- **风格关键词**: 专业、代码感、科技感、现代、高性能
- **推荐技术栈**: React + Next.js / Tailwind CSS / shadcn/ui

---

## 📐 页面结构 (Pattern)

### App Store Style Landing
- **转换重点**: 展示真实截图，包含评分(4.5+星)，二维码用于移动端，平台特定CTA
- **CTA位置**: 下载按钮突出展示(App Store + Play Store)
- **色彩策略**: 深色/浅色匹配应用商店风格，星级评分用金色，截图用设备框架
- **页面分区**:
  1. Hero + 设备模型
  2. 截图轮播
  3. 功能特性(带图标)
  4. 评价/评分
  5. 下载CTA

---

## 🎨 视觉风格

### 推荐: Vibrant & Block-based + Dark Mode (OLED)

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| **Dark Mode (OLED)** | 深黑底 #000000，低蓝光，高对比度 | 代码平台、开发者工具 |
| **Cyberpunk UI** | 霓虹灯效果，HUD风格，科幻感 | 展示AI/前沿科技感 |
| **Neumorphism** | 柔和阴影，凸起/凹陷效果 | 需要温和触感的界面 |

### 备选风格
- **Bento Grid** - 仪表盘/功能展示
- **Glassmorphism** - 现代SaaS感
- **Minimalism** - 文档/帮助中心

---

## 🌈 配色方案

### 方案一: 开发者工具风格 (主推)

| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#1E293B` | 主色调(深蓝灰) |
| Secondary | `#334155` | 次要元素 |
| CTA | `#22C55E` | 行动按钮(运行绿) |
| Background | `#0F172A` | 深色背景 |
| Text | `#F8FAFC` | 主文本(近白) |

### 方案二: 量子计算风格 (科技感)

| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#00FFFF` | 量子青 |
| Secondary | `#7B61FF` | 干涉紫 |
| CTA | `#FF00FF` | Magenta |
| Background | `#050510` | 深空黑 |
| Text | `#E0E0FF` | 淡紫白 |

### 方案三: 华为昇腾品牌色

| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#282迫D54` | 华为红(点缀) |
| Secondary | `#007C92` | 科技蓝 |
| CTA | `#00BFFF` | 亮青(CTA) |
| Background | `#0A1628` | 深邃蓝黑 |
| Text | `#E8F4F8` | 冷白 |

---

## ✍️ 字体系统

### 推荐字体搭配

| 用途 | 字体 | 特点 |
|------|------|------|
| **Heading** | JetBrains Mono | 代码感、等宽、精准 |
| **Body** | IBM Plex Sans | 现代、清晰、技术感 |
| **Code** | Fira Code / JetBrains Mono | 连字支持、编程友好 |

### Google Fonts 引入

```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
```

### 字体系统变量

```css
:root {
  --font-heading: 'JetBrains Mono', monospace;
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-code: 'Fira Code', 'JetBrains Mono', monospace;
  
  /* 字号系统 */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
}
```

---

## ✨ 动效规范

### 核心原则
- **时长**: 150-300ms (微交互)，≤400ms (复杂过渡)
- **缓动**: ease-out 进入，ease-in 退出
- **性能**: 仅使用 transform/opacity 动画

### 推荐效果
| 效果 | 参数 | 适用场景 |
|------|------|----------|
| 悬停放大 | scale(1.02), 200ms | 卡片、按钮 |
| 发光效果 | text-shadow: 0 0 10px | 霓虹按钮、代码关键字 |
| 渐变流动 | background-position 动画 | Hero背景、装饰 |
| 打字机效果 | 逐字显示 | 代码演示、标题 |
| 扫描线 | ::before overlay | Cyberpunk风格 |

---

## 🚫 避免的反模式

| ❌ 避免 | ✅ 推荐 |
|--------|--------|
| 扁平设计无深度 | 阴影+层次感 |
| 文字过密 | 大留白+清晰分区 |
| emoji作为图标 | SVG图标(Heroicons/Lucide) |
| 单调的单色按钮 | 渐变+悬停反馈 |
| 纯文字导航 | 图标+文字组合 |
| 0ms状态变化 | 150-300ms过渡动画 |

---

## 📋 预交付检查清单

### 视觉质量
- [ ] 无emoji作为结构图标
- [ ] 图标来自统一图标库(Heroicons/Lucide)
- [ ] 官方品牌资产使用正确
- [ ] 按压状态不改变布局

### 交互
- [ ] 所有可点击元素有悬停反馈
- [ ] 触控目标 ≥44x44pt
- [ ] 微交互动画 150-300ms
- [ ] 禁用状态视觉清晰

### 响应式
- [ ] 移动端优先
- [ ] 断点: 375px / 768px / 1024px / 1440px
- [ ] 无水平滚动

### 无障碍
- [ ] 对比度 ≥4.5:1
- [ ] 支持 prefers-reduced-motion
- [ ] 键盘导航支持
- [ ] 焦点状态可见

---

## 🔧 技术栈建议

### 前端框架
- **Next.js** - SSR/SSG，SEO友好
- **Tailwind CSS** - 原子化CSS，快速开发
- **shadcn/ui** - 高质量组件库

### 组件库
- Radix UI (底层)
- Lucide React (图标)
- Framer Motion (动画)

### 代码高亮
- Prism.js
- Shiki (VS Code同款)

---

## 📁 相关文件

- 设计系统数据库: `~/.openclaw/workspace/skills/ui-ux-pro-max/data/`
- 搜索脚本: `~/.openclaw/workspace/skills/ui-ux-pro-max/scripts/search.py`

---

*设计系统生成工具: ui-ux-pro-max v2.0*
