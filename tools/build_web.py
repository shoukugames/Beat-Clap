#!/usr/bin/env python3
"""Build the browser version into build/web/ with pygbag (https://pygame-web.github.io).

1. Renders each stage's music once into web_music/stage<N>.ogg at the browser's mixing rate
   (48000 Hz); rendering takes over a second per stage even on a PC.
2. Runs pygbag, which packs the game folder into build/web/.

Needs: numpy, pygame, pygbag (python3 -m pip install pygbag) and ffmpeg on PATH (or FFMPEG=/path).
"""
import os
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from beatclap import music  # noqa: E402
from beatclap.stages import STAGES  # noqa: E402

RATE = 48000   # what browsers mix at, whatever a game asks for


def render_music(ffmpeg):
    out = os.path.join(ROOT, "web_music")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    with tempfile.TemporaryDirectory() as tmp:
        for i, stage in enumerate(STAGES):
            pcm = (music.render(stage.song, RATE) * 32767).astype(np.int16)
            wav = os.path.join(tmp, f"stage{i}.wav")
            with wave.open(wav, "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(RATE)
                handle.writeframes(pcm.tobytes())
            subprocess.run([ffmpeg, "-loglevel", "error", "-y", "-i", wav, "-c:a", "libvorbis", "-q:a", "5",
                            os.path.join(out, f"stage{i}.ogg")], check=True)
    size = sum(os.path.getsize(os.path.join(out, f)) for f in os.listdir(out))
    print(f"web_music: {len(STAGES)} stages, {size // 1024} KB")


ffmpeg = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
if not ffmpeg:
    sys.exit("ffmpeg not found (set FFMPEG=/path/to/ffmpeg)")
render_music(ffmpeg)
env = dict(os.environ, PATH=os.path.dirname(os.path.abspath(ffmpeg)) + os.pathsep + os.environ.get("PATH", ""))
subprocess.run([sys.executable, "-m", "pygbag", "--build", "--title", "Beat Clap", "--app_name", "beat-clap", "."],
               cwd=ROOT, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if not os.path.exists(os.path.join(ROOT, "build", "web", "index.html")):
    sys.exit("pygbag did not write build/web/index.html")
print("build/web ready: upload the folder as-is")

# pygbag sometimes sizes the canvas before the game has opened its window, squeezing the game
# into a square: add a small script that keeps it the game's shape (tools/web_canvas_fix.py).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web_canvas_fix  # noqa: E402

web_canvas_fix.apply(os.path.join(ROOT, "build", "web", "index.html"))
