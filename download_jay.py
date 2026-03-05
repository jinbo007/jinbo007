#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量下载周杰伦热门歌曲
"""

import requests
import json
import time
import os
from urllib.parse import quote

# 配置
DOWNLOAD_DIR = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
BASE_URL = "https://www.myfreemp3.com.cn"

def ensure_download_dir():
    """确保下载目录存在"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def search_song(keyword):
    """搜索歌曲"""
    print(f"🔍 搜索: {keyword}")
    search_api = f"{BASE_URL}/?type=netease&name={quote(keyword)}"
    try:
        response = requests.get(search_api, timeout=10)
        if response.status_code == 200:
            print(f"✓ 找到搜索结果")
            return search_api
    except Exception as e:
        print(f"✗ 搜索失败: {e}")
    return None

def extract_audio_links(html):
    """从HTML中提取音频链接"""
    import re
    netease_pattern = r'https://[^"\']*\.music\.126\.net/[^"\']*\.mp3[^"\']*'
    links = re.findall(netease_pattern, html)
    return links[:5]

def get_download_links(search_url, keyword):
    """获取下载链接"""
    try:
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            html = response.text
            if ".mp3" in html or "music.126.net" in html:
                links = extract_audio_links(html)
                if links:
                    print(f"✓ 找到 {len(links)} 个音频链接")
                    return links

            # 如果没找到，返回搜索URL作为fallback
            return [search_url]
    except Exception as e:
        print(f"✗ 获取下载链接失败: {e}")
    return []

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
                        if downloaded % 81920 == 0:  # 每10个chunk显示一次
                            print(f"\r   进度: {progress:.1f}%", end='', flush=True)

        print(f"\r   进度: 100.0%")
        print(f"✓ 完成: {filepath}")
        return True
    except Exception as e:
        print(f"\n✗ 下载失败: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

def main():
    """主函数"""
    ensure_download_dir()

    # 周杰伦热门歌曲列表
    songs = [
        "青花瓷",
        "七里香",
        "晴天",
        "简单爱",
        "告白气球",
        "稻香",
        "夜曲",
        "双截棍",
        "东风破",
        "发如雪"
    ]

    print(f"🎵 开始下载周杰伦热门歌曲 ({len(songs)}首)\n")
    print("=" * 50)

    success = []
    failed = []

    for i, song in enumerate(songs, 1):
        print(f"\n[{i}/{len(songs)}] {song}")

        search_url = search_song(song)
        if not search_url:
            failed.append(song)
            continue

        print(f"🔗 获取下载链接...")
        download_links = get_download_links(search_url, song)

        if not download_links:
            print(f"✗ 未找到下载链接")
            failed.append(song)
            continue

        filename = f"周杰伦 - {song}.mp3"
        if download_mp3(download_links[0], filename):
            success.append(song)
        else:
            failed.append(song)

        # 避免请求过快
        time.sleep(2)

    print("\n" + "=" * 50)
    print(f"\n📊 下载完成:")
    print(f"✓ 成功: {len(success)}首")
    print(f"✗ 失败: {len(failed)}首")

    if success:
        print(f"\n成功下载:")
        for s in success:
            print(f"  ✓ {s}")

    if failed:
        print(f"\n失败:")
        for f in failed:
            print(f"  ✗ {f}")

if __name__ == "__main__":
    main()
