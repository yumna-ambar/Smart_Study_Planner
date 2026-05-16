"""
motivator.py - Motivational Quotes Engine
Loads and serves motivational quotes based on date or random selection.
"""

import json
import random
from datetime import datetime
from pathlib import Path


def load_quotes(filepath: str = None) -> list[dict]:
    if filepath is None:
        base = Path(__file__).parent.parent / "data" / "quotes.json"
        filepath = str(base)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return [{"quote": "Stay focused and keep going!", "author": "Unknown"}]


def get_daily_quote(quotes: list[dict] = None) -> dict:
    if quotes is None:
        quotes = load_quotes()

    day_index = datetime.now().timetuple().tm_yday % len(quotes)
    return quotes[day_index]


def get_random_quote(quotes: list[dict] = None) -> dict:
    if quotes is None:
        quotes = load_quotes()
    return random.choice(quotes)


def get_subject_emoji(subject_name: str) -> str:
    name = subject_name.lower()
    mapping = {
        "math": "📐", "mathematics": "📐", "calculus": "📐", "algebra": "📐",
        "physics": "⚛️", "chemistry": "🧪", "biology": "🧬",
        "english": "📖", "literature": "📖", "writing": "✍️",
        "history": "🏛️", "geography": "🌍",
        "computer": "💻", "programming": "💻", "coding": "💻", "cs": "💻",
        "economics": "📈", "business": "💼",
        "art": "🎨", "music": "🎵",
        "science": "🔬", "psychology": "🧠",
        "language": "🗣️", "french": "🇫🇷", "spanish": "🇪🇸", "arabic": "📜",
    }
    for key, emoji in mapping.items():
        if key in name:
            return emoji
    return "📚"