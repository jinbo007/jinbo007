#!/bin/bash
# 安装 OpenClaw Gateway Watchdog
# 支持 macOS (launchd) 和 Linux (cron)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WATCHDOG_SCRIPT="$SCRIPT_DIR/gateway-watchdog.sh"

echo "🦞 OpenClaw Gateway Watchdog 安装程序"
echo "======================================"

# 检查脚本是否存在
if [ ! -f "$WATCHDOG_SCRIPT" ]; then
    echo "❌ 找不到 watchdog 脚本: $WATCHDOG_SCRIPT"
    exit 1
fi

# 添加执行权限
chmod +x "$WATCHDOG_SCRIPT"
echo "✅ 已添加执行权限"

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - 使用 launchd
    echo ""
    echo "📱 检测到 macOS，使用 launchd 配置..."
    
    PLIST_FILE="$HOME/Library/LaunchAgents/com.openclaw.watchdog.plist"
    
    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.watchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$WATCHDOG_SCRIPT</string>
        <string>--notify</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>$HOME/.openclaw/logs/watchdog-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.openclaw/logs/watchdog-stderr.log</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF
    
    echo "✅ 已创建 launchd 配置: $PLIST_FILE"
    
    # 加载
    launchctl unload "$PLIST_FILE" 2>/dev/null
    launchctl load "$PLIST_FILE"
    
    echo "✅ 已加载 watchdog 服务"
    echo ""
    echo "📋 管理命令:"
    echo "   查看状态: launchctl list | grep openclaw"
    echo "   停止监控: launchctl unload $PLIST_FILE"
    echo "   启动监控: launchctl load $PLIST_FILE"
    echo "   查看日志: tail -f ~/.openclaw/logs/watchdog.log"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - 使用 cron
    echo ""
    echo "🐧 检测到 Linux，使用 cron 配置..."
    
    # 添加 cron 任务（每 5 分钟检查一次）
    CRON_JOB="*/5 * * * * $WATCHDOG_SCRIPT --notify"
    
    # 检查是否已存在
    if crontab -l 2>/dev/null | grep -q "gateway-watchdog"; then
        echo "⚠️ cron 任务已存在，跳过"
    else
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo "✅ 已添加 cron 任务"
    fi
    
    echo ""
    echo "📋 管理命令:"
    echo "   查看任务: crontab -l"
    echo "   编辑任务: crontab -e"
    echo "   查看日志: tail -f ~/.openclaw/logs/watchdog.log"
    
else
    echo "❌ 不支持的操作系统: $OSTYPE"
    echo "   你可以手动配置 cron 任务:"
    echo "   */5 * * * * $WATCHDOG_SCRIPT --notify"
    exit 1
fi

echo ""
echo "🎉 安装完成！"
echo "   Watchdog 将每 5 分钟检查一次 Gateway 状态"
echo "   如果检测到下线，会自动重启并发送通知"
