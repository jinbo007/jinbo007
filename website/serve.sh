#!/bin/bash
# 个人网站本地预览服务器

PORT=${1:-8080}
WEBSITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🌐 启动个人网站服务器..."
echo "   端口: $PORT"
echo "   地址: http://localhost:$PORT"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

cd "$WEBSITE_DIR"
python3 -m http.server $PORT 2>/dev/null || python -m http.server $PORT
