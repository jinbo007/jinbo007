#!/bin/bash
# Vibe Coding 自动新闻推送 - 安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEWS_SCRIPT="$SCRIPT_DIR/daily_news_simple.py"

echo "🦞 Vibe Coding 新闻推送 - 安装程序"
echo "=================================="

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装 Python 3"
    exit 1
fi

echo "✅ Python 3 已安装: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
pip3 install requests --quiet 2>/dev/null || pip install requests --quiet 2>/dev/null || true

# 创建输出目录
mkdir -p ~/clawd/vibe-news/output

# 配置说明
echo ""
echo "📋 配置说明"
echo "=================================="
echo ""
echo "📱 Discord Webhook (必需)"
echo "   置信: 1465634481837834291"
echo "   - 在 Discord 服务器设置 → Integrations → Webhooks"
echo "   - 创建 New Webhook"
echo "   - 复制 Webhook URL"
echo "   - 填入下面:"
echo ""
echo "   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1465634481837834291/YOUR_TOKEN"
echo ""
echo "⚠️  重要: 获取到 Webhook URL 后，将 URL 保存到脚本文件"
echo ""

# macOS launchd 配置
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📅 配置 macOS 定时任务 (launchd)..."
    
    PLIST_FILE="$HOME/Library/LaunchAgents/com.openclaw.vibe-news.plist"
    
    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>Vibe Coding Daily News</string>
    <key>Program</key>
    <string>/usr/bin/python3</string>
    <key>ProgramArguments</key>
    <array>
        <string>$NEWS_SCRIPT</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$HOME/clawd/vibe-news/output/cron.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/clawd/vibe-news/output/cron-error.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF
    
    echo "✅ 已创建 launchd 配置: $PLIST_FILE"
    
    # 加载任务
    launchctl unload "$PLIST_FILE" 2>/dev/null || true
    launchctl load "$PLIST_FILE"
    
    echo "✅ 已加载定时任务"
    echo ""
    echo "📋 管理命令:"
    echo "   查看状态: launchctl list | grep vibe-news"
    echo "   手动运行: python3 $NEWS_SCRIPT"
    echo "   停止任务: launchctl unload $PLIST_FILE"
    echo "   查看日志: tail -f $HOME/clawd/vibe-news/output/cron.log"

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📅 配置 Linux 定时任务 (cron)..."
    
    # 检查是否已存在
    if crontab -l 2>/dev/null | grep -q "vibe-news"; then
        echo "⚠️ cron 任务已存在，跳过"
    else
        CRON_JOB="0 8 * * * /usr/bin/python3 $NEWS_SCRIPT >> $HOME/clawd/vibe-news/output/cron.log 2>&1"
        
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo "✅ 已添加 cron 任务"
    fi
    
    echo ""
    echo "📋 管理命令:"
    echo "   查看任务: crontab -l"
    echo "   编辑任务: crontab -e"
    echo "   查看日志: tail -f $HOME/clawd/vibe-news/output/cron.log"
fi

# 测试运行
echo ""
read -p "是否现在测试运行一次？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🧪 测试运行..."
    python3 "$NEWS_SCRIPT"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📝 下一步:"
echo "   1. 获取 Discord Webhook URL 并更新脚本中的 DISCORD_WEBHOOK"
echo "   2. 编辑 ~/clawd/vibe-news/daily_news_simple.py 中的 DISCORD_WEBHOOK 变量"
echo "   3. 手动运行测试: python3 ~/clawd/vibe-news/daily_news_simple.py"
echo ""
echo "⏰ 从明天开始，每天早上 8:00 自动发送新闻！"
