#!/usr/bin/env python3
"""
改进的下载脚本 - 点击下载按钮
"""
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# 下载目录
download_dir = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
os.makedirs(download_dir, exist_ok=True)

# 歌曲名
song_name = "你的身边不再是我"

def download_audio(url, filename):
    """下载音频文件"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.myfreemp3.com.cn/",
        }
        print(f"    开始下载: {url[:60]}...")
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()

        file_path = os.path.join(download_dir, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # 检查文件大小
        file_size = os.path.getsize(file_path)
        if file_size < 1000:
            print(f"    ✗ 文件太小: {file_size} bytes")
            os.remove(file_path)
            return False

        print(f"    ✓ 下载完成: {file_size/1024/1024:.1f} MB")
        return True
    except Exception as e:
        print(f"    ✗ 下载失败: {e}")
        return False

def find_and_click_download(driver):
    """查找并点击下载按钮"""
    print("  查找下载按钮...")

    # 尝试多种下载按钮选择器
    download_button_selectors = [
        "button[download]",
        "a[download]",
        ".download",
        ".TLH_download",
        "[data-download]",
        "button:contains('下载')",
        "a:contains('下载')",
    ]

    for selector in download_button_selectors[:6]:  # 只使用CSS选择器
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"    找到 {len(elements)} 个元素 (选择器: {selector})")
                for i, elem in enumerate(elements):
                    try:
                        text = elem.text
                        print(f"      按钮 {i+1}: '{text}'")
                    except:
                        pass
                # 点击第一个下载按钮
                elements[0].click()
                print(f"    ✓ 已点击下载按钮")
                time.sleep(3)
                return True
        except:
            continue

    return False

def find_download_link_from_page(driver):
    """从页面中查找下载链接"""
    print("  查找下载链接...")

    # 查找 audio 标签
    audio_elements = driver.find_elements(By.TAG_NAME, "audio")
    if audio_elements:
        audio_url = audio_elements[0].get_attribute("src")
        if audio_url:
            print(f"    ✓ 找到 audio 标签")
            return audio_url

    # 查找包含 mp3 的 a 标签
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and ('.mp3' in href or '.m4a' in href):
            print(f"    ✓ 找到 mp3 链接")
            return href

    # 查找所有 link 标签
    link_elements = driver.find_elements(By.TAG_NAME, "link")
    for link in link_elements:
        href = link.get_attribute("href")
        if href and ('.mp3' in href or '.m4a' in href):
            print(f"    ✓ 找到 link 标签")
            return href

    return None

def main():
    """主函数"""
    print("="*60)
    print(f"开始下载歌曲: {song_name}")
    print("="*60)

    # 初始化浏览器
    print("启动浏览器...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("打开网站...")
        driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
        time.sleep(3)

        print("查找搜索框...")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input"))
        )

        print(f"输入歌曲名: {song_name}")
        search_box.clear()
        search_box.send_keys(song_name)
        time.sleep(1)

        print("提交搜索...")
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        print("查找搜索结果...")
        # 尝试多种选择器查找结果
        result_elements = []
        selectors = [
            ".list-item",
            "li[data-id]",
            "li[data-song]",
            "ul.music-list li",
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    result_elements = elements
                    print(f"  找到 {len(elements)} 个结果 (选择器: {selector})")
                    break
            except:
                continue

        if not result_elements:
            print("✗ 未找到搜索结果")
            return

        # 查找包含歌曲名的结果
        song_element = None
        for i, elem in enumerate(result_elements[:10]):
            try:
                elem_text = elem.text
                if elem_text and song_name in elem_text and len(elem_text) < 200:
                    print(f"  找到匹配: {elem_text[:80]}")
                    song_element = elem
                    break
            except:
                continue

        if not song_element:
            print("使用第一个搜索结果")
            song_element = result_elements[0]

        print("点击搜索结果...")
        song_element.click()
        time.sleep(5)

        # 尝试多种下载方式

        # 方式1: 点击下载按钮
        if find_and_click_download(driver):
            print("  等待下载开始...")
            time.sleep(5)

        # 方式2: 从页面查找下载链接
        download_url = find_download_link_from_page(driver)
        if download_url:
            filename = f"{song_name}.mp3"
            if download_audio(download_url, filename):
                print(f"\n✓ 下载成功!")
                print(f"保存位置: {download_dir}/{filename}")
                return

        print("\n✗ 自动下载失败")
        print("\n手动下载步骤:")
        print("  1. 右键点击播放进度条")
        print("  2. 选择 '音频另存为'")
        print("  3. 保存到: /Users/jinbo/Documents/AIProject/clawbot/mp3/")

        # 等待用户手动操作
        print("\n浏览器将在 30 秒后关闭...")
        time.sleep(30)

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()
        print("\n浏览器已关闭")

if __name__ == "__main__":
    main()
