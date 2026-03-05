# OpenClaw 完整迁移检查清单

## 准备工作
- [ ] 检查 OpenClaw Gateway 是否运行中
- [ ] 检查所有渠道连接状态（Discord/WhatsApp）

## 数据打包
- [ ] 打包工作区（~/clawd）
- [ ] 打包 OpenClaw 配置（~/.openclaw/）
- [ ] 打包内置技能（~/openclaw/skills/）
- [ ] 打包自定义技能（~/Documents/AIProject/clawbot/.trae/skills/）
- [ ] 打包 cron 任务（~/.openclaw/cron/）

## 传输
- [ ] 使用安全方式传输到新电脑（推荐 SCP）
- [ ] 在新电脑解压所有包

## 安装
- [ ] 安装 Node.js
- [ ] 安装 OpenClaw
- [ ] 解压配置
- [ ] 启动服务

## 验证
- [ ] 测试所有渠道
- [ ] 测试自定义技能

## 清理
- [ ] 删除旧电脑的凭据（迁移完成后）
