# ffmpeg-media-tools


步驟 1：下載 ffmpeg
前往官方網站下載

進入 ffmpeg 官網
點選 Windows → Windows builds from gyan.dev
下載 "ffmpeg-release-full.7z" 或 "ffmpeg-git-full.7z"
解壓縮 ffmpeg

使用 7-Zip 或內建解壓縮工具解壓 .7z 檔案
解壓後，會看到一個資料夾，例如：ffmpeg-6.0-full-build
進入該資料夾，裡面會有 bin、doc、presets 等資料夾

步驟 2：設定環境變數
找到 ffmpeg.exe

進入 ffmpeg-6.0-full-build\bin 資料夾
確保裡面有 ffmpeg.exe、ffplay.exe、ffprobe.exe
加入環境變數

按 Win + R，輸入 sysdm.cpl，按 Enter
進入 [進階] 分頁，點擊 [環境變數]
在 [系統變數] 中找到 Path，選擇它，然後點擊 [編輯]
點擊 [新增]，輸入 ffmpeg 的 bin 資料夾路徑，例如：
`C:\Users\你的帳號\Downloads\ffmpeg-6.0-full-build\bin`
點擊 [確定] → [確定]，關閉所有視窗
步驟 3：確認 ffmpeg 安裝成功
打開 cmd（按 Win + R，輸入 cmd，按 Enter）
輸入：
`ffmpeg -version`
如果顯示 ffmpeg version ...，表示安裝成功！🎉