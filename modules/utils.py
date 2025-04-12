"""Hilfsfunktionen."""

import time

def slow_print(text: str, delay: float = 0.05):
    """Gibt Text langsam aus, um eine dramatische Wirkung zu erzeugen."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
