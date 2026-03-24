from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os
import uuid

app = Flask(__name__)
FOLDER = 'downloads'

if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        unique_id = str(uuid.uuid4())
        output_template = f"{FOLDER}/{unique_id}.%(ext)s"

        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,

        'ffmpeg_location': './ffmpeg/bin',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

        try:

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)

            filename = f"{unique_id}.mp3"
            return send_from_directory(FOLDER, filename, as_attachment=True)
        
        except Exception as e:
            return f"Error: {str(e)}"
        
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)