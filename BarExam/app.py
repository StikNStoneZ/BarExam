from flask import Flask, render_template, request
from analyzers.bpm_analyzer import analyze_beat
from flask import Flask, render_template, request
import os

from analyzers.lyric_analyzer import analyze_lyrics

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
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
    beat_path = None

    # save beat if uploaded
    if beat and beat.filename != "":
        beat_path = os.path.join(app.config["UPLOAD_FOLDER"], beat.filename)
        beat.save(beat_path)
        beat_results = analyze_beat(beat_path)

    # analyze lyrics if text exists
    if lyrics.strip() != "":
        lyrics_results = analyze_lyrics(lyrics)

    return render_template(
        "index.html",
        result=lyrics_results,
        beat=beat_results
    )
if __name__ == "__main__":
    app.run(debug=True)