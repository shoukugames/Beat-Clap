"""Beat Clap: clap along with English syllables at 100 BPM."""

__version__ = "0.4.0"  # the one place to bump; packaging scripts read it from here

# True when running in a web browser (pygbag / WebAssembly).
WEB = __import__("sys").platform == "emscripten"
