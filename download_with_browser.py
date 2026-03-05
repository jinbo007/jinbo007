#!/usr/bin/env python3
"""
通过浏览器获取 myfreemp3 搜索结果并下载
需要浏览器中运行 JavaScript 代码
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

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

def download_url(url, filename):
    """下载文件"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.myfreemp3.com.cn/",
        }
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

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
        print(f"    下载失败: {e}")
        return False

def main():
    chrome_options = Options()
    # 不使用无头模式，方便观察
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    success_count = 0
    fail_count = 0
    skipped = 0
    failed_songs = []

    try:
        # 打开网站
        driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
        time.sleep(3)

        # 等待页面加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input"))
        )

        for i, song in enumerate(songs, 1):
            if song in downloaded:
                print(f"[{i}/{len(songs)}] ⊘ 跳过: {song} (已下载)")
                skipped += 1
                continue

            print(f"\n[{i}/{len(songs)}] 处理: {song}")

            try:
                # 输入歌曲名
                search_box = driver.find_element(By.ID, "input")
                search_box.clear()
                search_box.send_keys(song)
                time.sleep(1)

                # 提交搜索
                search_box.submit()
                time.sleep(3)

                # 获取当前URL
                current_url = driver.current_url
                print(f"  当前URL: {current_url}")

                # 等待搜索结果
                time.sleep(2)

                # 执行JavaScript获取歌曲信息
                # 尝试从页面中提取第一个搜索结果
                js_script = """
                // 尝试从页面中查找歌曲链接
                var audio = document.querySelector('audio');
                if (audio && audio.src) {
                    return audio.src;
                }

                // 尝试查找下载链接
                var links = document.querySelectorAll('a');
                for (var i = 0; i < links.length; i++) {
                    var href = links[i].href;
                    if (href && (href.includes('.mp3') || href.includes('.m4a'))) {
                        return href;
                    }
                }

                return null;
                """

                download_url_str = driver.execute_script(js_script)

                if download_url_str:
                    print(f"  ✓ 找到下载链接: {download_url_str[:80]}...")

                    # 构造文件名
                    filename = f"{song}.mp3"

                    if download_url(download_url_str, filename):
                        print(f"  ✓ 下载成功")
                        success_count += 1
                    else:
                        print(f"  ✗ 下载失败")
                        fail_count += 1
                        failed_songs.append(song)
                else:
                    print(f"  ✗ 未找到下载链接")
                    fail_count += 1
                    failed_songs.append(song)

                # 返回搜索页面
                driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
                time.sleep(2)

            except Exception as e:
                print(f"  ✗ 处理失败: {e}")
                fail_count += 1
                failed_songs.append(song)

            # 避免请求过快
            time.sleep(2)

    finally:
        driver.quit()

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
    print("开始下载...")
    print("浏览器将打开并自动下载歌曲")
    print("请不要关闭浏览器窗口\n")
    main()
