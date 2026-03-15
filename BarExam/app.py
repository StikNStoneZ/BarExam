from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from analyzers.bpm_analyzer import analyze_beat
from analyzers.lyric_analyzer import analyze_lyrics

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    beat = request.files["beat"]
    lyrics = request.form["lyrics"]

    beat_results = None
    lyrics_results = None

    if beat and beat.filename != "":
        filename = secure_filename(beat.filename)
        beat_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        beat.save(beat_path)
        beat_results = analyze_beat(beat_path)

    if lyrics.strip() != "":
        lyrics_results = analyze_lyrics(lyrics)

    return render_template(
        "index.html",
        result=lyrics_results,
        beat=beat_results
    )


if __name__ == "__main__":
    app.run(debug=True)
