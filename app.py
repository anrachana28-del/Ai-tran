import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔑 Put your API key here (OpenAI)
API_KEY = "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"

# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return render_template("index.html", text="🎬 Upload video to get real AI text")

# -------------------------
# UPLOAD + SPEECH TO TEXT
# -------------------------
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["video"]
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    # -------------------------
    # 🔥 CALL WHISPER API
    # -------------------------
    url = "https://api.openai.com/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    files = {
        "file": open(path, "rb"),
        "model": (None, "whisper-1")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return render_template("index.html", text=f"❌ API Error: {response.text}")

    data = response.json()
    text = data.get("text", "")

    return render_template("index.html", text=text)

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
