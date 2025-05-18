import os

from src.mkv_processor import process_media


# MKV 檔修正
def main():
    folder_path = os.path.join("..", "media_data", "Season 01")
    process_media(
        folder_path=folder_path,
        specified_sub=None,
        specified_audio="jpn",
        max_threads=os.cpu_count(),
    )


if __name__ == "__main__":
    main()
