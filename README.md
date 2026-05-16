# 🧠 Smart Study Planner with Health Suggestions

> A Python-powered study planning web app that helps students build balanced study schedules while keeping their health in check.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Problem Statement

Students often struggle to manage study time across multiple subjects while neglecting their health — skipping breaks, forgetting to hydrate, and sleeping too little. This tool provides a simple, intelligent system that:

- Generates a **balanced, priority-based study timetable**
- Recommends **health habits** (water intake, sleep, breaks, nutrition, posture)
- Structures sessions using the **Pomodoro technique**
- Tracks **weekly progress** and allows session completion tracking

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 **Study Schedule Generator** | Creates a daily timetable based on subjects, priorities, and available hours |
| 🌿 **Health Hub** | Water intake, sleep, break, nutrition, and posture recommendations |
| 🍅 **Pomodoro Planner** | Breaks study time into 25-min sessions with automatic break scheduling |
| 📅 **Weekly View** | Plan and view your full week's study distribution |
| 📊 **Progress Tracker** | Check off completed sessions with a live progress bar |
| 💬 **Daily Motivational Quote** | A fresh quote every day with a refresh option |
| 📥 **Export Schedule** | Download your timetable as CSV or plain text |

---

## 🗂️ Project Structure
smart-study-planner/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignored files
│
├── modules/
│   ├── init.py         # Package exports
│   ├── planner.py          # Schedule generation logic
│   ├── health.py           # Health recommendations engine
│   ├── pomodoro.py         # Pomodoro session planning
│   └── motivator.py        # Quotes and subject emoji mapping
│
└── data/
└── quotes.json         # 20 motivational quotes database

---
## 🚀 Getting Started

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/smart-study-planner.git
cd smart-study-planner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** Streamlit
- **Data:** Pandas

---

## 📄 License

This project is licensed under the MIT License.

---

_Study smart. Stay healthy. Keep going._ 💜