#!/bin/bash
# 使用 unbuffer 运行 Python 脚本，实时显示输出

export PYTHONUNBUFFERED=1

echo "开始运行自动下载脚本..."
echo "时间: $(date)"
echo ""

python3 -u auto_download_songs.py

echo ""
echo "脚本执行完成"
echo "时间: $(date)"
