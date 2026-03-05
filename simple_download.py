#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
import time

DOWNLOAD_DIR = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

songs = ["青花瓷", "七里香", "晴天", "简单爱", "告白气球"]

for song in songs:
    filename = f"周杰伦 - {song}.mp3"
    print(f"\n🔍 搜索: {song}")

    try:
        # 访问搜索页面
        search_url = f"https://www.myfreemp3.com.cn/?page=searchPage"
        headers = {'User-Agent': 'Mozilla/5.0'}

        # 使用API格式
        api_url = f"https://www.myfreemp3.com.cn/?type=netease&name={requests.utils.quote(song)}"
        print(f"📡 请求: {api_url[:80]}...")

        response = requests.get(api_url, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            # 尝试从响应中提取音频链接
            text = response.text

            # 查找163音乐链接
            if "music.126.net" in text:
                import re
                matches = re.findall(r'(https://[^"\']*\.music\.126\.net/[^"\']*\.mp3[^"\']*)', text)
                if matches:
                    download_url = matches[0]
                    print(f"✓ 找到链接: {download_url[:60]}...")

                    # 下载
                    print(f"⬇️  下载中...")
                    resp = requests.get(download_url, headers=headers, timeout=30)

                    if resp.status_code == 200:
                        filepath = os.path.join(DOWNLOAD_DIR, filename)
                        with open(filepath, 'wb') as f:
                            f.write(resp.content)
                        print(f"✓ 完成: {filename}")
                    else:
                        print(f"✗ 下载失败")
                else:
                    print(f"✗ 未找到MP3链接")
            else:
                print(f"✗ 响应中未找到音频链接")
        else:
            print(f"✗ 请求失败")

    except Exception as e:
        print(f"✗ 错误: {e}")

    time.sleep(2)

print(f"\n✓ 全部完成")
