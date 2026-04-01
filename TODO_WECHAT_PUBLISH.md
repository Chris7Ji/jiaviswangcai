# 待办事项 - 微信公众号自动发布配置

## 📋 待确认事项

### 1. 公众号类型
- [x] **公众号（订阅号）** ✅ 已确认
- [ ] 是否已认证？（认证后可获得更多接口权限）

**注意**：订阅号即使认证，也无法使用草稿箱API，需要通过其他方式发布

### 2. API凭证
- [ ] 登录 https://mp.weixin.qq.com/
- [ ] 开发 → 基本配置
- [ ] 获取 **AppID** 和 **AppSecret**

### 3. 发布方式（订阅号）
由于订阅号限制，可选方案：
- [ ] **方案A**：使用第三方工具（壹伴助手、秀米等）
- [ ] **方案B**：使用微信开发者工具模拟发布
- [ ] **方案C**：手动复制到公众号后台
- [ ] **方案D**：升级为服务号（需300元/年认证费）

---

## 📁 已准备好的文件

| 文件 | 位置 | 说明 |
|------|------|------|
| 公众号文章（完整版） | `~/.openclaw/workspace/openclaw_article_2026-03-07.md` | Markdown格式，约1950字 |
| 公众号文章（发布版） | `~/.openclaw/workspace/openclaw_article_wechat.txt` | 适合复制粘贴 |
| 自动发布配置指南 | `~/.openclaw/workspace/WECHAT_PUBLISH_SETUP.md` | 完整配置步骤 |
| 发布脚本 | `~/.openclaw/workspace-creator/publish_to_wechat.sh` | 一键发布脚本（待配置） |

---

## 🚀 确认后需要做的

### 第一步：获取API凭证
1. 登录 https://mp.weixin.qq.com/
2. 开发 → 基本配置
3. 复制 **AppID** 和 **AppSecret**

### 第二步：配置环境变量
```bash
export WECHAT_APP_ID="wx..."
export WECHAT_APP_SECRET="..."
```

### 第三步：安装发布工具
```bash
npm install -g wechat-public-cli
```

### 第四步：测试发布
```bash
~/.openclaw/workspace-creator/publish_to_wechat.sh \
    ~/.openclaw/workspace/openclaw_article_2026-03-07.md \
    "凌晨2点，我的AI助手还在帮我改代码"
```

---

## 💡 临时方案

在配置完成前，可以：
- 手动复制 `openclaw_article_wechat.txt` 到公众号后台
- 或使用第三方工具（壹伴助手、秀米等）

---

## ⏰ 提醒

**Boss需要确认：**
1. 是否有认证的服务号？
2. AppID 和 AppSecret 是否已获取？

**确认后告诉我，立即开始配置！** 🚀

---

**记录时间**: 2026-03-07 17:01
**状态**: 等待Boss确认
