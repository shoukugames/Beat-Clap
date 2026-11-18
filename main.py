"""Web entry point for pygbag (https://pygame-web.github.io): Beat Clap in the browser.

Build with:  python3 tools/build_web.py     (writes build/web/)
The desktop game still starts with `python3 -m beatclap`; nothing here changes it.
In the browser there is no microphone: tap the screen (or press Space) to clap.
"""
import asyncio

import numpy  # noqa: F401  (imported here so pygbag loads numpy)
import pygame  # noqa: F401  (imported here so pygbag loads pygame)

from beatclap.game import Game


async def main():
    await Game().run_web()


asyncio.run(main())
