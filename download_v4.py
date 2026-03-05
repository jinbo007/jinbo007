#!/usr/bin/env python3
"""
下载"你的身边不再是我" - 健壮版
增加错误处理和等待时间
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# 下载目录
download_dir = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
os.makedirs(download_dir, exist_ok=True)

# 歌曲名
song_name = "你的身边不再是我"

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
    # 增加页面加载超时
    chrome_options.add_argument("--page-load-timeout=30000")
    chrome_options.add_argument("--load-timeout=30000")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 访问网站
        print("打开网站...")
        driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
        time.sleep(5)  # 增加等待时间

        # 搜索歌曲
        print(f"搜索: {song_name}")
        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "input"))
        )

        search_box.clear()
        search_box.send_keys(song_name)
        time.sleep(1)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)  # 增加等待时间

        # 查找搜索结果
        print("查找搜索结果...")
        result_elements = []

        # 等待页面完全加载
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, ".list-item, ul.music-list li, li[data-id]")) > 0
        )

        selectors = [
            ".list-item",
            "ul.music-list li",
            "li[data-id]",
            "li[onclick]",
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    result_elements = elements
                    print(f"  找到 {len(elements)} 个结果 (选择器: {selector})")
                    # 打印前几个结果的文本
                    for i, elem in enumerate(elements[:5]):
                        try:
                            text = elem.text
                            if text and len(text) < 100:
                                print(f"    结果 {i+1}: {text[:70]}")
                        except:
                            pass
                    break
            except:
                continue

        if not result_elements:
            print("✗ 未找到搜索结果")
            return

        # 查找包含歌曲名的结果
        matched_element = None
        for elem in result_elements[:10]:
            try:
                elem_text = elem.text
                if elem_text and song_name in elem_text and len(elem_text) < 200:
                    print(f"  ✓ 找到匹配: {elem_text[:70]}")
                    matched_element = elem
                    break
            except:
                pass

        if not matched_element:
            print("使用第一个搜索结果")
            matched_element = result_elements[0]

        # 点击搜索结果
        print("点击搜索结果...")
        matched_element.click()
        time.sleep(8)  # 增加等待时间

        # 打印当前URL
        current_url = driver.current_url
        print(f"当前URL: {current_url}")

        # 查找下载按钮
        print("查找下载按钮...")

        # 等待下载按钮出现
        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".TLH_download, .download, button[download], [data-download]"))
            )
            print("  ✓ 找到下载按钮")
            download_button.click()
            print("  ✓ 已点击下载按钮")
            time.sleep(5)
        except:
            print("  未找到下载按钮，继续...")

        # 等待弹框
        print("等待弹框...")
        try:
            modal = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".modal.show, .modal[style*='block']"))
            )
            print("  ✓ 找到弹框")

            # 在弹框中查找下载按钮
            try:
                modal_download_btn = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".modal button, .modal-footer button"))
                )
                print("  ✓ 找到弹框下载按钮")
                modal_download_btn.click()
                print("  ✓ 已点击弹框下载按钮")
                time.sleep(5)
            except:
                print("  未找到弹框下载按钮")
        except:
            print("  未找到弹框")

        # 等待跳转到播放页面
        print("等待跳转到播放页面...")
        start_time = time.time()
        timeout = 15
        while 'audioPage' not in current_url and (time.time() - start_time) < timeout:
            current_url = driver.current_url
            time.sleep(1)

        current_url = driver.current_url
        if 'audioPage' in current_url:
            print(f"  ✓ 已跳转到播放页面")
            print(f"  URL: {current_url}")
        else:
            print(f"  当前URL: {current_url}")

        time.sleep(5)

        # 查找下载链接
        print("查找下载链接...")

        # 查找audio标签
        audio_elements = driver.find_elements(By.TAG_NAME, "audio")
        if audio_elements:
            audio_url = audio_elements[0].get_attribute("src")
            if audio_url:
                print(f"  ✓ 找到audio标签: {audio_url[:60]}...")

                # 尝试下载
                filename = f"{song_name}.mp3"
                file_path = os.path.join(download_dir, filename)

                print(f"  下载中...")
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

                file_size = os.path.getsize(file_path)
                if file_size < 1000:
                    os.remove(file_path)
                    print(f"  ✗ 文件太小 ({file_size} bytes)")
                else:
                    print(f"  ✓ 下载成功 ({file_size/1024/1024:.1f} MB)")
                    print(f"\n✓ 下载完成!")
                    print(f"保存位置: {file_path}")
                    return

        # 查找其他下载链接
        print("查找其他下载链接...")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links[:20]:
            href = link.get_attribute("href")
            if href and ('.mp3' in href or '.m4a' in href):
                if 'music.126.net' in href or 'music.qq.com' in href or 'music.163.com' in href:
                    print(f"  ✓ 找到下载链接: {href[:60]}...")

                    # 尝试下载
                    filename = f"{song_name}.mp3"
                    file_path = os.path.join(download_dir, filename)

                    print(f"  下载中...")
                    import requests
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Referer": "https://www.myfreemp3.com.cn/",
                    }

                    response = requests.get(href, headers=headers, stream=True, timeout=60)
                    response.raise_for_status()

                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                    file_size = os.path.getsize(file_path)
                    if file_size < 1000:
                        os.remove(file_path)
                        print(f"  ✗ 文件太小 ({file_size} bytes)")
                    else:
                        print(f"  ✓ 下载成功 ({file_size/1024/1024:.1f} MB)")
                        print(f"\n✓ 下载完成!")
                        print(f"保存位置: {file_path}")
                        return

        print("\n✗ 自动下载失败")
        print("\n手动下载步骤:")
        print("  1. 右键点击播放进度条")
        print("  2. 选择 '音频另存为'")
        print("  3. 保存到: /Users/jinbo/Documents/AIProject/clawbot/mp3")

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
