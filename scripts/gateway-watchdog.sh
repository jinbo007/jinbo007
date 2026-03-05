#!/bin/bash
# OpenClaw Gateway Watchdog - 自动监控和重启
# 用法: ./gateway-watchdog.sh [--notify]

LOG_FILE="$HOME/.openclaw/logs/watchdog.log"
MAX_LOG_SIZE=10485760  # 10MB
NOTIFY_ON_RESTART=${1:-"--notify"}

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    # 日志轮转
    if [ -f "$LOG_FILE" ] && [ $(wc -c < "$LOG_FILE") -gt $MAX_LOG_SIZE ]; then
        mv "$LOG_FILE" "${LOG_FILE}.old"
    fi
}

# 检查 Gateway 是否运行
check_gateway() {
    pgrep -f "openclaw gateway" > /dev/null 2>&1
    return $?
}

# 检查 Gateway 健康状态（通过 API）
check_health() {
    local status
    status=$(openclaw status 2>&1)
    if echo "$status" | grep -q "critical"; then
        return 1
    fi
    return 0
}

# 重启 Gateway
restart_gateway() {
    log "⚠️ Gateway 未运行，正在重启..."
    
    # 先停止（以防万一）
    openclaw gateway stop 2>/dev/null
    sleep 2
    
    # 启动
    openclaw gateway start 2>&1
    sleep 5
    
    # 验证启动成功
    if check_gateway; then
        log "✅ Gateway 重启成功"
        
        # 发送通知
        if [ "$NOTIFY_ON_RESTART" = "--notify" ]; then
            send_notification "OpenClaw Gateway 已自动重启" "检测到服务停止，已自动恢复运行"
        fi
        return 0
    else
        log "❌ Gateway 重启失败！"
        send_notification "⚠️ OpenClaw Gateway 重启失败" "请手动检查服务状态"
        return 1
    fi
}

# 发送系统通知（macOS）
send_notification() {
    local title="$1"
    local message="$2"
    
    if command -v osascript &> /dev/null; then
        osascript -e "display notification \"$message\" with title \"$title\"" 2>/dev/null
    fi
    
    # 也记录到心跳状态
    echo "{
  \"lastRestart\": \"$(date -Iseconds)\",
  \"reason\": \"$message\"
}" > "$HOME/clawd/memory/watchdog-last-restart.json"
}

# 主逻辑
main() {
    log "🔍 检查 Gateway 状态..."
    
    if ! check_gateway; then
        log "❌ Gateway 未运行"
        restart_gateway
        exit $?
    fi
    
    if ! check_health; then
        log "⚠️ Gateway 健康检查失败"
        restart_gateway
        exit $?
    fi
    
    log "✅ Gateway 运行正常"
    exit 0
}

main
