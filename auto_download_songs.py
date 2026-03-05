#!/usr/bin/env python3
"""
使用 Selenium 从 myfreemp3.com.cn 自动下载歌曲
默认下载第一个搜索结果，如果没有找到则跳过
"""
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

def get_downloaded_files():
    """获取已下载的文件列表"""
    downloaded = set()
    for f in os.listdir(download_dir):
        if f.endswith('.mp3'):
            # 从文件名中提取歌曲名（去除后缀和歌手信息）
            song_name = f.replace('.mp3', '').split('-')[0].strip()
            downloaded.add(song_name)
    return downloaded

def download_audio(url, filename):
    """下载音频文件"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.myfreemp3.com.cn/",
        }
        response = requests.get(url, headers=headers, stream=True, timeout=60)
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

def search_and_download(driver, song_name):
    """搜索并下载歌曲"""
    try:
        print(f"  正在搜索: {song_name}")

        # 打开搜索页面
        driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
        time.sleep(2)

        # 查找并输入搜索框
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input"))
        )
        search_box.clear()
        search_box.send_keys(song_name)
        time.sleep(1)

        # 提交搜索
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # 尝试查找搜索结果
        # 方法1: 查找包含歌曲名的列表项
        results = driver.find_elements(By.CSS_SELECTOR, "li")
        print(f"  找到 {len(results)} 个 li 元素")

        song_element = None
        for elem in results:
            try:
                elem_text = elem.text
                # 查找包含歌曲名的元素（排除导航菜单等）
                if elem_text and song_name in elem_text and len(elem_text) < 200:
                    print(f"  找到结果: {elem_text[:50]}")
                    song_element = elem
                    break
            except:
                continue

        if not song_element:
            print(f"  ✗ 未找到搜索结果，跳过")
            return False

        # 点击第一个结果
        song_element.click()
        time.sleep(3)

        # 查找音频元素
        audio_elem = driver.find_elements(By.TAG_NAME, "audio")
        if audio_elem:
            audio_url = audio_elem[0].get_attribute("src")
            if audio_url:
                print(f"  ✓ 找到音频URL: {audio_url[:60]}...")
                filename = f"{song_name}.mp3"

                if download_audio(audio_url, filename):
                    print(f"  ✓ 下载成功")
                    return True
                else:
                    print(f"  ✗ 下载失败")
                    return False

        # 方法2: 查找包含MP3链接的元素
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and ('.mp3' in href or '.m4a' in href):
                print(f"  ✓ 找到下载链接: {href[:60]}...")
                filename = f"{song_name}.mp3"

                if download_audio(href, filename):
                    print(f"  ✓ 下载成功")
                    return True
                else:
                    print(f"  ✗ 下载失败")
                    return False

        print(f"  ✗ 未找到下载链接")
        return False

    except Exception as e:
        print(f"  ✗ 搜索失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    # 获取已下载的文件
    downloaded = get_downloaded_files()
    print(f"已下载: {len(downloaded)} 首歌曲")

    # 初始化浏览器
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)

    success_count = 0
    fail_count = 0
    skipped = 0
    failed_songs = []

    try:
        for i, song in enumerate(songs, 1):
            # 检查是否已下载
            if song in downloaded:
                print(f"[{i}/{len(songs)}] ⊘ 跳过: {song} (已下载)")
                skipped += 1
                continue

            print(f"\n[{i}/{len(songs)}] 处理: {song}")

            if search_and_download(driver, song):
                success_count += 1
                downloaded.add(song)
            else:
                fail_count += 1
                failed_songs.append(song)

            # 避免请求过快
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\n用户中断下载...")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

        # 输出统计
        print("\n" + "="*60)
        print(f"下载完成！")
        print(f"成功: {success_count}")
        print(f"失败: {fail_count}")
        print(f"跳过: {skipped}")
        print(f"总计: {len(songs)}")
        print("="*60)

        if failed_songs:
            print("\n失败的歌曲:")
            for song in failed_songs:
                print(f"  - {song}")

if __name__ == "__main__":
    print("="*60)
    print("🎵 开始批量下载歌曲")
    print("="*60)
    print(f"下载目录: {download_dir}")
    print(f"待下载: {len(songs)} 首歌曲")
    print("="*60 + "\n")

    main()
