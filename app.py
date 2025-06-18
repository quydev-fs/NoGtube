from flask import Flask, render_template
from routes import endpoints
import json

with open("static/config.json" , "r") as f:
    app_config = json.load(f)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

for bp in endpoints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(host=app_config.get("listeningIP", "0.0.0.0"), port=app_config.get("port", 5000))
