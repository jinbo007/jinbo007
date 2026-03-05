# 🤖 Vibe Coding 自动新闻推送

每天早上 8:00 自动发送 Vibe Coding 相关的新闻到 Discord 和 WhatsApp。

---

## 📋 文件结构

```
~/clawd/vibe-news/
├── daily_news_simple.py    # 主脚本
├── install.sh              # 安装脚本
├── .env.example             # 配置示例
└── output/                 # 输出目录
    ├── daily-2026-03-04.md
    ├── cron.log
    └── cron-error.log
```

---

## 🚀 快速安装

### 1️⃣ 运行安装脚本

```bash
cd ~/clawd/vibe-news
bash install.sh
```

### 2️⃣ 配置 Discord Webhook

**获取 Webhook URL：**
1. 打开你的 Discord 服务器
2. 进入 **Integrations** → **Webhooks**
3. 点击 **New Webhook**
4. 选择你的频道
5. 复制 Webhook URL

**更新脚本：**
编辑 `daily_news_simple.py`，找到这一行：
```python
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1465634481837834291/YOUR_WEBHOOK_TOKEN"
```

替换为：
```python
DISCORD_WEBHOOK = "你的实际_Webhook_URL"
```

---

## ⏰ 定时任务

### macOS（自动配置）

安装脚本会自动配置 **launchd**：
- ✅ 每天早上 8:00 运行
- ✅ 自动重启（系统重启后）
- ✅ 日志记录到 `~/clawd/vibe-news/output/cron.log`

**管理命令：**
```bash
# 查看状态
launchctl list | grep vibe-news

# 手动运行
launchctl start com.openclaw.vibe-news

# 停止任务
launchctl unload ~/Library/LaunchAgents/com.openclaw.vibe-news.plist

# 查看日志
tail -f ~/clawd/vibe-news/output/cron.log
```

### Linux（需要手动配置）

```bash
# 添加 cron 任务
crontab -e

# 添加这一行（如果不存在）
0 8 * * * /usr/bin/python3 ~/clawd/vibe-news/daily_news_simple.py >> ~/clawd/vibe-news/output/cron.log 2>&1
```

---

## 📊 新闻来源

| 来源 | 说明 |
|------|------|
| **GitHub AI 热门** | AI/LLM 相关高星项目 |
| **GitHub Vibe Coding** | Vibe Coding、Claude Code、Cursor 等编辑器 |

---

## 🧪 手动运行

**运行一次测试：**
```bash
python3 ~/clawd/vibe-news/daily_news_simple.py
```

**查看日志：**
```bash
tail -f ~/clawd/vibe-news/output/cron.log
```

**查看错误：**
```bash
cat ~/clawd/vibe-news/output/cron-error.log
```

---

## 🛠️ 故障排查

| 问题 | 解决方案 |
|------|--------|
| Discord 发送失败 | 检查 Webhook URL 是否正确 |
| GitHub API 限流 | 等待 1 小时后再试 |
| 定时任务未运行 | 检查 launchd/cron 服务状态 |
| Python 依赖缺失 | 运行 `pip3 install requests` |

---

## 📝 配置文件

**`.env.example`（模板）**
```bash
# Discord Webhook URL（必需）
DISCORD_WEBHOOK=https://discord.com/api/webhooks/1465634481837834291/YOUR_TOKEN

# GitHub Token（可选，提高 API 限制）
GITHUB_TOKEN=ghp_YOUR_TOKEN
```

---

## ✅ 验证安装

```bash
# 检查脚本是否存在
ls -la ~/clawd/vibe-news/daily_news_simple.py

# 检查 launchd 任务（macOS）
launchctl list | grep vibe-news

# 或检查 cron 任务（Linux）
crontab -l | grep vibe-news
```

---

## 📅 输出示例

**每天早上 8:00 在 Discord 收到：**

```
🔥 Vibe Coding 日报 - 2026年03月04日

## 📦 GitHub 热门 AI 项目

1. **OpenClaw** ⭐ 255.9k
   个人 AI 助手平台，支持多系统
   🔗 https://github.com/openclaw/openclaw

2. **AutoGPT** ⭐ 182.2k
   自主 AI 代理框架
   🔗 https://github.com/Significant-Gravitas/AutoGPT
...
```

---

## 🎯 使用场景

- 📱 每天早上自动推送最新 Vibe Coding 新闻
- 🧠 自动保存日报到本地
- 🔍 包含热门 GitHub 项目
- 💬 发送到指定的 Discord 频道

---

**开始安装：**
```bash
cd ~/clawd/vibe-news
bash install.sh
```

---
*创建时间：2026-03-04*
*最后更新：2026-03-04*
