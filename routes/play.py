from flask import Blueprint, Response, request
import subprocess
import tempfile
import time
import os

play_route = Blueprint("play", __name__)

@play_route.route("/play")
def play():
    url = request.args.get("url")
    quality = request.args.get("quality", "best")

    if not url:
        return "❌ Missing URL", 400

    clean_old_temp_files()

    try:
        proc = subprocess.Popen(
            ["yt-dlp", "-f", quality, "-o", "-", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        return Response(proc.stdout, mimetype="video/mp4")
    except Exception as e:
        print(f"[ERROR] yt-dlp stream error: {e}")
        return "❌ Stream failed", 500

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
