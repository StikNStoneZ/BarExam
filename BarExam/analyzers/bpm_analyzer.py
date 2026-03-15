import librosa
from analyzers.bpm_library import get_similar_tracks


def analyze_bpm(file_path):
    
    # load only a portion of the track to save memory
    y, sr = librosa.load(
    file_path,
    mono=True,
    offset=10,       # skip first 10 seconds
    duration=20,     # analyze next 20 seconds
    res_type="kaiser_fast"
    )

    # remove silence at beginning/end
    y, _ = librosa.effects.trim(y)

    # detect rhythmic energy
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # estimate tempo
    tempo = librosa.beat.tempo(
        onset_envelope=onset_env,
        sr=sr
    )

    bpm = round(float(tempo[0]))

    # fix half/double tempo issue common in rap
    if bpm < 80:
        bpm *= 2
    elif bpm > 180:
        bpm /= 2

    return round(bpm)


def analyze_beat(file_path):

    try:
        bpm = analyze_bpm(file_path)

        similar_tracks = get_similar_tracks(bpm)

        return {
            "bpm": bpm,
            "similar_tracks": similar_tracks
        }

    except Exception as e:

        print("Beat analysis failed:", e)

        return {
            "bpm": None,
            "similar_tracks": [],
            "error": "Beat analysis failed"
        }
