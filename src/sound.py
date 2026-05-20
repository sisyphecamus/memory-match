# Memory Match v2.0 — Sound generation and playback

import math
import struct
import wave
import os
import tempfile

SAMPLE_RATE = 44100


def _generate_wav_bytes(frames, filename):
    """Write raw float samples to a WAV file and return the path."""
    path = os.path.join(tempfile.gettempdir(), filename)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        data = b""
        for sample in frames:
            clipped = max(-1.0, min(1.0, sample))
            data += struct.pack("<h", int(clipped * 32767))
        wf.writeframes(data)
    return path


def generate_sounds():
    """Generate four programmatic game sound effects.

    Returns a dict mapping sound names to file paths.
    """
    paths = {}

    # Flip — short rising tone C5→E5, sine wave, 80ms
    dur = 0.08
    n = int(SAMPLE_RATE * dur)
    frames = []
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = 523 + (659 - 523) * (i / n)
        env = 1.0 - (i / n)
        frames.append(math.sin(2 * math.pi * freq * t) * env * 0.6)
    paths["flip"] = _generate_wav_bytes(frames, "mm_flip.wav")

    # Match — two-note ascending chime C5→G5, 200ms
    dur = 0.20
    n = int(SAMPLE_RATE * dur)
    frames = []
    for i in range(n):
        t = i / SAMPLE_RATE
        if t < 0.1:
            freq = 523 + (784 - 523) * (t / 0.1)
        else:
            freq = 784
        env = max(0, 1.0 - (t / dur) * 1.2)
        frames.append(math.sin(2 * math.pi * freq * t) * env * 0.5)
    paths["match"] = _generate_wav_bytes(frames, "mm_match.wav")

    # Mismatch — low buzz 200Hz descending, square-ish wave, 150ms
    dur = 0.15
    n = int(SAMPLE_RATE * dur)
    frames = []
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = 200 - 30 * (i / n)
        env = 1.0 - (i / n)
        raw = math.sin(2 * math.pi * freq * t)
        square = 1.0 if raw > 0 else -1.0
        frames.append(square * env * 0.25)
    paths["mismatch"] = _generate_wav_bytes(frames, "mm_mismatch.wav")

    # Victory — major chord arpeggio C5-E5-G5-C6, 600ms
    dur = 0.60
    n = int(SAMPLE_RATE * dur)
    notes = [
        (0.00, 0.14, 523),
        (0.14, 0.28, 659),
        (0.28, 0.42, 784),
        (0.42, 0.60, 1047),
    ]
    frames = []
    for i in range(n):
        t = i / SAMPLE_RATE
        val = 0.0
        for start, end, freq in notes:
            if start <= t < end:
                local = (t - start) / (end - start)
                env = 1.0 - local * 0.3
                val += math.sin(2 * math.pi * freq * t) * env * 0.35
        frames.append(val)
    paths["victory"] = _generate_wav_bytes(frames, "mm_victory.wav")

    return paths


class SoundManager:
    """Manages game sound playback via pygame.mixer."""

    def __init__(self):
        import pygame

        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
        self._paths = generate_sounds()
        self._sounds = {}
        for name, path in self._paths.items():
            self._sounds[name] = pygame.mixer.Sound(path)

    def play(self, name):
        if name in self._sounds:
            self._sounds[name].play()
