from flask import Flask, render_template, request, jsonify, Response
import subprocess
import tempfile
import os
import json
import uuid
import time

app = Flask(__name__)

# Custom temp dir for the app
APP_TEMP_DIR = os.path.join(tempfile.gettempdir(), "yt_web_app")
os.makedirs(APP_TEMP_DIR, exist_ok=True)

# --- Cleanup: delete all temp files on startup ---
def purge_app_temp_dir():
    for f in os.listdir(APP_TEMP_DIR):
        path = os.path.join(APP_TEMP_DIR, f)
        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f"[BOOT] Deleted leftover: {path}")
        except Exception as e:
            print(f"[ERROR] Failed to delete {path}: {e}")

# --- Cleanup: delete old .mp4 files (>30 min) ---
def clean_old_temp_files(threshold_minutes=30):
    now = time.time()
    for filename in os.listdir(APP_TEMP_DIR):
        if filename.endswith(".mp4"):
            path = os.path.join(APP_TEMP_DIR, filename)
            try:
                if os.path.isfile(path):
                    mtime = os.path.getmtime(path)
                    if now - mtime > threshold_minutes * 60:
                        os.remove(path)
                        print(f"[CLEANUP] Deleted old file: {path}")
            except Exception as e:
                print(f"[ERROR] Cleanup failed on {path}: {e}")

# --- Search YouTube videos using yt-dlp ---
def search_youtube(query, max_results=5):
    command = [
        'yt-dlp',
        f'ytsearch{max_results}:{query}',
        '--dump-json',
        '--default-search', 'ytsearch',
        '--flat-playlist',
        '--skip-download',
        '--quiet'
    ]
    try:
        output = subprocess.check_output(command).decode('utf-8')
        videos = [json.loads(line) for line in output.splitlines()]
        return [{"title": v["title"], "url": v["webpage_url"]} for v in videos if "webpage_url" in v]
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] yt-dlp search failed: {e}")
        return []

# --- Route: Home ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Route: Search ---
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])
    clean_old_temp_files()
    results = search_youtube(query)
    return jsonify(results)

# --- Route: Play ---
@app.route("/play")
def play():
    url = request.args.get("url")
    quality = request.args.get("quality", "best")
    if not url:
        return "Missing 'url' parameter", 400

    clean_old_temp_files()

    video_filename = f"{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(APP_TEMP_DIR, video_filename)

    command = [
        "yt-dlp",
        "-f", quality,
        "-o", output_path,
        "--merge-output-format", "mp4",
        "--quiet",
        url
    ]

    try:
        print(f"[INFO] Downloading video: {url} with quality: {quality}")
        subprocess.run(command, check=True)

        def generate():
            with open(output_path, 'rb') as f:
                yield from f
            os.remove(output_path)
            print(f"[CLEANUP] Deleted temp video after stream: {output_path}")

        return Response(generate(), mimetype='video/mp4')

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] yt-dlp download failed: {e}")
        return "Download failed", 500
    except Exception as e:
        print(f"[ERROR] Stream failed: {e}")
        return "Internal error", 500

# --- Run App ---
if __name__ == "__main__":
    purge_app_temp_dir()
    app.run(debug=True, host="0.0.0.0", port=5000)
