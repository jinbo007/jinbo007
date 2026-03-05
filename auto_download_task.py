#!/usr/bin/env python3
"""
根据下载任务指引自动下载歌曲
使用 Selenium 从 myfreemp3.com.cn 下载
"""
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# 下载目录
download_dir = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
download_list_file = "/Users/jinbo/Documents/AIProject/clawbot/下载清单.txt"

# 排除关键词（DJ版、翻唱版等）
exclude_keywords = ['DJ', 'dj', 'Dj', 'cover', 'Cover', 'COVER',
                    'remix', 'Remix', 'REMIX', '混音', '版',
                    'Live', 'live', 'LIVE']

# 优先级关键词
priority_keywords = ['原版', '官方']

def load_download_list():
    """加载下载清单"""
    with open(download_list_file, 'r', encoding='utf-8') as f:
        songs = f.read().strip().split('\n')

    # 过滤空行和已下载的歌曲
    result = []
    for song in songs:
        song_clean = song.strip()
        if song_clean and not song_clean.startswith('[已下载]'):
            result.append(song_clean)
        elif song_clean.startswith('[已下载]'):
            # 提取原始歌曲名
            song_clean = song_clean.replace('[已下载]', '').strip()
            result.append(f"[已下载] {song_clean}")

    return result

def is_excluded(title):
    """检查是否应该排除"""
    title_lower = title.lower()
    for keyword in exclude_keywords:
        if keyword.lower() in title_lower:
            return True
    return False

def has_priority(title):
    """检查是否有优先级关键词"""
    for keyword in priority_keywords:
        if keyword in title:
            return True
    return False

def init_browser():
    """初始化浏览器"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def search_song(driver, song_name):
    """搜索歌曲"""
    try:
        print(f"  搜索: {song_name}")

        # 打开搜索页面
        driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
        time.sleep(2)

        # 查找搜索框
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input"))
        )

        # 清空并输入
        search_box.clear()
        search_box.send_keys(song_name)
        time.sleep(1)

        # 提交搜索
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # 查找搜索结果
        # 尝试多种选择器
        result_elements = []
        selectors = [
            "li[data-id]",
            "li[data-song]",
            "ul.music-list li",
            ".list-item",
            "li[onclick]",
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    result_elements = elements
                    print(f"    找到 {len(elements)} 个结果（选择器: {selector}）")
                    break
            except:
                continue

        if not result_elements:
            print(f"    ✗ 未找到搜索结果")
            return None

        # 筛选和排序结果
        best_result = None
        best_score = -1

        for i, elem in enumerate(result_elements[:10]):  # 只检查前10个
            try:
                title_text = elem.text

                if not title_text or song_name not in title_text:
                    continue

                # 检查是否应该排除
                if is_excluded(title_text):
                    continue

                # 计算优先级分数
                score = 0

                # 包含优先级关键词
                if has_priority(title_text):
                    score += 10

                # 完全匹配
                if title_text == song_name:
                    score += 5

                # 包含歌曲名（前部分匹配）
                if title_text.startswith(song_name):
                    score += 3

                # 较早的结果（通常更相关）
                score -= i

                if score > best_score:
                    best_score = score
                    best_result = elem
                    print(f"    候选 {i+1}: {title_text[:50]} (分数: {score})")

            except:
                continue

        if not best_result:
            # 如果所有结果都被排除，选择第一个
            try:
                best_result = result_elements[0]
                print(f"    使用第一个结果作为备选")
            except:
                pass

        if best_result:
            # 点击结果
            best_result.click()
            time.sleep(3)
            return True

        return None

    except Exception as e:
        print(f"    ✗ 搜索失败: {e}")
        return False

def download_song(driver, song_name):
    """下载歌曲"""
    try:
        print(f"  尝试下载...")

        # 方法1: 查找 audio 标签
        audio_elements = driver.find_elements(By.TAG_NAME, "audio")
        if audio_elements:
            audio_url = audio_elements[0].get_attribute("src")
            if audio_url and ('.mp3' in audio_url or '.m4a' in audio_url):
                print(f"    ✓ 找到音频链接")
                filename = f"{song_name}.mp3"
                file_path = os.path.join(download_dir, filename)

                # 使用 requests 下载
                import requests
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://www.myfreemp3.com.cn/",
                }

                response = requests.get(audio_url, headers=headers, stream=True, timeout=60)
                response.raise_for_status()

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                # 检查文件大小
                file_size = os.path.getsize(file_path)
                if file_size < 1000:
                    os.remove(file_path)
                    print(f"    ✗ 文件太小 ({file_size} bytes)")
                    return False

                print(f"    ✓ 下载成功 ({file_size/1024/1024:.1f} MB)")
                return True

        # 方法2: 右键下载
        try:
            # 查找播放器或进度条
            player_elements = driver.find_elements(By.CSS_SELECTOR, "audio, video, .progress, .play-bar")

            if player_elements:
                # 右键点击
                actions = ActionChains(driver)
                actions.context_click(player_elements[0]).perform()
                time.sleep(1)

                # 查找"音频另存为"选项
                save_as_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '音频另存为') or contains(text(), 'Save')]")
                if save_as_elements:
                    save_as_elements[0].click()
                    time.sleep(5)
                    print(f"    ✓ 已点击下载（右键方式）")
                    return True

        except Exception as e:
            print(f"    右键下载失败: {e}")

        print(f"    ✗ 未找到下载方式")
        return False

    except Exception as e:
        print(f"    ✗ 下载失败: {e}")
        return False

def main():
    """主函数"""
    # 加载下载清单
    songs = load_download_list()

    print("="*60)
    print("音乐下载任务")
    print("="*60)
    print(f"下载目录: {download_dir}")
    print(f"总歌曲数: {len(songs)}")

    # 统计
    pending = [s for s in songs if not s.startswith('[已下载]')]
    downloaded = [s for s in songs if s.startswith('[已下载]')]

    print(f"待下载: {len(pending)} 首")
    print(f"已下载: {len(downloaded)} 首")
    print("="*60 + "\n")

    if not pending:
        print("所有歌曲已下载完成！")
        return

    # 初始化浏览器
    print("启动浏览器...")
    driver = init_browser()

    success_count = 0
    skip_count = len(downloaded)
    fail_count = 0
    failed_songs = []

    try:
        for i, song in enumerate(songs, 1):
            # 跳过已下载的歌曲
            if song.startswith('[已下载]'):
                print(f"[{i}/{len(songs)}] ⊘ 跳过: {song}")
                continue

            print(f"\n[{i}/{len(songs)}] 处理: {song}")

            # 搜索歌曲
            if search_song(driver, song):
                # 下载歌曲
                if download_song(driver, song):
                    success_count += 1
                else:
                    fail_count += 1
                    failed_songs.append(song)
            else:
                fail_count += 1
                failed_songs.append(song)

            # 延迟，避免请求过快
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
        print("下载完成!")
        print("="*60)
        print(f"成功: {success_count}")
        print(f"跳过: {skip_count}")
        print(f"失败: {fail_count}")
        print(f"总计: {len(songs)}")
        print("="*60)

        if failed_songs:
            print("\n失败的歌曲:")
            for song in failed_songs:
                print(f"  - {song}")

if __name__ == "__main__":
    main()
