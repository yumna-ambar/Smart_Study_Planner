"""
app.py - Smart Study Planner with Health Suggestions
Main Streamlit application entry point.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Module imports ────────────────────────────────────────────────────────────
from modules.planner import generate_schedule, generate_weekly_plan, export_schedule_csv, export_schedule_txt
from modules.health import get_full_health_report
from modules.pomodoro import get_pomodoro_plan, get_pomodoro_stats
from modules.motivator import get_daily_quote, get_random_quote, get_subject_emoji, load_quotes

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Sora', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #f0f0f0;
    }

    .card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }

    .stat-box {
        background: rgba(255,255,255,0.09);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Sora', sans-serif;
        color: #a78bfa;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #c4b5fd;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .quote-block {
        background: linear-gradient(135deg, rgba(167,139,250,0.15), rgba(96,165,250,0.1));
        border-left: 4px solid #a78bfa;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        font-style: italic;
        font-size: 1.05rem;
    }

    .tip-item {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin: 0.3rem 0;
        font-size: 0.92rem;
    }

    .pomo-study {
        background: rgba(167,139,250,0.2);
        border-left: 3px solid #a78bfa;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
    }
    .pomo-break {
        background: rgba(52,211,153,0.1);
        border-left: 3px solid #34d399;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
    }

    .section-header {
        font-family: 'Sora', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #c4b5fd;
        margin-bottom: 0.8rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(196,181,253,0.2);
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
    }

    section[data-testid="stSidebar"] {
        background: rgba(15,12,41,0.9);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #6d28d9, #4338ca);
        transform: translateY(-1px);
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        background: rgba(255,255,255,0.05);
        color: #c4b5fd;
        border: 1px solid rgba(255,255,255,0.1);
        font-family: 'Sora', sans-serif;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(79,70,229,0.4)) !important;
        border-color: #a78bfa !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Session state initialisation ──────────────────────────────────────────────
if "subjects" not in st.session_state:
    st.session_state.subjects = []
if "schedule_generated" not in st.session_state:
    st.session_state.schedule_generated = False
if "completed_sessions" not in st.session_state:
    st.session_state.completed_sessions = set()
if "quote_refreshed" not in st.session_state:
    st.session_state.quote_refreshed = False
if "current_quote" not in st.session_state:
    st.session_state.current_quote = get_daily_quote()


# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧠 Smart Study Planner")
    st.markdown("---")

    st.markdown("### 👤 Student Info")
    student_name = st.text_input("Your Name", placeholder="e.g. Aisha", value="Student")
    wake_up_time = st.time_input("⏰ Wake-up Time", value=datetime.strptime("07:00", "%H:%M").time())
    study_start = st.time_input("📖 Study Start Time", value=datetime.strptime("09:00", "%H:%M").time())

    st.markdown("---")
    st.markdown("### 📚 Add Subjects")

    with st.form("add_subject_form", clear_on_submit=True):
        subj_name = st.text_input("Subject Name", placeholder="e.g. Mathematics")
        subj_priority = st.selectbox("Priority", [1, 2, 3], format_func=lambda x: {1: "🔴 High", 2: "🟡 Medium", 3: "🟢 Low"}[x])
        add_btn = st.form_submit_button("➕ Add Subject")

        if add_btn and subj_name.strip():
            st.session_state.subjects.append({
                "name": subj_name.strip(),
                "priority": subj_priority,
            })
            st.success(f"Added: {subj_name.strip()}")

    if st.session_state.subjects:
        st.markdown("**Current subjects:**")
        for i, s in enumerate(st.session_state.subjects):
            col1, col2 = st.columns([4, 1])
            emoji = get_subject_emoji(s["name"])
            priority_label = {1: "🔴", 2: "🟡", 3: "🟢"}[s["priority"]]
            col1.markdown(f"{emoji} {s['name']} {priority_label}")
            if col2.button("✕", key=f"del_{i}", help="Remove"):
                st.session_state.subjects.pop(i)
                st.rerun()

    st.markdown("---")
    st.markdown("### ⏱️ Study Hours")
    available_hours = st.slider("Hours available today", 1.0, 12.0, 4.0, 0.5)

    st.markdown("### 📅 Study Days (Weekly)")
    all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    study_days = st.multiselect("Select study days", all_days, default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

    st.markdown("---")
    generate_btn = st.button("🚀 Generate My Plan")

    if st.session_state.subjects:
        st.markdown("---")
        if st.button("🗑️ Clear All Subjects"):
            st.session_state.subjects = []
            st.session_state.schedule_generated = False
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════════════════════════

col_title, col_date = st.columns([3, 1])
with col_title:
    st.markdown(f"# 📚 Welcome, {student_name}!")
    st.markdown(f"*{datetime.now().strftime('%A, %B %d, %Y')}*")
with col_date:
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric("Study Hours Today", f"{available_hours}h")

quote = st.session_state.current_quote
st.markdown(f"""
<div class="quote-block">
    💬 <strong>"{quote['quote']}"</strong><br>
    <span style="color:#a78bfa; font-size:0.85rem;">— {quote['author']}</span>
</div>
""", unsafe_allow_html=True)

col_q1, col_q2 = st.columns([1, 5])
with col_q1:
    if st.button("🔄 New Quote"):
        st.session_state.current_quote = get_random_quote()
        st.rerun()


if generate_btn:
    if not st.session_state.subjects:
        st.error("Please add at least one subject in the sidebar first!")
    else:
        st.session_state.schedule_generated = True
        st.session_state.completed_sessions = set()


if st.session_state.schedule_generated and st.session_state.subjects:
    tabs = st.tabs(["📋 Today's Schedule", "🌿 Health Hub", "🍅 Pomodoro Plan", "📅 Weekly View", "📊 Progress"])

    wake_str = wake_up_time.strftime("%H:%M")
    start_str = study_start.strftime("%H:%M")

    schedule_df = generate_schedule(st.session_state.subjects, available_hours, start_str)
    health_report = get_full_health_report(available_hours, wake_str)
    pomodoro_sessions = get_pomodoro_plan(int(available_hours * 60))
    pomodoro_stats = get_pomodoro_stats(int(available_hours * 60))
    weekly_plan = generate_weekly_plan(st.session_state.subjects, available_hours, study_days) if study_days else {}

    with tabs[0]:
        st.markdown("<div class='section-header'>📋 Your Study Schedule for Today</div>", unsafe_allow_html=True)

        study_sessions = schedule_df[schedule_df["Subject"] != "💧 Break / Water"] if not schedule_df.empty else pd.DataFrame()
        break_sessions = schedule_df[schedule_df["Subject"] == "💧 Break / Water"] if not schedule_df.empty else pd.DataFrame()

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='stat-box'><div class='stat-number'>{len(st.session_state.subjects)}</div><div class='stat-label'>Subjects</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='stat-box'><div class='stat-number'>{len(study_sessions)}</div><div class='stat-label'>Study Sessions</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='stat-box'><div class='stat-number'>{len(break_sessions)}</div><div class='stat-label'>Breaks</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='stat-box'><div class='stat-number'>{available_hours}h</div><div class='stat-label'>Total Study</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if not schedule_df.empty:
            def highlight_rows(row):
                if row["Subject"] == "💧 Break / Water":
                    return ["background-color: rgba(52,211,153,0.1); color: #6ee7b7"] * len(row)
                elif "High" in str(row.get("Priority", "")):
                    return ["background-color: rgba(239,68,68,0.08)"] * len(row)
                return [""] * len(row)

            styled_df = schedule_df.style.apply(highlight_rows, axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📥 Export Your Schedule")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            csv_data = export_schedule_csv(schedule_df)
            st.download_button("⬇️ Download as CSV", csv_data, file_name=f"study_schedule_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
        with col_e2:
            txt_data = export_schedule_txt(schedule_df, student_name)
            st.download_button("⬇️ Download as TXT", txt_data, file_name=f"study_schedule_{datetime.now().strftime('%Y%m%d')}.txt", mime="text/plain", use_container_width=True)

    with tabs[1]:
        st.markdown("<div class='section-header'>🌿 Health & Wellness Hub</div>", unsafe_allow_html=True)

        h_col1, h_col2 = st.columns(2)

        with h_col1:
            water = health_report["water"]
            st.markdown(f"""
            <div class='card'>
                <h3>💧 Hydration Goal</h3>
                <div class='stat-number' style='color:#60a5fa;'>{water['glasses']} glasses</div>
                <p style='color:#93c5fd;'>{water['ml']} ml total</p>
                <p>Set a reminder every <strong>{water['reminder_interval']} minutes</strong></p>
            </div>
            """, unsafe_allow_html=True)

            sleep = health_report["sleep"]
            st.markdown(f"""
            <div class='card'>
                <h3>😴 Sleep Recommendation</h3>
                <div class='stat-number' style='color:#f472b6;'>{sleep['recommended_hours']}h</div>
                <p style='color:#f9a8d4;'>🌙 Bedtime: <strong>{sleep['bedtime']}</strong></p>
                <p>⏰ Wake up: <strong>{sleep['wake_time']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with h_col2:
            breaks = health_report["breaks"]
            st.markdown(f"""
            <div class='card'>
                <h3>🛑 Break Schedule</h3>
                <p>🟣 <strong>{breaks['short_break_count']}</strong> short breaks ({breaks['short_break_duration']} min each)</p>
                <p>🟠 <strong>{breaks['long_break_count']}</strong> long break(s) ({breaks['long_break_duration']} min each)</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='card'><h3>🥗 Nutrition Tips</h3>", unsafe_allow_html=True)
            for tip in health_report["nutrition"]:
                st.markdown(f"<div class='tip-item'>{tip}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h3>🛏️ Sleep Tips</h3>", unsafe_allow_html=True)
        for tip in health_report["sleep"]["tips"]:
            st.markdown(f"<div class='tip-item'>{tip}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.markdown("<div class='card'><h3>🧘 Break Tips</h3>", unsafe_allow_html=True)
            for tip in health_report["breaks"]["tips"]:
                st.markdown(f"<div class='tip-item'>{tip}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with p_col2:
            st.markdown("<div class='card'><h3>🪑 Posture & Ergonomics</h3>", unsafe_allow_html=True)
            for tip in health_report["posture"]:
                st.markdown(f"<div class='tip-item'>{tip}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("<div class='section-header'>🍅 Pomodoro Session Plan</div>", unsafe_allow_html=True)

        ps = pomodoro_stats
        pc1, pc2, pc3, pc4 = st.columns(4)
        with pc1:
            st.markdown(f"""<div class='stat-box'><div class='stat-number'>{ps['full_pomodoros']}</div><div class='stat-label'>Pomodoros</div></div>""", unsafe_allow_html=True)
        with pc2:
            st.markdown(f"""<div class='stat-box'><div class='stat-number'>{ps['short_breaks']}</div><div class='stat-label'>Short Breaks</div></div>""", unsafe_allow_html=True)
        with pc3:
            st.markdown(f"""<div class='stat-box'><div class='stat-number'>{ps['long_breaks']}</div><div class='stat-label'>Long Breaks</div></div>""", unsafe_allow_html=True)
        with pc4:
            st.markdown(f"""<div class='stat-box'><div class='stat-number'>{ps['total_time_hrs']}h</div><div class='stat-label'>Total Time</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**How to use:** Work for 25 minutes → take a short break → repeat. Every 4 sessions, take a longer break.")
        st.markdown("---")

        for session in pomodoro_sessions:
            css_class = "pomo-study" if session["type"] == "study" else "pomo-break"
            st.markdown(f"""
            <div class='{css_class}'>
                <strong>{session['label']}</strong> &nbsp;·&nbsp; {session['duration_min']} minutes
            </div>
            """, unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("<div class='section-header'>📅 Weekly Study Plan</div>", unsafe_allow_html=True)

        if not study_days:
            st.info("Please select study days in the sidebar.")
        else:
            selected_day = st.selectbox("View schedule for:", study_days)
            if selected_day and selected_day in weekly_plan:
                day_df = weekly_plan[selected_day]
                if not day_df.empty:
                    st.dataframe(day_df, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("### 📊 Weekly Overview")
            summary_data = []
            for day in study_days:
                day_df = weekly_plan.get(day, pd.DataFrame())
                study_sessions_count = len(day_df[day_df["Subject"] != "💧 Break / Water"]) if not day_df.empty else 0
                summary_data.append({
                    "Day": day,
                    "Study Sessions": study_sessions_count,
                    "Hours": available_hours,
                    "Subjects": len(st.session_state.subjects),
                })
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

    with tabs[4]:
        st.markdown("<div class='section-header'>📊 Session Progress Tracker</div>", unsafe_allow_html=True)
        st.markdown("Check off sessions as you complete them to track your progress today.")

        if not schedule_df.empty:
            study_only = schedule_df[schedule_df["Subject"] != "💧 Break / Water"].reset_index(drop=True)

            for i, row in study_only.iterrows():
                key = f"session_{i}"
                col_check, col_info = st.columns([1, 8])
                is_done = key in st.session_state.completed_sessions
                with col_check:
                    if st.checkbox("", value=is_done, key=f"cb_{i}"):
                        st.session_state.completed_sessions.add(key)
                    else:
                        st.session_state.completed_sessions.discard(key)
                with col_info:
                    emoji = get_subject_emoji(row["Subject"])
                    done_style = "text-decoration: line-through; color: #6b7280;" if is_done else ""
                    st.markdown(f"""
                    <div style='{done_style} padding: 0.3rem 0;'>
                        {emoji} <strong>{row['Subject']}</strong> &nbsp;|&nbsp; {row['Start']} – {row['End']} &nbsp;|&nbsp; {row['Duration']}
                    </div>
                    """, unsafe_allow_html=True)

            total_sessions = len(study_only)
            done_count = len([k for k in st.session_state.completed_sessions if k.startswith("session_")])
            progress = done_count / total_sessions if total_sessions > 0 else 0

            st.markdown("---")
            st.markdown(f"### Progress: {done_count}/{total_sessions} sessions completed")
            st.progress(progress)

            if progress == 1.0:
                st.balloons()
                st.success(f"🎉 Amazing work, {student_name}! You've completed all your study sessions today!")
            elif progress >= 0.5:
                st.info(f"💪 Halfway there, {student_name}! Keep it up!")
            elif progress > 0:
                st.info("🚀 Great start! Keep going!")

else:
    st.markdown("---")
    st.markdown("""
    <div class='card' style='text-align:center; padding: 3rem;'>
        <h2>👈 Get Started!</h2>
        <p style='font-size:1.1rem; color:#c4b5fd;'>
            Add your subjects and study hours in the sidebar, then click<br>
            <strong>🚀 Generate My Plan</strong> to create your personalized schedule.
        </p>
        <br>
        <p>✅ Personalized study timetable &nbsp;·&nbsp; 🌿 Health tips &nbsp;·&nbsp; 🍅 Pomodoro plan &nbsp;·&nbsp; 📅 Weekly view &nbsp;·&nbsp; 📊 Progress tracker</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#6b7280; font-size:0.8rem; padding-bottom:1rem;'>
    🧠 Smart Study Planner &nbsp;·&nbsp; Built with Python & Streamlit &nbsp;·&nbsp; Study smart, stay healthy 💜
</div>
""", unsafe_allow_html=True)