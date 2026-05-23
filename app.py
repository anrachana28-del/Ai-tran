import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# -------------------------
# CONFIG (SECURE)
# -------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔐 API KEY from Environment Variable (NOT hardcoded)
API_KEY = os.getenv("OPENAI_API_KEY")

# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return render_template("index.html", text="🎬 Upload video to get AI transcript")

# -------------------------
# UPLOAD + SPEECH TO TEXT
# -------------------------
@app.route("/upload", methods=["POST"])
def upload():

    # check file
    if "video" not in request.files:
        return render_template("index.html", text="❌ No file uploaded")

    file = request.files["video"]

    if file.filename == "":
        return render_template("index.html", text="❌ No file selected")

    # save file
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    # -------------------------
    # check API KEY
    # -------------------------
    if not API_KEY:
        return render_template("index.html", text="❌ API KEY missing (set OPENAI_API_KEY in Render)")

    # -------------------------
    # CALL OpenAI Speech-to-Text API
    # -------------------------
    url = "https://api.openai.com/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        files = {
            "file": open(path, "rb"),
            "model": (None, "whisper-1")
        }

        response = requests.post(url, headers=headers, files=files)

        if response.status_code != 200:
            return render_template("index.html", text=f"❌ API Error: {response.text}")

        data = response.json()
        text = data.get("text", "No transcript found")

        return render_template("index.html", text=text)

    except Exception as e:
        return render_template("index.html", text=f"❌ Server Error: {str(e)}")

# -------------------------
# RUN (Render compatible)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
