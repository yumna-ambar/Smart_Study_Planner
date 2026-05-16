"""
health.py - Health Suggestions Engine
Provides personalized health tips based on study duration and user habits.
"""


def get_water_recommendation(study_hours: float) -> dict:
    base_glasses = 8
    extra = int(study_hours / 2)
    total = base_glasses + extra
    total_ml = total * 250

    return {
        "glasses": total,
        "ml": total_ml,
        "reminder_interval": max(30, int(60 / (total / 8))),
        "message": f"Drink {total} glasses ({total_ml}ml) of water today."
    }


def get_break_recommendation(study_hours: float) -> dict:
    short_breaks = int(study_hours * 2)
    long_breaks = max(1, int(study_hours / 2))

    tips = [
        "👀 Follow the 20-20-20 rule: every 20 min, look 20 feet away for 20 seconds.",
        "🧘 Do light stretches during short breaks — roll your shoulders and neck.",
        "🚶 Take a short walk during long breaks to boost blood flow.",
        "📵 Avoid screens during breaks — rest your eyes completely.",
        "🌬️ Take 3 deep breaths before starting each new study session.",
    ]

    return {
        "short_break_count": short_breaks,
        "long_break_count": long_breaks,
        "short_break_duration": 5,
        "long_break_duration": 15,
        "tips": tips
    }


def get_sleep_recommendation(wake_up_time: str, study_hours: float) -> dict:
    from datetime import datetime, timedelta

    recommended_sleep = 8.5 if study_hours >= 6 else 8.0
    wake = datetime.strptime(wake_up_time, "%H:%M")
    bedtime = wake - timedelta(hours=recommended_sleep)
    bedtime_str = bedtime.strftime("%I:%M %p")

    tips = []
    if study_hours >= 6:
        tips.append("📖 Heavy study day — aim for 8.5 hours of sleep for memory consolidation.")
    else:
        tips.append("😴 Aim for 8 hours tonight to keep your brain sharp.")

    tips += [
        "📵 Avoid screens 30 minutes before bed.",
        "🌡️ Keep your room cool (18–20°C) for better sleep quality.",
        "📝 Write tomorrow's tasks before sleeping to reduce anxiety.",
        "☕ Avoid caffeine after 3:00 PM.",
    ]

    return {
        "recommended_hours": recommended_sleep,
        "bedtime": bedtime_str,
        "wake_time": wake_up_time,
        "tips": tips
    }


def get_nutrition_tips(study_hours: float) -> list[str]:
    base_tips = [
        "🥜 Snack on nuts, fruits, or dark chocolate — great brain fuel.",
        "🍌 Bananas and oats provide slow-release energy.",
        "🥗 Eat a light lunch — heavy meals cause sluggishness.",
        "☕ Limit caffeine to 1–2 cups; prefer green tea for steadier energy.",
        "🚫 Avoid sugary snacks — the energy crash will hurt your focus.",
    ]
    if study_hours >= 5:
        base_tips.append("🍳 High-intensity study day: eat a protein-rich breakfast.")
    return base_tips


def get_posture_tips() -> list[str]:
    return [
        "🪑 Sit with your back straight and feet flat on the floor.",
        "💻 Keep your screen at eye level to avoid neck strain.",
        "⌨️ Elbows should be at 90° when typing.",
        "👁️ Your screen should be ~50cm from your eyes.",
        "🔆 Study in a well-lit room to reduce eye strain.",
    ]


def get_full_health_report(study_hours: float, wake_up_time: str) -> dict:
    return {
        "water": get_water_recommendation(study_hours),
        "breaks": get_break_recommendation(study_hours),
        "sleep": get_sleep_recommendation(wake_up_time, study_hours),
        "nutrition": get_nutrition_tips(study_hours),
        "posture": get_posture_tips(),
    }