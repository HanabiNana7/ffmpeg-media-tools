import os
import glob
import subprocess


def process_single_mkv(
    file,
    folder_path,
    output_folder_path,
    specified_audio=None,
):
    """處理單一 MKV 檔案，移除內嵌字幕並合併外部字幕"""
    base_name = os.path.splitext(os.path.basename(file))[0]
    output_path = os.path.join(output_folder_path, os.path.basename(file))

    # 搜尋對應的字幕檔案（優先 srt，其次 ass）
    sup_path = os.path.join(folder_path, f"{base_name}.sup")
    ass_path = os.path.join(folder_path, f"{base_name}.ass")
    srt_path = os.path.join(folder_path, f"{base_name}.srt")

    sub_path = (
        sup_path
        if os.path.exists(sup_path)
        else (
            ass_path
            if os.path.exists(ass_path)
            else srt_path if os.path.exists(srt_path) else None
        )
    )

    # FFmpeg 指令 僅保留視訊
    cmd = [
        "ffmpeg",
        "-i",
        file,
        "-map",
        "0:v:0",  # 視訊流
        "-map",
        "0:t?",  # 章節流（如果有）
        "-map",
        "0:d?",  # 附加資料流（如有封面圖）
        "-c:v",
        "copy",  # 視訊流複製，不轉碼
        "-c:t",
        "copy",  # 保留章節資訊
        "-c:d",
        "copy",  # 保留附加資料（如封面圖）
    ]

    # 字幕處理，若無 sup ass srt 則移除所有字幕
    if sub_path:
        subtitle_codec = (
            "dvdsub"
            if sub_path.endswith(".sup")
            else "ass" if sub_path.endswith(".ass") else "mov_text"
        )
        print(f"subtitle_codec={subtitle_codec}")
        cmd = [
            "ffmpeg",
            "-i",
            file,
            "-i",
            sub_path,  # 輸入字幕
            "-map",
            "0:v:0",  # 視訊流
            "-map",
            "0:t?",  # 章節流（如果有）
            "-map",
            "0:d?",  # 附加資料流（如有封面圖）
            "-map",
            "1:s",  # 指定字幕流
            "-c:v",
            "copy",  # 視訊流複製，不轉碼
            "-c:t",
            "copy",  # 保留章節資訊
            "-c:d",
            "copy",  # 保留附加資料（如封面圖）
            "-c:s",
            subtitle_codec,
            "-metadata:s:s:0",
            "title=繁體中文 (台灣)",  # 設定字幕名稱
            "-metadata:s:s:0",
            "language=chi",  # 設定字幕語言（chi = 繁體中文）
        ]
    else:
        print("無 sup ass srt 字幕，移除所有字幕")

    # 音訊處理，若無指定則保留全部音訊
    if specified_audio:
        ## 取得所有音訊軌道語言資訊
        cmd_probe = [
            "ffprobe",
            "-i",
            file,
            "-show_streams",
            "-select_streams",
            "a",
            "-loglevel",
            "error",
        ]
        audio_result = subprocess.run(
            cmd_probe, capture_output=True, text=True, encoding="utf-8"
        )
        streams = audio_result.stdout.split("\n")

        audio_tracks = []
        index = None
        for line in streams:
            if "index=" in line:
                index = int(line.split("=")[1].strip()) - 1
            if "TAG:language=" in line and index is not None:
                lang = line.split("=")[1].strip()
                if lang == specified_audio:
                    audio_tracks.append(f"0:a:{index}")
                index = None

        if not audio_tracks:
            print(f"{file}，沒有指定音訊 {specified_audio}，保留全部音訊")
            cmd.extend(["-map", "0:a", "-c:a", "copy"])
        else:
            for track in audio_tracks:
                cmd.extend(["-map", track, "-c:a", "copy"])
    else:
        print(f"{file}，沒有指定音訊，保留全部音訊")
        cmd.extend(["-map", "0:a", "-c:a", "copy"])

    # 執行 ffmpeg 並捕捉錯誤輸出
    cmd.append(output_path)
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    if result.returncode == 0:

        print(f"✅ 處理完成: {file} → {output_path}")
    else:

        print(f"❌ 處理失敗: {file}\n錯誤訊息: {result.stderr}")


def process_media(folder_path, specified_audio=None, max_threads=5):
    output_folder_path = folder_path + "_output"
    os.makedirs(output_folder_path, exist_ok=True)
    mkv_files_list = glob.glob(os.path.join(folder_path, "*.mkv"))

    for mkv_file in mkv_files_list:
        process_single_mkv(
            file=mkv_file,
            folder_path=folder_path,
            output_folder_path=output_folder_path,
            specified_audio=specified_audio,
        )
