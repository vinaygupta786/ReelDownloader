from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_video(video_url):
    ydl_opts = {
    'format': 'best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'nocheckcertificate': True,  # Skips SSL certificate checks
    'extractor_args': {
        'youtube': {
            'skip_dash_manifest': True,  # Avoids issues with DASH streams
        },
    },
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        file_name = ydl.prepare_filename(info_dict)
    
    return file_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    
    try:
        file_path = download_video(video_url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
