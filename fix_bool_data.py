
import sqlite3
import os

DB_PATH = r'C:/Users/User/projetos antigravity/FGinovaigestao/instance/database.db'

def fix_data():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("Converting 0 (False) to NULL (None) for 3-state logic...")
    
    # 1. Update has_env
    c.execute("UPDATE project SET has_env = NULL WHERE has_env = 0")
    print(f"Updated has_env: {c.rowcount} rows affected.")
    
    # 2. Update has_backup_db
    c.execute("UPDATE project SET has_backup_db = NULL WHERE has_backup_db = 0")
    print(f"Updated has_backup_db: {c.rowcount} rows affected.")
    
    conn.commit()
    conn.close()
    print("Data fix completed.")

if __name__ == "__main__":
    fix_data()
