import os
from flask import Flask, render_template, request, redirect, url_for
import whisper

# --------------------
# App Setup
# --------------------
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --------------------
# Load Whisper Model
# (use tiny for Render free)
# --------------------
model = whisper.load_model("tiny")

# --------------------
# Home Page
# --------------------
@app.route("/")
def index():
    return render_template("index.html", text="Upload video to start")

# --------------------
# Upload + Process Video
# --------------------
@app.route("/upload", methods=["POST"])
def upload():

    if "video" not in request.files:
        return "No file uploaded"

    file = request.files["video"]

    if file.filename == "":
        return "No selected file"

    # Save file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    try:
        # --------------------
        # Speech to Text (Whisper)
        # --------------------
        result = model.transcribe(file_path)

        text = result["text"]

        return render_template("index.html", text=text)

    except Exception as e:
        return f"Error processing video: {str(e)}"

# --------------------
# Run Server (Render Compatible)
# --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
