"""
planner.py - Study Schedule Generator
Generates a balanced daily/weekly study timetable based on user input.
"""

import pandas as pd
from datetime import datetime, timedelta


def generate_schedule(subjects: list[dict], available_hours: float, start_time: str = "08:00") -> pd.DataFrame:
    if not subjects or available_hours <= 0:
        return pd.DataFrame()

    sorted_subjects = sorted(subjects, key=lambda x: x["priority"])

    weights = {1: 3, 2: 2, 3: 1}
    total_weight = sum(weights[s["priority"]] for s in sorted_subjects)

    schedule = []
    current_time = datetime.strptime(start_time, "%H:%M")
    session_count = 0

    for subject in sorted_subjects:
        weight = weights[subject["priority"]]
        allocated_hours = (weight / total_weight) * available_hours
        allocated_minutes = int(allocated_hours * 60)

        remaining = allocated_minutes
        while remaining > 0:
            session_duration = min(25, remaining)
            end_time = current_time + timedelta(minutes=session_duration)

            schedule.append({
                "Session": f"#{session_count + 1}",
                "Subject": subject["name"],
                "Priority": "🔴 High" if subject["priority"] == 1 else "🟡 Medium" if subject["priority"] == 2 else "🟢 Low",
                "Start": current_time.strftime("%H:%M"),
                "End": end_time.strftime("%H:%M"),
                "Duration": f"{session_duration} min",
            })

            session_count += 1
            current_time = end_time
            remaining -= session_duration

            if remaining > 0:
                break_end = current_time + timedelta(minutes=5)
                schedule.append({
                    "Session": "—",
                    "Subject": "💧 Break / Water",
                    "Priority": "—",
                    "Start": current_time.strftime("%H:%M"),
                    "End": break_end.strftime("%H:%M"),
                    "Duration": "5 min",
                })
                current_time = break_end

    return pd.DataFrame(schedule)


def generate_weekly_plan(subjects: list[dict], daily_hours: float, study_days: list[str]) -> dict:
    weekly = {}
    for day in study_days:
        weekly[day] = generate_schedule(subjects, daily_hours)
    return weekly


def export_schedule_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)


def export_schedule_txt(df: pd.DataFrame, student_name: str = "Student") -> str:
    lines = [
        f"📚 STUDY SCHEDULE FOR {student_name.upper()}",
        f"Generated: {datetime.now().strftime('%A, %B %d %Y at %H:%M')}",
        "=" * 50,
        ""
    ]
    for _, row in df.iterrows():
        if row["Subject"] == "💧 Break / Water":
            lines.append(f"  [{row['Start']} - {row['End']}]  🛑 BREAK")
        else:
            lines.append(f"  [{row['Start']} - {row['End']}]  {row['Subject']} ({row['Duration']}) — Priority: {row['Priority']}")
    lines.append("")
    lines.append("=" * 50)
    lines.append("Good luck! Stay hydrated and take your breaks. 💪")
    return "\n".join(lines)