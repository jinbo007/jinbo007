#!/bin/bash
# OpenClaw 完整迁移脚本
# 用法: ./migrate.sh [pack|transfer|unpack]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE=${1:-"pack"}

echo "🦞 OpenClaw 完整迁移工具"
echo "================================"

# 创建输出目录
mkdir -p ~/clawd/migration/output

if [ "$MODE" = "pack" ]; then
    echo ""
    echo "📦 开始打包..."
    
    # 1. 打包工作区
    echo "  • 打包工作区..."
    tar -czf ~/clawd/migration/output/clawd-workspace.tar.gz -C ~/clawd \
        --exclude=".git" \
        --exclude="node_modules" \
        --exclude="migration" \
        .
    
    # 2. 打包 OpenClaw 配置
    echo "  • 打包配置..."
    tar -czf ~/clawd/migration/output/openclaw-config.tar.gz -C ~/.openclaw \
        openclaw.json \
        credentials/ \
        devices/ \
        cron/ \
        clawdbot.json 2>/dev/null || true
    
    # 3. 打包内置技能
    echo "  • 打包内置技能..."
    tar -czf ~/clawd/migration/output/openclaw-skills.tar.gz -C ~/openclaw/skills .
    
    # 4. 打包自定义技能（如果存在）
    if [ -d ~/Documents/AIProject/clawbot/.trae/skills ]; then
        echo "  • 打包自定义技能..."
        tar -czf ~/clawd/migration/output/custom-skills.tar.gz \
            -C ~/Documents/AIProject/clawbot/.trae/skills .
    fi
    
    # 5. 创建安装脚本
    cat > ~/clawd/migration/output/install.sh << 'INSTALL'
#!/bin/bash
# OpenClaw 安装脚本
# 在新电脑上运行

set -e

echo "🦞 OpenClaw 安装程序"
echo "================================"

# 检查是否存在压缩包
for pkg in clawd-workspace.tar.gz openclaw-config.tar.gz openclaw-skills.tar.gz; do
    if [ ! -f "$pkg" ]; then
        echo "❌ 找不到: $pkg"
        exit 1
    fi
done

# 1. 安装 OpenClaw（如果未安装）
if ! command -v openclaw &> /dev/null; then
    echo "📦 安装 OpenClaw..."
    npm install -g openclaw
fi

# 2. 解压工作区
echo "📂 解压工作区..."
mkdir -p ~/clawd
tar -xzf clawd-workspace.tar.gz -C ~/clawd

# 3. 解压配置
echo "⚙️ 解压配置..."
mkdir -p ~/.openclaw
tar -xzf openclaw-config.tar.gz -C ~/.openclaw

# 设置权限
chmod 700 ~/.openclaw/credentials 2>/dev/null || true

# 4. 解压技能
echo "🧩 解压技能..."
mkdir -p ~/openclaw/skills
tar -xzf openclaw-skills.tar.gz -C ~/openclaw/skills

# 5. 解压自定义技能（如果存在）
if [ -f custom-skills.tar.gz ]; then
    echo "🎵 解压自定义技能..."
    mkdir -p ~/Documents/AIProject/clawbot/.trae/skills
    tar -xzf custom-skills.tar.gz -C ~/Documents/AIProject/clawbot/.trae/skills
fi

# 6. 启动服务
echo "🚀 启动 Gateway..."
openclaw gateway start

echo ""
echo "✅ 安装完成！"
echo ""
echo "📋 后续步骤："
echo "   1. 重新配对 WhatsApp（如需要）"
echo "   2. 测试所有渠道"
echo "   3. 测试自定义技能"
echo ""
echo "🎉 欢迎使用 OpenClaw！"
INSTALL

    chmod +x ~/clawd/migration/output/install.sh
    
    # 6. 创建传输脚本
    cat > ~/clawd/migration/output/transfer.sh << 'TRANSFER'
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
TRANSFER

    chmod +x ~/clawd/migration/output/transfer.sh
    
    echo ""
    echo "✅ 打包完成！"
    echo ""
    echo "📁 输出文件："
    ls -lh ~/clawd/migration/output/
    echo ""
    echo "📋 下一步："
    echo "   1. 将 output/ 目录传输到新电脑"
    echo "   2. 在新电脑上运行 install.sh"
    echo ""
    echo "💡 传输方式："
    echo "   • SCP: ~/clawd/migration/output/transfer.sh user@host"
    echo "   • U盘: 复制 output/ 目录"
    echo "   • 云盘: 上传 output/ 目录（注意：不要分享给他人）"

elif [ "$MODE" = "transfer" ]; then
    TARGET=${2:-""}
    
    if [ -z "$TARGET" ]; then
        echo "用法: ./migrate.sh transfer user@host"
        echo "示例: ./migrate.sh transfer jinbo@192.168.1.100"
        exit 1
    fi
    
    ~/clawd/migration/output/transfer.sh "$TARGET"

elif [ "$MODE" = "unpack" ]; then
    echo "📂 解压模式（在新电脑上运行）"
    cd ~/clawd/migration/output
    ./install.sh
fi
