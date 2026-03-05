#!/usr/bin/env python3
"""
使用 Selenium 从 myfreemp3.com.cn 下载歌曲
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

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

def init_driver():
    """初始化浏览器驱动"""
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/Users/jinbo/.selenium/chrome-profile")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 设置下载目录
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def search_and_download(driver, song_name):
    """搜索并下载歌曲"""
    try:
        # 打开搜索页面
        driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
        time.sleep(2)

        # 查找搜索框
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input"))
        )
        search_box.clear()
        search_box.send_keys(song_name)
        time.sleep(1)

        # 提交搜索
        search_box.submit()
        time.sleep(3)

        # 查找搜索结果
        # 尝试多种可能的选择器
        possible_selectors = [
            (By.CSS_SELECTOR, "ul.music-list li"),
            (By.CSS_SELECTOR, ".list-item"),
            (By.CSS_SELECTOR, "li[data-id]"),
            (By.CSS_SELECTOR, "[data-song]"),
        ]

        song_element = None
        for by, selector in possible_selectors:
            try:
                elements = driver.find_elements(by, selector)
                if elements:
                    print(f"  → 找到 {len(elements)} 个结果，使用选择器: {selector}")
                    song_element = elements[0]  # 取第一个结果
                    break
            except:
                continue

        if not song_element:
            print(f"  ✗ 未找到搜索结果")
            return False

        # 点击歌曲
        song_element.click()
        time.sleep(2)

        # 查找下载按钮
        download_button = None
        try:
            # 尝试多种可能的下载按钮选择器
            download_selectors = [
                (By.CSS_SELECTOR, ".TLH_download"),
                (By.CSS_SELECTOR, ".download"),
                (By.CSS_SELECTOR, "button[download]"),
                (By.CSS_SELECTOR, "a[download]"),
                (By.CSS_SELECTOR, "[data-download]"),
            ]

            for by, selector in download_selectors:
                try:
                    buttons = driver.find_elements(by, selector)
                    if buttons:
                        download_button = buttons[0]
                        break
                except:
                    continue

            if download_button:
                download_button.click()
                time.sleep(3)
                print(f"  ✓ 已点击下载按钮")
                return True
            else:
                print(f"  ✗ 未找到下载按钮")
                return False

        except Exception as e:
            print(f"  ✗ 点击下载失败: {e}")
            return False

    except Exception as e:
        print(f"  ✗ 搜索失败: {e}")
        return False

def main():
    """主函数"""
    driver = init_driver()

    success_count = 0
    fail_count = 0
    skipped = 0
    failed_songs = []

    try:
        for i, song in enumerate(songs, 1):
            if song in downloaded:
                print(f"[{i}/{len(songs)}] ⊘ 跳过: {song} (已下载)")
                skipped += 1
                continue

            print(f"\n[{i}/{len(songs)}] 处理: {song}")

            if search_and_download(driver, song):
                print(f"  ✓ 下载成功")
                success_count += 1
            else:
                print(f"  ✗ 下载失败")
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
    main()
