#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Music Downloader - 从 myfreemp3.com.cn 下载音乐
"""

import requests
import json
import time
import os
from urllib.parse import quote

# 配置
DOWNLOAD_DIR = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
BASE_URL = "https://www.myfreemp3.com.cn"
SEARCH_URL = f"{BASE_URL}/?page=searchPage"

def ensure_download_dir():
    """确保下载目录存在"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def search_song(keyword):
    """搜索歌曲"""
    print(f"🔍 搜索: {keyword}")
    # 使用API搜索
    search_api = f"{BASE_URL}/?type=netease&name={quote(keyword)}"
    try:
        response = requests.get(search_api, timeout=10)
        if response.status_code == 200:
            print(f"✓ 找到搜索结果")
            return search_api
    except Exception as e:
        print(f"✗ 搜索失败: {e}")
    return None

def get_download_links(search_url, keyword):
    """获取下载链接"""
    try:
        # 尝试直接访问搜索结果页面
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            # 尝试从页面中提取音频链接
            html = response.text

            # 查找可能的MP3链接
            # 通常在audio标签或特定API响应中
            if ".mp3" in html or "music.126.net" in html:
                print(f"✓ 在页面中找到音频链接")
                # 这里需要更复杂的解析，暂时简化
                return extract_audio_links(html)

            # 尝试调用API获取链接
            # myfreemp3的API格式
            api_url = f"https://www.myfreemp3.com.cn/?type=netease&name={quote(keyword)}"
            return [api_url]
    except Exception as e:
        print(f"✗ 获取下载链接失败: {e}")
    return []

def extract_audio_links(html):
    """从HTML中提取音频链接"""
    import re
    # 匹配网易云音乐链接
    netease_pattern = r'https://[^"\']*\.music\.126\.net/[^"\']*\.mp3[^"\']*'
    links = re.findall(netease_pattern, html)
    return links[:5]  # 最多返回5个链接

def download_mp3(url, filename):
    """下载MP3文件"""
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    print(f"⬇️  下载中: {filename}")

    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\r   进度: {progress:.1f}%", end='')

        print(f"\n✓ 下载完成: {filepath}")
        return True
    except Exception as e:
        print(f"\n✗ 下载失败: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

def main():
    """主函数"""
    ensure_download_dir()

    keyword = "美丽的神话"
    print(f"🎵 开始下载: {keyword}\n")

    # 搜索歌曲
    search_url = search_song(keyword)
    if not search_url:
        print(f"✗ 未找到: {keyword}")
        return

    # 获取下载链接
    print(f"🔗 获取下载链接...")
    download_links = get_download_links(search_url, keyword)

    if not download_links:
        print(f"✗ 未找到下载链接")
        return

    print(f"✓ 找到 {len(download_links)} 个可能的下载链接")

    # 下载
    for i, link in enumerate(download_links[:1], 1):  # 只下载第一个
        filename = f"{keyword}.mp3"
        if download_mp3(link, filename):
            print(f"\n✓ 成功下载: {keyword}")
            return

    print(f"\n✗ 下载失败: {keyword}")

if __name__ == "__main__":
    main()
