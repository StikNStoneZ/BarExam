import librosa
import numpy as np
from analyzers.bpm_library import rap_bpm_library


def analyze_bpm(file_path):

    # analyze multiple small sections for stability
    segments = [10, 25, 40]
    tempos = []

    for offset in segments:
        try:

            # very lightweight audio loading
            y, sr = librosa.load(
                file_path,
                mono=True,
                offset=offset,
                duration=5,
                sr=8000,
                res_type="kaiser_fast"
            )

            # normalize volume
            y = librosa.util.normalize(y)

            # trim silence
            y, _ = librosa.effects.trim(y)

            # detect rhythmic energy
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)

            # estimate tempo
            tempo = librosa.beat.tempo(
                onset_envelope=onset_env,
                sr=sr
            )

            tempos.append(float(tempo[0]))

        except Exception:
            pass

    # if nothing worked
    if not tempos:
        return 0

    # use median for stability
    bpm = np.median(tempos)

    # fix half/double tempo (common in rap beats)
    if bpm < 80:
        bpm *= 2
    elif bpm > 180:
        bpm /= 2

    return round(bpm)


def analyze_beat(file_path):

    try:
        bpm = analyze_bpm(file_path)

        similar_tracks = rap_bpm_library(bpm)

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
