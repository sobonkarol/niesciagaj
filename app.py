from flask import Flask, render_template, request, send_file
import os
import yt_dlp

app = Flask(__name__)

# Ścieżka, w której będą tymczasowo przechowywane pobrane filmy
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download_video():
    tweet_url = request.form['tweet_url']
    custom_file_name = request.form['file_name']

    # Ustal domyślną nazwę pliku, jeśli użytkownik nie podał nazwy
    if not custom_file_name:
        custom_file_name = "your_video_from_x"

    try:
        # Konfiguracja yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{custom_file_name}.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(tweet_url, download=True)
            video_file = ydl.prepare_filename(info_dict)

        # Zwrócenie pliku do użytkownika
        return send_file(video_file, as_attachment=True)

    except Exception as e:
        return f"Błąd pobierania: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
