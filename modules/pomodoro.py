"""
pomodoro.py - Pomodoro Timer Logic
Handles Pomodoro session tracking and statistics.
"""


def get_pomodoro_plan(total_minutes: int) -> list[dict]:
    sessions = []
    elapsed = 0
    session_num = 1
    pomodoro_count = 0

    while elapsed < total_minutes:
        study_duration = min(25, total_minutes - elapsed)
        sessions.append({
            "type": "study",
            "label": f"🍅 Pomodoro #{session_num}",
            "duration_min": study_duration,
            "elapsed_start": elapsed,
        })
        elapsed += study_duration
        session_num += 1
        pomodoro_count += 1

        if elapsed >= total_minutes:
            break

        if pomodoro_count % 4 == 0:
            break_duration = 15
            break_label = "☕ Long Break"
        else:
            break_duration = 5
            break_label = "💧 Short Break"

        sessions.append({
            "type": "break",
            "label": break_label,
            "duration_min": break_duration,
            "elapsed_start": elapsed,
        })
        elapsed += break_duration

    return sessions


def get_pomodoro_stats(total_study_minutes: int) -> dict:
    full_pomodoros = total_study_minutes // 25
    remaining = total_study_minutes % 25
    short_breaks = max(0, full_pomodoros - (full_pomodoros // 4))
    long_breaks = full_pomodoros // 4
    total_break_time = (short_breaks * 5) + (long_breaks * 15)
    total_time = total_study_minutes + total_break_time

    return {
        "full_pomodoros": full_pomodoros,
        "partial_session": remaining,
        "short_breaks": short_breaks,
        "long_breaks": long_breaks,
        "total_break_time_min": total_break_time,
        "total_time_min": total_time,
        "total_time_hrs": round(total_time / 60, 1),
    }