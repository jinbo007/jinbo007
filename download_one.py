#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载单首歌曲
"""

import requests
import os

DOWNLOAD_DIR = "/Users/jinbo/Documents/AIProject/clawbot/mp3"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

song = "青花瓷"
filename = f"周杰伦 - {song}.mp3"
filepath = os.path.join(DOWNLOAD_DIR, filename)

print(f"🔍 下载: {song}")

# 使用备用方法 - 直接搜索网易云音乐
try:
    search_url = f"https://music.163.com/api/search/pc/web/keyword/get?s={song}&type=1&limit=1"
    response = requests.get(search_url, timeout=10)
    print(f"搜索状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"返回数据: {data}")
    else:
        print(f"请求失败")

except Exception as e:
    print(f"错误: {e}")
