from yt_dlp import YoutubeDL
import os
import subprocess

# YouTubeから動画をダウンロード
def download_videos_from_file(file_path):
    # ファイルからURLを読み取る
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    # 改行文字を削除してURLをクリーニングする
    urls = [url.strip() for url in urls]

    # ダウンロードと変換のオプション設定
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        #'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'm4v',
        }],
    }

    # URLごとにダウンロード
    for url in urls:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

# カレントディレクトリ内のm4vファイルのプロファイルを変更
def change_profiles_in_directory():
    # カレントディレクトリ内のすべてのファイルを取得
    files = os.listdir()

    # m4vファイルのみを選択
    m4v_files = [file for file in files if file.endswith('.m4v')]

    # 各ファイルに対して処理を実行
    for input_file in m4v_files:
        output_file = input_file  # 出力ファイル名を入力ファイル名と同じに設定
        change_profile(input_file, output_file)

# m4vファイルのプロファイルを変更
def change_profile(input_file, output_file):
    # ffmpegコマンドを構築
    cmd = [
        'ffmpeg',
        '-i', input_file,  # 入力ファイル
        '-c:v', 'libx264',  # ビデオコーデックを指定
        '-profile:v', 'baseline',  # プロファイルをbaselineに設定
        '-c:a', 'copy',  # オーディオストリームをコピー
        output_file  # 出力ファイル
    ]

    # ffmpegを呼び出してプロセスを開始
    subprocess.run(cmd)

def main():
    # テキストファイルのパスを指定してダウンロードする
    file_path = 'urls.txt'
    download_videos_from_file(file_path)

    # m4vファイルのプロファイルを変更
    change_profiles_in_directory()

if __name__ == "__main__":
    main()
