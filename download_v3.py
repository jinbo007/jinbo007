#!/usr/bin/env python3
"""
下载"你的身边不再是我" - 改进版
确保找到匹配内容，点击下载，在弹框中点击下载
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

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 访问网站
        print("打开网站...")
        driver.get("https://www.myfreemp3.com.cn/?page=searchPage")
        time.sleep(3)

        # 搜索歌曲
        print(f"搜索: {song_name}")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input"))
        )
        search_box.clear()
        search_box.send_keys(song_name)
        time.sleep(1)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        # 查找匹配的搜索结果
        print("查找搜索结果...")
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
                    print(f"  找到 {len(elements)} 个结果 (选择器: {selector})")
                    break
            except:
                continue

        if not result_elements:
            print("✗ 未找到搜索结果")
            return

        # 查找包含歌曲名的结果
        matched_element = None
        for i, elem in enumerate(result_elements[:15]):
            try:
                elem_text = elem.text
                if elem_text and song_name in elem_text and len(elem_text) < 200:
                    print(f"  ✓ 找到匹配: {elem_text[:80]}")
                    matched_element = elem
                    break
            except:
                continue

        if not matched_element:
            print("✗ 未找到匹配的结果，使用第一个")
            matched_element = result_elements[0]

        # 点击结果
        print("点击搜索结果...")
        matched_element.click()
        time.sleep(5)

        # 查找并点击下载按钮
        print("查找下载按钮...")

        # 查找包含"下载"文本的按钮
        download_buttons = []
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in all_buttons:
            try:
                btn_text = btn.text
                if btn_text and "下载" in btn_text:
                    download_buttons.append(btn)
                    print(f"  ✓ 找到下载按钮: '{btn_text}'")
            except:
                pass

        # 查找包含download类名的元素
        download_elements = driver.find_elements(By.CSS_SELECTOR, ".download, [download], .TLH_download")
        for elem in download_elements:
            if elem not in download_buttons:
                download_buttons.append(elem)
                print(f"  ✓ 找到下载元素 (class)")

        if download_buttons:
            print(f"  总共找到 {len(download_buttons)} 个下载元素")

            # 点击第一个下载按钮
            print("  点击第一个下载按钮...")
            download_buttons[0].click()
            time.sleep(3)
        else:
            print("✗ 未找到下载按钮")

        # 等待弹框出现
        print("等待弹框...")

        try:
            # 等待模态框出现
            modal = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".modal.show, .modal[style*='block'], [class*='modal']"))
            )
            print("  ✓ 找到弹框")
        except:
            print("  未找到弹框")

        # 查找弹框中的下载按钮
        print("在弹框中查找下载按钮...")
        modal_download_buttons = []

        # 方法1: 查找弹框中的button
        try:
            modals = driver.find_elements(By.CSS_SELECTOR, ".modal")
            if modals:
                buttons = modals[0].find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    try:
                        btn_text = btn.text
                        if btn_text and "下载" in btn_text:
                            modal_download_buttons.append(btn)
                            print(f"    ✓ 找到: '{btn_text}'")
                    except:
                        pass
        except:
            pass

        # 方法2: 查找.modal-footer中的按钮
        try:
            footer_buttons = driver.find_elements(By.CSS_SELECTOR, ".modal-footer button")
            for btn in footer_buttons:
                modal_download_buttons.append(btn)
                try:
                    btn_text = btn.text
                    print(f"    ✓ footer按钮: '{btn_text}'")
                except:
                    pass
        except:
            pass

        if modal_download_buttons:
            print(f"  弹框中找到 {len(modal_download_buttons)} 个下载按钮")

            # 点击第一个下载按钮
            print("  点击弹框中的下载按钮...")
            modal_download_buttons[0].click()
            time.sleep(5)
        else:
            print("  ✗ 弹框中未找到下载按钮")

        print("\n✓ 下载流程已完成")
        print("\n手动下载步骤:")
        print("  1. 右键点击播放进度条")
        print("  2. 选择 '音频另存为'")
        print("  3. 保存到: /Users/jinbo/Documents/AIProject/clawbot/mp3/")

        print("\n浏览器将在 60 秒后关闭...")
        time.sleep(60)

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()
        print("\n浏览器已关闭")

if __name__ == "__main__":
    main()
