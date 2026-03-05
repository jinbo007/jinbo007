#!/usr/bin/env python3
"""
Vibe Coding 新闻自动推送
每天早上 8:00 发送到 Discord 和 WhatsApp
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict

# 配置
CONFIG = {
    "discord_webhook": os.environ.get("DISCORD_WEBHOOK_URL", ""),
    "whatsapp_api": os.environ.get("WHATSAPP_API_URL", ""),
    "github_token": os.environ.get("GITHUB_TOKEN", ""),
    "output_dir": os.path.expanduser("~/clawd/vibe-news")
}

# 新闻源
NEWS_SOURCES = {
    "github_ai": "https://api.github.com/search/repositories?q=ai+OR+llm+OR+claude+OR+gpt&sort=stars&order=desc&per_page=5",
    "github_vibe": "https://api.github.com/search/repositories?q=vibe+coding+OR+claude+code+OR+cursor&sort=updated&per_page=5",
    "producthunt": "https://api.producthunt.com/v2/api/graphql",
}

def fetch_github_trending() -> List[Dict]:
    """获取 GitHub AI 相关热门项目"""
    try:
        headers = {}
        if CONFIG["github_token"]:
            headers["Authorization"] = f"token {CONFIG['github_token']}"
        
        response = requests.get(NEWS_SOURCES["github_ai"], headers=headers, timeout=10)
        data = response.json()
        
        news = []
        for item in data.get("items", [])[:5]:
            news.append({
                "title": item["name"],
                "description": item.get("description", "无描述")[:100],
                "url": item["html_url"],
                "stars": item["stargazers_count"],
                "source": "GitHub"
            })
        return news
    except Exception as e:
        print(f"获取 GitHub 数据失败: {e}")
        return []

def fetch_github_vibe() -> List[Dict]:
    """获取 Vibe Coding 相关更新"""
    try:
        headers = {}
        if CONFIG["github_token"]:
            headers["Authorization"] = f"token {CONFIG['github_token']}"
        
        response = requests.get(NEWS_SOURCES["github_vibe"], headers=headers, timeout=10)
        data = response.json()
        
        news = []
        for item in data.get("items", [])[:5]:
            news.append({
                "title": item["name"],
                "description": item.get("description", "无描述")[:100],
                "url": item["html_url"],
                "updated": item["updated_at"][:10],
                "source": "GitHub Vibe"
            })
        return news
    except Exception as e:
        print(f"获取 Vibe Coding 数据失败: {e}")
        return []

def fetch_web_news() -> List[Dict]:
    """从网络获取新闻（使用 Brave Search API）"""
    # 如果有 Brave Search API key
    brave_api_key = os.environ.get("BRAVE_API_KEY", "")
    if not brave_api_key:
        return []
    
    try:
        headers = {"X-Subscription-Token": brave_api_key}
        params = {
            "q": "vibe coding OR claude code OR cursor editor OR AI coding",
            "count": 5,
            "freshness": "pd"  # 过去一天
        }
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params,
            timeout=10
        )
        data = response.json()
        
        news = []
        for item in data.get("web", {}).get("results", [])[:5]:
            news.append({
                "title": item["title"],
                "description": item.get("description", "")[:100],
                "url": item["url"],
                "source": "Web"
            })
        return news
    except Exception as e:
        print(f"获取网络新闻失败: {e}")
        return []

def generate_summary(github_news: List, vibe_news: List, web_news: List) -> str:
    """生成新闻总结"""
    today = datetime.now().strftime("%Y年%m月%d日")
    
    summary = f"""# 🔥 Vibe Coding 日报 - {today}

"""
    
    if github_news:
        summary += "## 📦 GitHub 热门 AI 项目\n\n"
        for i, item in enumerate(github_news, 1):
            summary += f"{i}. **{item['title']}** ⭐ {item['stars']:,}\n"
            summary += f"   {item['description']}\n"
            summary += f"   🔗 {item['url']}\n\n"
    
    if vibe_news:
        summary += "## 🌊 Vibe Coding 最新动态\n\n"
        for i, item in enumerate(vibe_news, 1):
            summary += f"{i}. **{item['title']}** (更新: {item['updated']})\n"
            summary += f"   {item['description']}\n"
            summary += f"   🔗 {item['url']}\n\n"
    
    if web_news:
        summary += "## 🌐 相关新闻\n\n"
        for i, item in enumerate(web_news, 1):
            summary += f"{i}. **{item['title']}**\n"
            summary += f"   {item['description']}\n"
            summary += f"   🔗 {item['url']}\n\n"
    
    if not github_news and not vibe_news and not web_news:
        summary += "暂无新内容\n"
    
    summary += f"""
---
🤖 自动生成 by OpenClaw | {datetime.now().strftime("%H:%M:%S")}
"""
    
    return summary

def format_for_discord(summary: str) -> Dict:
    """格式化为 Discord 消息"""
    return {
        "content": summary[:2000],  # Discord 消息限制
        "username": "Vibe Coding Bot",
        "avatar_url": "https://claude.ai/images/claude_app_icon.png"
    }

def send_to_discord(summary: str) -> bool:
    """发送到 Discord"""
    webhook_url = CONFIG["discord_webhook"]
    if not webhook_url:
        print("⚠️ 未配置 Discord Webhook URL")
        return False
    
    try:
        payload = format_for_discord(summary)
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ 已发送到 Discord")
            return True
        else:
            print(f"❌ Discord 发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Discord 发送异常: {e}")
        return False

def send_to_whatsapp(summary: str) -> bool:
    """发送到 WhatsApp"""
    # 使用 OpenClaw 的 message 工具
    # 这里保存到文件，让 OpenClaw 的 cron 处理
    output_file = os.path.join(CONFIG["output_dir"], "whatsapp_message.txt")
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"✅ WhatsApp 消息已保存到: {output_file}")
    return True

def save_daily_report(summary: str):
    """保存日报到文件"""
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(CONFIG["output_dir"], f"daily-{today}.md")
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"✅ 日报已保存到: {output_file}")

def main():
    print(f"🤖 开始生成 Vibe Coding 日报...")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取新闻
    github_news = fetch_github_trending()
    vibe_news = fetch_github_vibe()
    web_news = fetch_web_news()
    
    # 生成总结
    summary = generate_summary(github_news, vibe_news, web_news)
    
    # 保存日报
    save_daily_report(summary)
    
    # 发送到 Discord
    send_to_discord(summary)
    
    # 发送到 WhatsApp
    send_to_whatsapp(summary)
    
    print(f"✅ 完成!")
    return summary

if __name__ == "__main__":
    main()
