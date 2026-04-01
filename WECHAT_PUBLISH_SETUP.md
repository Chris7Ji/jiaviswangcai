# 微信公众号自动发布配置指南

## 一、前提条件

### 1. 公众号类型要求
- **必须是已认证的服务号**
- 订阅号无法使用草稿箱API
- 认证费用：300元/年（微信官方收取）

### 2. 所需权限
- 草稿箱管理权限（add_news, get_news, update_news, delete_news）
- 素材管理权限（上传图片、封面图）

---

## 二、获取API凭证

### 步骤1：登录公众号后台
1. 访问 https://mp.weixin.qq.com/
2. 登录您的公众号

### 步骤2：获取AppID和AppSecret
1. 左侧菜单 → 开发 → 基本配置
2. 找到 **AppID(应用ID)**
3. 点击 **AppSecret(应用密钥)** 的"重置"或"查看"
4. 保存这两个值（AppSecret只显示一次！）

### 步骤3：配置IP白名单
1. 在同一页面找到 **IP白名单**
2. 添加您的服务器IP地址
3. 如果是本地测试，需要内网穿透工具（如ngrok）

### 步骤4：开通接口权限
1. 左侧菜单 → 开发 → 接口权限
2. 确认以下权限已开通：
   - ✅ 草稿箱管理
   - ✅ 素材管理
   - ✅ 消息管理

---

## 三、配置OpenClaw

### 1. 创建配置文件

```bash
mkdir -p ~/.openclaw/workspace-creator/config
cat > ~/.openclaw/workspace-creator/config/wechat.yml << 'EOF'
# 微信公众号配置
wechat:
  app_id: "YOUR_APP_ID"
  app_secret: "YOUR_APP_SECRET"
  token: ""  # 可选，用于消息加解密
  encoding_aes_key: ""  # 可选，用于消息加解密
  
# 发布配置
publish:
  default_author: "YOUR_NAME"  # 默认作者名
  default_source_url: ""  # 默认原文链接
  need_open_comment: 1  # 是否开启评论：1开启，0关闭
  only_fans_can_comment: 0  # 是否仅粉丝可评论
EOF
```

### 2. 设置环境变量

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
echo 'export WECHAT_APP_ID="wx...your_app_id"' >> ~/.zshrc
echo 'export WECHAT_APP_SECRET="your_app_secret"' >> ~/.zshrc
source ~/.zshrc
```

### 3. 安装wechat-public-cli工具

```bash
# 方案A：通过npm安装（推荐）
npm install -g wechat-public-cli

# 方案B：通过clawhub安装（需等待速率限制解除）
clawhub install wechat-public-cli --dir ~/.openclaw/workspace-creator/skills/

# 方案C：使用wechat-mp
pip3 install wechat-mp
```

---

## 四、发布脚本

### 创建自动发布脚本

```bash
cat > ~/.openclaw/workspace-creator/publish_to_wechat.sh << 'EOF'
#!/bin/bash
# 微信公众号自动发布脚本

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: $0 <markdown文件> [标题]"
    exit 1
fi

MD_FILE=$1
TITLE=${2:-""}

# 检查文件
if [ ! -f "$MD_FILE" ]; then
    echo "错误: 文件不存在 $MD_FILE"
    exit 1
fi

# 读取配置
APP_ID=${WECHAT_APP_ID:-""}
APP_SECRET=${WECHAT_APP_SECRET:-""}

if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    echo "错误: 未设置 WECHAT_APP_ID 或 WECHAT_APP_SECRET"
    echo "请先配置环境变量"
    exit 1
fi

echo "📝 准备发布到微信公众号"
echo "文件: $MD_FILE"
echo "标题: ${TITLE:-自动提取}"
echo ""

# 使用wechat-public-cli发布
# 注意：需要提前安装 wechat-public-cli
if command -v wechat-public-cli &> /dev/null; then
    wechat-public-cli publish \
        --app-id "$APP_ID" \
        --app-secret "$APP_SECRET" \
        --file "$MD_FILE" \
        --title "$TITLE"
else
    echo "⚠️  wechat-public-cli 未安装"
    echo "请先安装: npm install -g wechat-public-cli"
    exit 1
fi
EOF

chmod +x ~/.openclaw/workspace-creator/publish_to_wechat.sh
```

---

## 五、使用方法

### 1. 命令行发布

```bash
# 发布文章
~/.openclaw/workspace-creator/publish_to_wechat.sh \
    ~/.openclaw/workspace/openclaw_article_2026-03-07.md \
    "凌晨2点，我的AI助手还在帮我改代码"
```

### 2. 通过笔杆子Agent发布

配置完成后，可以直接对笔杆子说：
```
把刚才写的OpenClaw文章发布到公众号
```

---

## 六、替代方案

如果暂时无法配置API，可以使用：

### 方案1：手动复制（当前）
- 复制 `openclaw_article_wechat.txt` 内容
- 粘贴到公众号后台

### 方案2：使用第三方工具
- **壹伴助手**：浏览器插件，一键采集发布
- **秀米**：在线排版工具，支持同步到公众号
- **135编辑器**：类似秀米，排版工具

### 方案3：等待技能完善
- wechat-article技能正在开发中
- 完成后可直接通过Agent自动发布

---

## 七、注意事项

1. **安全问题**
   - AppSecret非常敏感，不要泄露
   - 不要提交到GitHub等公开仓库
   - 建议定期重置AppSecret

2. **频率限制**
   - 公众号API有调用频率限制
   - 一般每天最多发布8篇图文
   - 注意控制发布频率

3. **内容审核**
   - 发布的内容需要符合微信规范
   - 敏感内容可能被拦截
   - 建议先发布到草稿箱预览

---

## 八、快速检查清单

- [ ] 公众号已认证（服务号）
- [ ] 已获取AppID和AppSecret
- [ ] 已配置IP白名单
- [ ] 已开通草稿箱管理权限
- [ ] 已安装wechat-public-cli
- [ ] 已配置环境变量
- [ ] 已测试发布功能

---

**配置完成后，即可实现一键发布到微信公众号草稿箱！**
