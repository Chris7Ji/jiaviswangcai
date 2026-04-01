# 邮件相关学习记录
# 分类: 邮件系统配置和使用
# 创建: 2026-03-10

## 2026-03-10 14:00:00
**ID**: learn-001
**优先级**: MEDIUM
**类别**: best_practice
**摘要**: OpenClaw gateway restart 命令不需要sudo权限
**场景**: 之前错误地认为重启OpenClaw网关服务需要sudo权限
**纠正**: 实际上，openclaw gateway restart 命令在普通用户权限下即可执行，无需sudo
**建议修复**: 在需要重启OpenClaw网关时，直接使用 `openclaw gateway restart` 而非 `sudo openclaw gateway restart`
**相关工具**: openclaw CLI
**适用场景**: OpenClaw服务管理
**状态**: ✅ 已验证

## 2026-03-10 23:11:00
**ID**: learn-003
**优先级**: HIGH
**类别**: best_practice
**摘要**: 健康长寿报告邮件发送配置完成
**场景**: 为健康长寿科研成果监控任务配置邮件发送功能
**核心配置**:
- SMTP服务器: smtp.qq.com:465
- 发件邮箱: 86940135@qq.com
- 授权码: swqfjvmoupdebhgh
- 收件人: 86940135@qq.com, jiyingguo@huawei.com
- 脚本位置: send_health_email.sh, send_health_email.py
**应用**: 每天08:30自动生成报告后自动发送邮件
**状态**: ✅ 已验证（测试发送成功）