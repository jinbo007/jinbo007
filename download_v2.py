#!/usr/bin/env python3
"""
根据更新后的任务指引下载歌曲
流程：搜索 → 点击下载按钮 → 等待弹框 → 点击弹框下载 → 跳转播放页面 → 提取MP3链接 → 下载
"""
import os
import time
import re
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

# 排除关键词
exclude_keywords = ['DJ', 'dj', 'Dj', 'cover', 'Cover', 'COVER',
                    'remix', 'Remix', 'REMIX', '混音', '版',
                    'Live', 'live', 'LIVE']

# 优先级关键词
priority_keywords = ['原版', '官方']

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

def download_from_url(url, filename):
    """从URL下载文件"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.myfreemp3.com.cn/",
        }
        print(f"    开始下载...")
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()

        file_path = os.path.join(download_dir, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        file_size = os.path.getsize(file_path)
        if file_size < 1000:
            os.remove(file_path)
            print(f"    ✗ 文件太小 ({file_size} bytes)")
            return False

        print(f"    ✓ 下载完成 ({file_size/1024/1024:.1f} MB)")
        return True
    except Exception as e:
        print(f"    ✗ 下载失败: {e}")
        return False

def extract_mp3_link(driver):
    """从播放页面提取MP3链接"""
    print("  提取MP3链接...")

    # 方法1: 查找 audio 标签
    audio_elements = driver.find_elements(By.TAG_NAME, "audio")
    if audio_elements:
        audio_url = audio_elements[0].get_attribute("src")
        if audio_url and ('.mp3' in audio_url or '.m4a' in audio_url):
            print(f"    ✓ 找到 audio 标签")
            return audio_url

    # 方法2: 查找包含 .mp3 的链接
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and ('.mp3' in href or '.m4a' in href):
            # 排除页面导航链接
            if 'music.126.net' in href or 'music.qq.com' in href or 'music.163.com' in href:
                print(f"    ✓ 找到 MP3 链接")
                return href

    # 方法3: 查找所有可能的下载链接
    all_links = driver.find_elements(By.TAG_NAME, "a") + driver.find_elements(By.TAG_NAME, "link")
    for link in all_links:
        href = link.get_attribute("href")
        if href:
            # 查找常见音乐CDN链接
            if re.search(r'\.(mp3|m4a)(\?|$)', href, re.IGNORECASE):
                if 'http' in href and href.startswith('http'):
                    print(f"    ✓ 找到音乐链接")
                    return href

    return None

def main():
    """主函数"""
    print("="*60)
    print(f"开始下载: {song_name}")
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
        # 步骤1: 访问网站
        print("1. 访问网站...")
        driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
        time.sleep(3)

        # 步骤2: 搜索音乐
        print("2. 搜索音乐...")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input"))
        )

        search_box.clear()
        search_box.send_keys(song_name)
        time.sleep(1)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # 步骤3: 检查结果
        print("3. 检查搜索结果...")
        result_elements = []
        selectors = [
            ".list-item",
            "ul.music-list li",
            "li[data-id]",
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    result_elements = elements
                    print(f"   找到 {len(elements)} 个结果")
                    break
            except:
                continue

        if not result_elements:
            print("✗ 未找到搜索结果")
            return

        # 步骤4: 智能匹配最佳版本
        print("4. 智能匹配最佳版本...")
        best_result = None
        best_score = -1

        for i, elem in enumerate(result_elements[:15]):
            try:
                elem_text = elem.text
                if not elem_text or song_name not in elem_text:
                    continue

                # 排除非原版
                if is_excluded(elem_text):
                    continue

                # 计算分数
                score = 0

                # 包含优先级关键词
                if has_priority(elem_text):
                    score += 10

                # 完全匹配
                if elem_text == song_name:
                    score += 5

                # 包含歌曲名
                if song_name in elem_text:
                    score += 3

                # 较早的结果（通常更相关）
                score -= i

                if score > best_score:
                    best_score = score
                    best_result = elem
                    print(f"   候选 {i+1}: {elem_text[:50]} (分数: {score})")
            except:
                continue

        if not best_result:
            # 如果所有结果都被排除，使用第一个
            print("   使用第一个结果作为备选")
            best_result = result_elements[0]

        # 步骤5: 点击下载按钮
        print("5. 查找并点击下载按钮...")

        # 查找结果中的下载按钮
        try:
            # 查找结果中的下载图标或按钮
            download_btn = best_result.find_element(By.CSS_SELECTOR, ".download, [download], .TLH_download, button:contains('下载')")
            download_btn.click()
            print("   ✓ 已点击下载按钮")
        except:
            # 如果没有下载按钮，点击整个结果
            best_result.click()
            print("   ✓ 已点击结果")

        time.sleep(3)

        # 步骤6-7: 等待弹框，点击弹框中的下载
        print("6. 等待下载弹框...")

        # 查找可能的弹框
        try:
            # 等待模态框出现
            modal = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".modal, .modal-dialog, [role='dialog']"))
            )
            print("   找到弹框")

            # 查找弹框中的下载按钮
            modal_download_btn = modal.find_element(By.CSS_SELECTOR, "button:contains('下载'), .download, [data-download]")
            modal_download_btn.click()
            print("   ✓ 已点击弹框中的下载")
        except:
            print("   未找到弹框，继续...")

        time.sleep(3)

        # 步骤8: 等待跳转到播放页面
        print("8. 等待跳转到播放页面...")
        current_url = driver.current_url

        # 检查URL是否包含 audioPage
        timeout = 10
        start_time = time.time()
        while 'audioPage' not in current_url and (time.time() - start_time) < timeout:
            current_url = driver.current_url
            time.sleep(0.5)

        if 'audioPage' in current_url:
            print(f"   ✓ 已跳转到播放页面")
            print(f"   URL: {current_url}")
        else:
            print(f"   当前URL: {current_url}")

        time.sleep(3)

        # 步骤9: 获取下载链接
        print("9. 获取下载链接...")
        download_url = extract_mp3_link(driver)

        if download_url:
            print(f"   ✓ 下载链接: {download_url[:60]}...")

            # 步骤10: 下载音乐
            print("10. 下载音乐...")
            filename = f"{song_name}.mp3"

            if download_from_url(download_url, filename):
                print(f"\n✓ 下载成功!")
                print(f"保存位置: {download_dir}/{filename}")
                return

        print("\n✗ 未能自动提取下载链接")
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
