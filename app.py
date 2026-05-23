import os
from flask import Flask, render_template, request

app = Flask(__name__)

# --------------------
# Folder setup
# --------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --------------------
# Load Whisper safely (avoid crash on Render)
# --------------------
model = None

def load_model():
    global model
    try:
        import whisper
        model = whisper.load_model("tiny")  # safe for free server
        print("Whisper loaded")
    except Exception as e:
        print("Whisper not loaded:", e)

load_model()

# --------------------
# Home
# --------------------
@app.route("/")
def home():
    return render_template("index.html", text="Upload video to start")

# --------------------
# Upload video
# --------------------
@app.route("/upload", methods=["POST"])
def upload():

    if "video" not in request.files:
        return "No file found"

    file = request.files["video"]

    if file.filename == "":
        return "No file selected"

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    # --------------------
    # If Whisper not available
    # --------------------
    if model is None:
        return render_template("index.html",
            text="❌ Whisper not available on server (check install)")

    try:
        # --------------------
        # Speech to text
        # --------------------
        result = model.transcribe(path)
        text = result["text"]

        return render_template("index.html", text=text)

    except Exception as e:
        return render_template("index.html", text=f"Error: {str(e)}")

# --------------------
# Run server (IMPORTANT for Render)
# --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
