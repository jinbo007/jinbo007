#!/usr/bin/env python3
"""
检查并标记已下载的歌曲
"""
import os
import re

# 下载目录
download_dir = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
download_list_file = "/Users/jinbo/Documents/AIProject/clawbot/下载清单.txt"

# 获取已下载的歌曲
downloaded_songs = set()
for f in os.listdir(download_dir):
    if f.endswith('.mp3'):
        # 提取歌曲名（去除文件扩展名和歌手信息）
        song_name = f.replace('.mp3', '').split('-')[0].strip()
        downloaded_songs.add(song_name)

print(f"已下载歌曲: {len(downloaded_songs)} 首")
print("="*60)

# 读取下载清单
with open(download_list_file, 'r', encoding='utf-8') as f:
    songs = f.read().strip().split('\n')

print(f"待下载歌曲: {len(songs)} 首")
print("="*60)

# 处理下载清单
marked_songs = []
marked_count = 0

for song in songs:
    song_clean = song.strip()
    if not song_clean:
        continue

    # 检查是否已下载
    is_downloaded = False
    for downloaded in downloaded_songs:
        # 模糊匹配（包含关系）
        if downloaded in song_clean or song_clean in downloaded:
            is_downloaded = True
            break

    if is_downloaded:
        marked_songs.append(f"[已下载] {song_clean}")
        marked_count += 1
        print(f"✓ {song_clean}")
    else:
        marked_songs.append(song_clean)
        print(f"  {song_clean}")

print("="*60)
print(f"已标记: {marked_count} 首")
print(f"待下载: {len(songs) - marked_count} 首")
print("="*60)

# 写回文件（标记已下载的歌曲）
with open(download_list_file, 'w', encoding='utf-8') as f:
    for song in marked_songs:
        f.write(song + '\n')

print(f"\n✓ 已更新下载清单: {download_list_file}")
