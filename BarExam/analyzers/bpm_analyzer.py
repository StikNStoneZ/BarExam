import aubio
import numpy as np


# -----------------------------
# RAP BPM LIBRARY
# -----------------------------

rap_bpm_library = [

("Lose Yourself", "Eminem", 86),
("HUMBLE.", "Kendrick Lamar", 150),
("N.Y. State of Mind", "Nas", 94),
("No Role Modelz", "J. Cole", 100),
("Alright", "Kendrick Lamar", 110),
("Still D.R.E.", "Dr. Dre", 93),
("C.R.E.A.M.", "Wu-Tang Clan", 90),
("Juicy", "Notorious B.I.G.", 96),
("Shook Ones Pt. II", "Mobb Deep", 94),
("Power", "Kanye West", 154),

("God's Plan", "Drake", 77),
("Sicko Mode", "Travis Scott", 78),
("Mask Off", "Future", 150),
("Bad and Boujee", "Migos", 127),
("XO Tour Llif3", "Lil Uzi Vert", 155),
("Goosebumps", "Travis Scott", 130),
("DNA.", "Kendrick Lamar", 140),
("Money Trees", "Kendrick Lamar", 72),
("Middle Child", "J. Cole", 84),
("Rap God", "Eminem", 148),

]


# -----------------------------
# BPM DETECTION
# -----------------------------

def analyze_bpm(file_path):

    win_s = 1024
    hop_s = 512

    samplerate = 44100

    source = aubio.source(file_path, samplerate, hop_s)
    samplerate = source.samplerate

    tempo_detector = aubio.tempo("default", win_s, hop_s, samplerate)

    beats = []

    while True:

        samples, read = source()

        if tempo_detector(samples):
            beats.append(tempo_detector.get_last_s())

        if read < hop_s:
            break

    if len(beats) > 1:

        intervals = np.diff(beats)

        bpm = 60 / np.median(intervals)

        # normalize half/double tempo
        if bpm < 70:
            bpm *= 2
        if bpm > 180:
            bpm /= 2

        return round(bpm, 2)

    return None


# -----------------------------
# FIND SIMILAR SONGS
# -----------------------------

def get_similar_tracks(bpm, tolerance=5):

    matches = []

    for title, artist, song_bpm in rap_bpm_library:

        if abs(song_bpm - bpm) <= tolerance:
            matches.append(f"{artist} — {title}")

    return matches[:5]


# -----------------------------
# MAIN BEAT ANALYZER
# -----------------------------

def analyze_beat(file_path):

    try:

        bpm = analyze_bpm(file_path)

        if bpm is None:
            return {"error": "Could not detect BPM"}

        similar_tracks = get_similar_tracks(bpm)

        return {
            "bpm": bpm,
            "similar_tracks": similar_tracks
        }

    except Exception as e:

        print("Beat analysis error:", e)

        return {"error": "Beat analysis failed"}
