#!/bin/bash
# 传输脚本
# 用法: ./transfer.sh user@host

TARGET=${1:?"user@new-computer"}

if [ -z "$TARGET" ]; then
    echo "用法: ./transfer.sh user@host"
    echo "示例: ./transfer.sh jinbo@192.168.1.100"
    exit 1
fi

echo "📤 传输文件到 $TARGET..."
scp ~/clawd/migration/output/*.tar.gz ~/clawd/migration/output/install.sh ${TARGET}:~/

echo "✅ 传输完成！"
echo ""
echo "在新电脑上运行:"
echo "   chmod +x ~/install.sh"
echo "   ./install.sh"
