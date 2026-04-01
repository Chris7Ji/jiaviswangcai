# GitHub操作技能指南

## 概述
GitHub MCP技能支持仓库管理、Issues、Pull Requests、代码搜索等操作。

## 安装
```bash
clawhub install github-mcp --dir skills/
# 或强制安装（如果被标记为可疑）
clawhub install github-mcp --dir skills/ --force
```

## 支持操作

### 1. 仓库管理
- 创建仓库
- 克隆仓库
- 推送代码
- 查看仓库信息

### 2. Issues管理
- 创建Issue
- 评论Issue
- 关闭Issue
- 列出Issues

### 3. Pull Requests
- 创建PR
- 审查PR
- 合并PR
- 列出PRs

### 4. 代码搜索
- 搜索代码
- 搜索仓库
- 搜索用户

### 5. Actions
- 查看工作流状态
- 触发工作流
- 查看日志

### 6. Release管理
- 创建Release
- 查看Releases
- 上传资源

## 配置要求

### 1. GitHub Token
需要配置GitHub Personal Access Token：
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

获取方式：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择需要的权限（repo, workflow等）
4. 复制生成的token

### 2. 环境变量
```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export GITHUB_TOKEN="your-token"
export GITHUB_USERNAME="your-username"
```

## 使用示例

### 创建Issue
```python
# 使用github-mcp技能创建Issue
```

### 创建Pull Request
```python
# 使用github-mcp技能创建PR
```

### 查看Actions状态
```python
# 使用github-mcp技能查看CI状态
```

## 替代方案

如果github-mcp技能无法安装，可以使用：

### 1. GitHub CLI (gh)
```bash
# 安装
brew install gh

# 登录
gh auth login

# 常用命令
gh repo create
gh issue create
gh pr create
gh pr merge
```

### 2. 直接使用git命令
```bash
# 克隆
git clone https://github.com/user/repo.git

# 推送
git push origin main

# 拉取
git pull origin main
```

### 3. GitHub API
```python
import requests

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# 创建Issue
response = requests.post(
    "https://api.github.com/repos/owner/repo/issues",
    headers=headers,
    json={"title": "Bug report", "body": "Description"}
)
```

## 当前状态

由于github-mcp技能被标记为可疑，建议：
1. 使用GitHub CLI (gh) 作为替代
2. 或手动配置GitHub API调用
3. 等待技能更新或选择其他方案

## 相关技能
- ✅ github - 基础GitHub操作（已安装）
- ✅ gh-issues - GitHub Issues管理（已安装）
