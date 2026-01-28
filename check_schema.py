import sqlite3
import os

db_path = 'instance/database.db'
if not os.path.exists(db_path):
    print("Database file does not exist.")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables:", [t[0] for t in tables])
    
    # Try querying User with quotes if needed
    try:
        cursor.execute('SELECT count(*) FROM "user"')
        print(f"User count (quoted): {cursor.fetchone()[0]}")
    except:
        pass
        
    try:
        cursor.execute("SELECT count(*) FROM client")
        print(f"Client count: {cursor.fetchone()[0]}")
    except:
        pass
except Exception as e:
    print(e)
conn.close()
