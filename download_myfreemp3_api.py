#!/usr/bin/env python3
"""
使用 myfreemp3.com.cn 的 API 下载歌曲
"""
import requests
import json
import time
import os
from urllib.parse import quote

# 待下载的歌曲清单
songs = [
    "红尘有缘",
    "红尘路上我们慢",
    "情已冷心已凉",
    "寂寞是我的归宿",
    "余生要把自己度过",
    "爱你和忘记我",
    "没爸妈何为家",
    "我的相思，你能否？",
    "人生只能往前走",
    "刻在心里的执念",
    "李英(无休的思念)",
    "能不能把你挽留？",
    "你是我最美的相遇",
    "情罪",
    "你不回头我就不",
    "叹岁月如刀",
    "今生有你陪着我",
    "以知己的名义爱你",
    "忘风忘雨忘不了你",
    "爱的世界只有你",
    "人生苦乐要自渡",
    "缘分来了就是你",
    "如果今生不能拥有",
    "我的真心你不在意",
    "我的快乐就是想你",
    "爸妈的爱最伟大",
    "其实我离不开你",
    "你留给我的伤太",
    "哑巴新娘",
    "酒醉的雨滴",
    "不要在我寂寞的时候",
    "为爱停留",
    "当我孤独的时候",
    "此生为你无怨无悔",
    "等你等了那么久",
    "错错错",
    "爱情码头",
    "包容",
    "人生的路",
    "爱到心累伤到心碎",
    "我不是除了你就",
    "偏偏放不下你",
    "我的思念你能否",
    "在你心里我是什么？",
    "见与不见，你都在",
    "我这一生没有可",
    "问问自己",
    "我的靠山是我自己",
    "谁不想活得很风光",
    "人生有多少苦难？心要洒脱",
    "能不能把你挽留？",
    "为什么爱的模棱两可？",
    "一曲红尘",
    "万爱千恩",
    "风雨中的诺言",
    "思念怎么断，记忆怎么删？",
    "人生路上不敢回想",
    "心甘情愿做你一生的知己",
    "转眼我们都老了",
    "苹果香",
    "六星街dj沈念版",
    "黑大是回乡带娃",
    "人生啊",
    "望爱却步",
    "走在人生的路口",
    "放下一切成全你",
    "我们再也没有了以后",
    "可以惯着你可以换了你",
    "今生太短来生太远",
    "还能相信谁？",
    "人生这条路，哭也不认输"
]

# 下载目录
download_dir = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
os.makedirs(download_dir, exist_ok=True)

# 已下载的歌曲
downloaded = set([
    "红尘有缘",
    "红尘路上我们慢",
    "莲的心事",
    "爱到心累伤到心碎",
    "寂寞是我的归宿",
    "人生啊",
    "人生只能往前走",
    "万爱千恩",
])

# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.myfreemp3.com.cn/",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://www.myfreemp3.com.cn",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}

# API 基础URL
BASE_URL = "https://www.myfreemp3.com.cn"

def search_song(song_name, search_type="netease"):
    """搜索歌曲"""
    try:
        url = f"{BASE_URL}/api/search"
        data = f"input={song_name}&filter=name&page=1&type={search_type}"

        response = requests.post(url, headers=headers, data=data, timeout=10)
        result = response.json()

        if result.get("code") == 200:
            data_list = result.get("data", {})
            song_list = data_list.get("list", [])
            if song_list:
                return song_list[0]  # 返回第一首歌
        return None

    except Exception as e:
        print(f"  ✗ 搜索失败: {e}")
        return None

def download_song(song_info, song_name):
    """下载歌曲"""
    try:
        # 尝试获取下载链接
        song_url = song_info.get("url_128") or song_info.get("url_320") or song_info.get("url_m4a")

        if not song_url:
            print(f"  ✗ 无下载链接")
            return False

        # 下载歌曲
        response = requests.get(song_url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

        # 构造文件名
        artist = song_info.get("singer", "未知")
        filename = f"{song_name}-{artist}.mp3"
        file_path = os.path.join(download_dir, filename)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # 检查文件大小
        if os.path.getsize(file_path) < 1000:
            os.remove(file_path)
            return False

        return True

    except Exception as e:
        print(f"  ✗ 下载失败: {e}")
        return False

def main():
    success_count = 0
    fail_count = 0
    skipped = 0
    failed_songs = []

    for i, song_name in enumerate(songs, 1):
        if song_name in downloaded:
            print(f"[{i}/{len(songs)}] ⊘ 跳过: {song_name} (已下载)")
            skipped += 1
            continue

        print(f"\n[{i}/{len(songs)}] 处理: {song_name}")

        # 尝试不同的搜索类型
        song_info = None
        for search_type in ["netease", "kuake", "ws"]:
            song_info = search_song(song_name, search_type)
            if song_info:
                print(f"  → 找到 ({search_type}): {song_info.get('name')} - {song_info.get('singer')}")
                break

        if not song_info:
            print(f"  ✗ 未找到歌曲")
            fail_count += 1
            failed_songs.append(song_name)
            continue

        # 下载歌曲
        if download_song(song_info, song_name):
            print(f"  ✓ 下载成功")
            success_count += 1
        else:
            print(f"  ✗ 下载失败")
            fail_count += 1
            failed_songs.append(song_name)

        # 避免请求过快
        time.sleep(2)

    # 输出统计
    print("\n" + "="*50)
    print(f"下载完成！")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"跳过: {skipped}")
    print(f"总计: {len(songs)}")
    print("="*50)

    if failed_songs:
        print("\n失败的歌曲:")
        for song in failed_songs:
            print(f"  - {song}")

if __name__ == "__main__":
    main()
