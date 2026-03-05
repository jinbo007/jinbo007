# 🔥 技术日报自动推送系统

每天早上 8:00 自动获取最新技术动态，发送到 Discord 并推送到 GitHub Pages。

---

## 📋 新闻源

| 类别 | 来源 | 说明 |
|------|------|------|
| 🌊 Vibe Coding | GitHub | Claude Code, Cursor, Windsurf |
| ☁️ Cloudflare | GitHub + Blog | Workers, Pages, Wrangler |
| 🤖 Codex & AI Coding | GitHub | OpenAI Codex, GitHub Copilot |
| 🚀 Anti-Gravity | GitHub | Anti-Gravity 相关项目 |
| 📝 技术博客 | GitHub | 技术博客和工程博客 |

---

## 🚀 快速开始

### 1️⃣ 安装

```bash
cd ~/clawd/tech-news
bash install.sh
```

### 2️⃣ 配置 Discord Webhook

编辑 `tech_news_daily.py`，修改第 12 行：

```python
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

### 3️⃣ 测试运行

```bash
python3 ~/clawd/tech-news/tech_news_daily.py
```

---

## 📂 文件结构

```
~/clawd/tech-news/
├── tech_news_daily.py     # 主脚本
├── install.sh             # 安装脚本
├── README.md              # 本文件
└── output/                # 输出目录
    ├── tech-news-2026-03-04.md
    ├── cron.log
    └── cron-error.log
```

---

## ⏰ 定时任务

### macOS (launchd)

**自动配置**：安装脚本会自动配置 launchd

**管理命令：**
```bash
# 查看状态
launchctl list | grep tech-news

# 手动运行
launchctl start com.openclaw.tech-news

# 停止任务
launchctl unload ~/Library/LaunchAgents/com.openclaw.tech-news.plist

# 查看日志
tail -f ~/clawd/tech-news/output/cron.log
```

### Linux (cron)

**手动配置：**
```bash
crontab -e

# 添加这一行
0 8 * * * /usr/bin/python3 ~/clawd/tech-news/tech_news_daily.py >> ~/clawd/tech-news/output/cron.log 2>&1
```

---

## 📊 输出示例

### Discord 消息

```
🔥 技术日报 - 2026年03月04日

## 🌊 Vibe Coding

1. claude-plugins - Claude Code 插件市场
   ⭐ 120 | TypeScript | 2026-03-04

2. CodePilot - Claude Code 桌面 GUI
   ⭐ 85 | TypeScript | 2026-03-04
...
```

### Markdown 文件

**位置：** `~/clawd/tech-news/output/tech-news-2026-03-04.md`

**自动推送到：** `https://jinbo007.github.io/tech-news-2026-03-04.md`

---

## 🔧 自定义新闻源

编辑 `tech_news_daily.py` 中的 `NEWS_SOURCES` 字典：

```python
NEWS_SOURCES = {
    "vibe_coding": {
        "name": "🌊 Vibe Coding",
        "github_queries": [
            "vibe coding",
            "claude code",
            "cursor editor"
        ]
    },
    # 添加更多...
}
```

---

## 🛠️ 故障排查

| 问题 | 解决方案 |
|------|---------|
| Discord 发送失败 | 检查 Webhook URL 是否正确 |
| GitHub 推送失败 | 检查 Git 配置和网络连接 |
| 定时任务未运行 | 检查 launchd/cron 服务状态 |
| Python 依赖缺失 | 运行 `pip3 install requests feedparser` |

---

## 📝 依赖

- Python 3.6+
- requests
- feedparser (可选，用于 RSS)

---

## ✅ 验证安装

```bash
# 检查脚本是否存在
ls -la ~/clawd/tech-news/tech_news_daily.py

# 检查 launchd 任务（macOS）
launchctl list | grep tech-news

# 或检查 cron 任务（Linux）
crontab -l | grep tech-news

# 手动运行测试
python3 ~/clawd/tech-news/tech_news_daily.py
```

---

**开始安装：**
```bash
cd ~/clawd/tech-news
bash install.sh
```

---

*创建时间：2026-03-04*  
*最后更新：2026-03-04*
