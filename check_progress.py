#!/usr/bin/env python3
"""
下载进度追踪器
"""
import os

download_dir = "/Users/jinbo/Documents/AIProject/clawbot/mp3"

def get_downloaded_files():
    """获取已下载的文件列表"""
    files = []
    for f in os.listdir(download_dir):
        if f.endswith('.mp3'):
            file_path = os.path.join(download_dir, f)
            size = os.path.getsize(file_path)
            size_mb = size / (1024 * 1024)
            files.append((f, size_mb))
    return sorted(files, key=lambda x: x[1], reverse=True)

def format_size(size_mb):
    """格式化文件大小"""
    if size_mb < 1:
        return f"{size_mb*1024:.1f} KB"
    return f"{size_mb:.1f} MB"

def main():
    print("="*60)
    print("📊 下载进度报告")
    print("="*60)

    files = get_downloaded_files()
    total = len(files)
    target = 81
    percent = (total / target) * 100

    print(f"\n总进度: {total}/{target} ({percent:.1f}%)")
    print(f"已完成: {total} 首歌曲")
    print(f"待下载: {target - total} 首歌曲")
    print(f"总大小: {sum([f[1] for f in files]):.1f} MB")

    print(f"\n{'='*60}")
    print("已下载歌曲列表（按大小排序）:")
    print(f"{'='*60}")

    for i, (filename, size) in enumerate(files, 1):
        print(f"{i:2d}. {filename:<60} {format_size(size):>8}")

    print(f"\n{'='*60}")
    print(f"下载位置: {download_dir}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
