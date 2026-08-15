import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "ecobuddy.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    family_members INTEGER NOT NULL,
    city TEXT NOT NULL,
    month INTEGER NOT NULL,
    consumption_kwh REAL NOT NULL,
    bill REAL NOT NULL,
    eco_score INTEGER NOT NULL,
    biggest_consumer TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ EcoBuddy database initialized successfully!")
print(f"📁 Database: {DB_PATH}")