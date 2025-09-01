import sqlite3
import csv
import os

# SQLite database file
SQLITE_DB = "mkw.db"

# Folder to store CSVs
OUTPUT_FOLDER = "csv_exports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(SQLITE_DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get all table names
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row["name"] for row in cur.fetchall()]

for table in tables:
    cur.execute(f"SELECT * FROM {table};")
    rows = cur.fetchall()
    if not rows:
        print(f"Table '{table}' is empty, skipping.")
        continue

    # CSV file path
    csv_file = os.path.join(OUTPUT_FOLDER, f"{table}.csv")
    
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(rows[0].keys())
        # Write data
        for row in rows:
            writer.writerow(list(row))
    
    print(f"Exported table '{table}' to {csv_file}")

cur.close()
conn.close()
print("All tables exported successfully!")
