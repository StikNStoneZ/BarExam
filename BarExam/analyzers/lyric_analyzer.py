import re
import math

from collections import defaultdict
import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict

d = cmudict.dict()


# -----------------------------
# TOKENIZE
# -----------------------------
def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


# -----------------------------
# RHYME TAIL
# -----------------------------
def get_rhyme_tail(word):

    if word not in d:
        return None

    pronunciation = d[word][0]

    for i, phoneme in enumerate(pronunciation):
        if "1" in phoneme or "2" in phoneme:
            return tuple(pronunciation[i:])

    return tuple(pronunciation[-2:])

def get_phonemes(word):

    if word not in d:
        return None

    return d[word][0]

def multiword_multisyllables(text):

    lines = text.split("\n")

    clusters = set()

    for line in lines:

        words = tokenize(line)

        phonemes = []

        word_boundaries = []

        for word in words:

            p = get_phonemes(word)

            if not p:
                continue

            word_boundaries.append(len(phonemes))

            phonemes.extend(p)


        for start in range(len(phonemes)):

            for size in range(3,6):

                end = start + size

                if end > len(phonemes):
                    break

                segment = tuple(phonemes[start:end])

                clusters.add(segment)


    return len(clusters)


def advanced_multisyllabic_patterns(words):

    phoneme_words = []

    for word in words:

        phonemes = get_phonemes(word)

        if not phonemes:
            continue

        phoneme_words.append((word, phonemes))


    window_map = defaultdict(set)

    MIN_WINDOW = 3
    MAX_WINDOW = 6


    for word, phonemes in phoneme_words:

        length = len(phonemes)

        for size in range(MIN_WINDOW, min(MAX_WINDOW, length) + 1):

            window = tuple(phonemes[-size:])

            window_map[window].add(word)


    clusters = []

    for window, group in window_map.items():

        # require multiple distinct words
        if len(group) < 2:
            continue

        # ignore overly common rhyme tails
        if len(group) > 10:
            continue

        clusters.append((window, group))


    # remove nested windows
    clusters.sort(key=lambda x: len(x[0]), reverse=True)

    filtered = []

    seen_words = set()

    for window, group in clusters:

        key = tuple(sorted(group))

        if key in seen_words:
            continue

        seen_words.add(key)

        filtered.append((window, group))


    return filtered

# -----------------------------
# SYLLABLE COUNT
# -----------------------------
def syllable_count(word):

    if word not in d:
        return 1

    return sum(1 for p in d[word][0] if p[-1].isdigit())


# -----------------------------
# VOCABULARY RICHNESS
# -----------------------------
def vocabulary_richness(words):

    if not words:
        return 0

    return round(len(set(words)) / len(words), 2)


# -----------------------------
# RHYME DENSITY
# -----------------------------
def rhyme_density(words):

    rhyme_map = defaultdict(list)

    for word in words:

        tail = get_rhyme_tail(word)

        if not tail:
            continue

        rhyme_map[tail].append(word)

    rhyme_words = sum(len(v) for v in rhyme_map.values() if len(v) > 1)

    return round(rhyme_words / len(words), 2) if words else 0


# -----------------------------
# INTERNAL RHYME CLUSTERS
# -----------------------------
def internal_rhymes(words):

    rhyme_map = defaultdict(set)

    for word in words:

        tail = get_rhyme_tail(word)

        if not tail:
            continue

        rhyme_map[tail].add(word)

    clusters = [v for v in rhyme_map.values() if len(v) >= 2]

    return len(clusters)


# -----------------------------
# MULTISYLLABIC INTERNAL RHYMES
# -----------------------------
def multisyllabic_internal_rhymes(words):

    rhyme_map = defaultdict(set)

    for word in words:

        tail = get_rhyme_tail(word)

        if not tail:
            continue

        if len(tail) >= 3:
            rhyme_map[tail].add(word)

    clusters = [v for v in rhyme_map.values() if len(v) >= 2]

    return len(clusters)


# -----------------------------
# MULTISYLLABIC RHYMES
# -----------------------------
def multisyllabic_rhymes(words):

    families = defaultdict(set)

    for word in words:

        tail = get_rhyme_tail(word)

        if not tail or len(tail) < 3:
            continue

        families[tail].add(word)

    return {k: v for k, v in families.items() if len(v) >= 2}


# -----------------------------
# PHRASE RHYMES
# -----------------------------
def phrase_rhymes(text):

    lines = text.lower().split("\n")

    pairs = set()

    for line in lines:

        words = tokenize(line)

        for i in range(len(words)):

            w = words[i]

            tail1 = get_rhyme_tail(w)

            if not tail1:
                continue

            for size in [2, 3]:

                if i + size >= len(words):
                    continue

                phrase = words[i+1:i+1+size]

                phonemes = []
                valid = True

                for pw in phrase:

                    if pw not in d:
                        valid = False
                        break

                    phonemes += d[pw][0]

                if not valid or len(phonemes) < 2:
                    continue

                if tail1[-2:] == tuple(phonemes[-2:]):
                    pairs.add((w, " ".join(phrase)))

    return pairs


# -----------------------------
# RHYME CHAINS
# -----------------------------
def rhyme_chain_score(text):

    lines = text.split("\n")

    endings = []

    for line in lines:

        words = tokenize(line)

        if not words:
            endings.append(None)
            continue

        endings.append(get_rhyme_tail(words[-1]))

    longest = 1
    current = 1

    for i in range(1, len(endings)):

        if endings[i] and endings[i] == endings[i-1]:
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest


# -----------------------------
# RHYME SCHEME DETECTION
# -----------------------------
def rhyme_scheme(text):

    lines = text.split("\n")

    scheme_map = {}
    scheme = []
    current_letter = "A"

    for line in lines:

        words = tokenize(line)

        if not words:
            scheme.append(None)
            continue

        tail = get_rhyme_tail(words[-1])

        if not tail:
            scheme.append(None)
            continue

        if tail not in scheme_map:

            scheme_map[tail] = current_letter
            current_letter = chr(ord(current_letter) + 1)

        scheme.append(scheme_map[tail])

    return scheme


# -----------------------------
# SCHEME COMPLEXITY
# -----------------------------
def scheme_complexity(scheme):

    filtered = [s for s in scheme if s]

    if not filtered:
        return 0

    unique = len(set(filtered))

    transitions = sum(1 for i in range(1, len(filtered)) if filtered[i] != filtered[i-1])

    return unique + transitions


# -----------------------------
# SYLLABLE PATTERNS
# -----------------------------
def syllable_patterns(text):

    lines = text.split("\n")

    patterns = []

    for line in lines:

        words = tokenize(line)

        if not words:
            continue

        pattern = tuple(syllable_count(w) for w in words)

        patterns.append(pattern)

    counts = defaultdict(int)

    for p in patterns:
        counts[p] += 1

    repeated = sum(v for v in counts.values() if v > 1)

    return repeated


# -----------------------------
# LINE RHYME DENSITY
# -----------------------------
def rhyme_density_per_line(text):

    lines = text.split("\n")

    densities = []

    for line in lines:

        words = tokenize(line)

        if not words:
            continue

        densities.append(rhyme_density(words))

    return densities


# -----------------------------
# MAIN ANALYZER
# -----------------------------
def analyze_lyrics(text):

    words = tokenize(text)

    advanced_multi = advanced_multisyllabic_patterns(words)

    multiword_multi = multiword_multisyllables(text)

    vocab = vocabulary_richness(words)

    density = rhyme_density(words)

    internal = internal_rhymes(words)

    multi_internal = multisyllabic_internal_rhymes(words)

    multis = multisyllabic_rhymes(words)

    phrase = phrase_rhymes(text)

    chain = rhyme_chain_score(text)

    scheme = rhyme_scheme(text)

    scheme_score = scheme_complexity(scheme)

    patterns = syllable_patterns(text)

    line_densities = rhyme_density_per_line(text)

    avg_line_density = round(sum(line_densities) / len(line_densities), 2) if line_densities else 0
    max_line_density = max(line_densities) if line_densities else 0

    multi_count = len(multis)
    phrase_count = len(phrase)

    # normalization
    internal_score = min(1, internal / 40)
    multi_internal_score = min(1, multi_internal / 15)
    multi_score = min(1, multi_count / 20)
    phrase_score = min(1, phrase_count / 20)
    pattern_score = min(1, patterns / 10)
    scheme_score = min(1, scheme_score / 10)
    chain_score = min(1, chain / 4)
    advanced_multi_score = min(1, len(advanced_multi) / 20)

    multiword_multi_score = min(1, multiword_multi / 40)

    score = (
        vocab * 25 +
        density * 30 +
        internal_score * 8 +
        multi_internal_score * 8 +
        multi_score * 8 +
        phrase_score * 6 +
        advanced_multi_score * 8 +
        multiword_multi_score * 5 +
        pattern_score * 2 +
        scheme_score * 2 +
        chain_score * 1
    )

    score = round(min(score, 100), 1)

    # -----------------------------
    # SCORE INTERPRETATION
    # -----------------------------
    if score < 60:
        label = "Baisc rhyme structure"
    elif score < 70:
        label = "Moderate Technical Control"
    elif score < 80:
        label = "Highly Technical"
    elif score < 85:
        label = "Elite Rhyme Craftsmanship"
    elif score < 90:
        label = "Legendary Rhyme Density"
    else:
        label = "What The Fuck"

    return {
        "total_words": len(words),
        "vocabulary_richness": vocab,
        "rhyme_density": density,
        "technical_complexity": score,
	"score_label": label,
        "internal_rhyme_count": internal,
        "multisyllabic_rhyme_count": multi_count,
        "phrase_rhyme_count": phrase_count,
        "average_line_rhyme_density": avg_line_density,
        "max_line_rhyme_density": max_line_density
    }
