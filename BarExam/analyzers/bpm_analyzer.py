import librosa
import numpy as np


# --------------------------------
# RAP BPM LIBRARY
# --------------------------------

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

("All Caps", "MF DOOM", 91),
("Figaro", "MF DOOM", 96),
("Accordion", "MF DOOM", 90),
("Ms. Jackson", "OutKast", 94),
("ATLiens", "OutKast", 97),
("Dead Presidents II", "Jay-Z", 88),
("Big Pimpin", "Jay-Z", 89),
("Hate It Or Love It", "The Game", 94),
("In Da Club", "50 Cent", 90),
("Many Men", "50 Cent", 95),

("X Gon Give It To Ya", "DMX", 95),
("Hypnotize", "Notorious B.I.G.", 94),
("The Real Slim Shady", "Eminem", 104),
("Stan", "Eminem", 80),
("Without Me", "Eminem", 112),
("Stronger", "Kanye West", 104),
("Flashing Lights", "Kanye West", 90),
("Otis", "Jay-Z & Kanye West", 94),
("Empire State of Mind", "Jay-Z", 87),
("A Milli", "Lil Wayne", 76)

]


# --------------------------------
# BPM DETECTION
# --------------------------------

def analyze_bpm(file_path):

    y, sr = librosa.load(file_path, mono=True, duration=30, res_type="kaiser_fast")

    # remove silence
    y, _ = librosa.effects.trim(y)

    # separate drums from melody
    y_harm, y_perc = librosa.effects.hpss(y)

    # detect rhythmic energy
    onset_env = librosa.onset.onset_strength(y=y_perc, sr=sr)

    # estimate tempo candidates
    tempos = librosa.beat.tempo(
        onset_envelope=onset_env,
        sr=sr,
        aggregate=None
    )

    bpm = float(np.median(tempos))

    # normalize hip-hop ranges
    if bpm < 70:
        bpm *= 2

    if bpm > 160:
        bpm /= 2

    return round(bpm, 2)


# --------------------------------
# FIND SIMILAR SONGS
# --------------------------------

def get_similar_tracks(bpm, tolerance=5):

    matches = []

    for title, artist, song_bpm in rap_bpm_library:

        if abs(song_bpm - bpm) <= tolerance:
            matches.append(f"{artist} — {title}")

    return matches[:5]


# --------------------------------
# MAIN BEAT ANALYZER
# --------------------------------

def analyze_beat(file_path):

    bpm = analyze_bpm(file_path)

    similar_tracks = get_similar_tracks(bpm)

    return {
        "bpm": bpm,
        "similar_tracks": similar_tracks
    }
