import os
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ❌ REMOVE Whisper (causes memory crash on Render)

@app.route("/")
def home():
    return render_template("index.html", text="Ready to upload video")

@app.route("/upload", methods=["POST"])
def upload():

    if "video" not in request.files:
        return "No file uploaded"

    file = request.files["video"]

    if file.filename == "":
        return "No file selected"

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    # ✅ Safe response (no AI processing for now)
    return render_template(
        "index.html",
        text=f"✅ Video uploaded successfully!\nFile: {file.filename}"
    )

# IMPORTANT for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
