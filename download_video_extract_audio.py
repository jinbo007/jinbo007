#!/usr/bin/env python3
import subprocess
import os

download_dir = "/Users/jinbo/Documents/AIProject/clawbot/mp3"
ytdlp_path = "/Users/jinbo/Library/Python/3.11/bin/yt-dlp"

song_name = "错错错"
search_query = f"ytsearch1:{song_name} 歌曲"

# 先尝试下载视频再提取音频
cmd = [
    ytdlp_path,
    search_query,
    "-f", "bestvideo+bestaudio/best",
    "--merge-output-format", "mp4",
    "-o", os.path.join(download_dir, f"{song_name}.%(ext)s"),
    "--no-playlist",
    "--cookies-from-browser", "chrome",
    "--js-runtimes", "node",
    "-v"
]

print("尝试下载完整视频...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✓ 视频下载成功！")
    # 提取音频
    print("\n提取音频中...")
    video_file = os.path.join(download_dir, f"{song_name}.mp4")
    audio_file = os.path.join(download_dir, f"{song_name}.mp3")

    extract_cmd = [
        "ffmpeg",
        "-i", video_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-y",  # 覆盖已存在的文件
        audio_file
    ]

    result2 = subprocess.run(extract_cmd, capture_output=True, text=True)

    if result2.returncode == 0:
        print("✓ 音频提取成功！")
        # 删除视频文件
        os.remove(video_file)
        print(f"已下载: {song_name}.mp3")
    else:
        print("✗ 音频提取失败")
        print(result2.stderr[-500:])
else:
    print("\n✗ 视频下载失败")
    print("\n标准错误 (最后1000字符):")
    print(result.stderr[-1000:])
