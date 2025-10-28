# selene.py
import sqlite3
from datetime import date

DB_FILE = "selene.db"

# create table if it doesn't exist
with sqlite3.connect(DB_FILE) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cycle_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT,
            phase TEXT,
            symptoms TEXT,
            mood TEXT
        )
    """)

def log_cycle():
    today = input("Date (YYYY-MM-DD) [default today]: ").strip() or str(date.today())
    phase = input("Phase (start/end/etc): ").strip()
    symptoms = input("Symptoms (comma-separated): ").strip()
    mood = input("Mood: ").strip()

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO cycle_log (log_date, phase, symptoms, mood) VALUES (?,?,?,?)",
            (today, phase, symptoms, mood),
        )
    print(f"\n🌙 Cycle info saved for {today}!\n")

def show_logs():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("SELECT * FROM cycle_log ORDER BY log_date DESC").fetchall()
    print("\n=== Your Logged Cycles ===")
    for r in rows:
        print(f"{r[1]} | phase: {r[2]} | mood: {r[4]} | symptoms: {r[3]}")

if __name__ == "__main__":
    while True:
        cmd = input("» ").strip().lower()
        if cmd == "log":
            log_cycle()
        elif cmd == "show":
            show_logs()
        elif cmd in ("quit", "exit"):
            print("Goodbye 🌸")
            break
        else:
            print("Commands: log, show, quit")
