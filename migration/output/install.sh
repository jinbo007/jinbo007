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
