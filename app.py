import os
from flask import Flask, render_template, request

app = Flask(__name__)

# --------------------
# Setup upload folder
# --------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --------------------
# Home page
# --------------------
@app.route("/")
def home():
    return render_template("index.html", text="🎬 Ready to upload video")

# --------------------
# Upload handler
# --------------------
@app.route("/upload", methods=["POST"])
def upload():

    if "video" not in request.files:
        return render_template("index.html", text="❌ No file uploaded")

    file = request.files["video"]

    if file.filename == "":
        return render_template("index.html", text="❌ No file selected")

    # Save file
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    # --------------------
    # SAFE OUTPUT (no Whisper to avoid Render crash)
    # --------------------
    text = f"""✅ Upload Success!

📁 File: {file.filename}
📍 Saved: {path}

⚠️ AI (Whisper) not enabled yet on Render
"""

    return render_template("index.html", text=text)

# --------------------
# Run server (Render required)
# --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
