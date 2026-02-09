
import sqlite3
import os

DB_PATH = r'C:/Users/User/projetos antigravity/FGinovaigestao/instance/database.db'

def check():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("--- Schema Info ---")
    c.execute("PRAGMA table_info(project)")
    rows = c.fetchall()
    for r in rows:
        if r[1] in ['has_env', 'has_backup_db']:
            print(f"Column: {r[1]}, Type: {r[2]}, NotNull: {r[3]}, Default: {r[4]}")

    print("\n--- Data Sample (first 5) ---")
    c.execute("SELECT id, nome, has_env, has_backup_db FROM project LIMIT 5")
    rows = c.fetchall()
    for r in rows:
        print(f"ID: {r[0]}, Name: {r[1]}, has_env: {r[2]}, has_backup_db: {r[3]}")

    conn.close()

if __name__ == "__main__":
    check()
