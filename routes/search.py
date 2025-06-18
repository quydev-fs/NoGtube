from flask import Blueprint, request, jsonify
from yt_dlp import YoutubeDL
import tempfile
import time
import json
import os
import subprocess
CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "static", "config.json")
)

with open(CONFIG_PATH,"r") as f:
    app_config = json.load(f)

search_route = Blueprint("search", __name__)

@search_route.route("/search")
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
