import sqlite3

conn = sqlite3.connect("database/ecobuddy.db")
cursor = conn.cursor()

# ---------------- CARBON ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS carbon_data(

id INTEGER PRIMARY KEY AUTOINCREMENT,

transport TEXT,

distance REAL,

electricity REAL,

diet TEXT,

emission REAL

)
""")

# ---------------- WATER ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS water_data(

id INTEGER PRIMARY KEY AUTOINCREMENT,

family INTEGER,

daily REAL,

source TEXT,

monthly REAL,

bill REAL

)
""")

# ---------------- ENERGY ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS energy_data(

id INTEGER PRIMARY KEY AUTOINCREMENT,

members INTEGER,

units REAL,

appliance TEXT,

bill REAL

)
""")

conn.commit()
conn.close()

print("Database Updated Successfully!")