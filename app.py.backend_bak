from flask import Flask, render_template, request, jsonify, Response
import os
import json
import tempfile
import time
import subprocess
from urllib.parse import unquote

app = Flask(__name__)

# Load config from static/config.json
with open("static/config.json", encoding="utf-8") as f:
    app_config = json.load(f)

TEMP_DIR = tempfile.gettempdir()
TEMP_LIFETIME = 60 * 60  # 1 giờ

def clean_old_temp_files():
    now = time.time()
    for f in os.listdir(TEMP_DIR):
        path = os.path.join(TEMP_DIR, f)
        if os.path.isfile(path) and now - os.path.getmtime(path) > TEMP_LIFETIME:
            try:
                os.remove(path)
            except:
                pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    clean_old_temp_files()

    max_results = app_config.get("maxResults", 5)
    print(f"[DEBUG] Search query='{query}', max={max_results}")

    results = search_youtube(query, max_results)
    return jsonify(results)

def search_youtube(query, max_results):
    # Sử dụng yt-dlp JSON để tìm kiếm
    cmd = [
        "yt-dlp", f"ytsearch{max_results}:{query}",
        "--print", "%(title)s ||| %(webpage_url)s",
        "--no-playlist", "--no-warnings", "--skip-download"
    ]
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR] yt-dlp search failed: {e}")
        return []

    results = []
    for line in output.strip().split("\n"):
        if " ||| " in line:
            title, url = line.split(" ||| ", 1)
            results.append({"title": title.strip(), "url": url.strip()})
    return results

@app.route("/play")
def play():
    url = request.args.get("url")
    quality = request.args.get("quality", "best")

    if not url:
        return "❌ Missing URL", 400

    clean_old_temp_files()

    # Dùng yt-dlp để stream video trực tiếp
    cmd = [
        "yt-dlp", "-f", quality, "-o", "-", url
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return Response(proc.stdout, mimetype="video/mp4")
    except Exception as e:
        print(f"[ERROR] yt-dlp stream error: {e}")
        return "❌ Stream failed", 500

if __name__ == "__main__":
    app.run(host=app_config.get("listeningIP", "0.0.0.0"), port=app_config.get("port", 5000))
