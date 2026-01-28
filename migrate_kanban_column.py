import sqlite3
import os

db_path = os.path.join('instance', 'database.db')
print(f"Migrating database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(project)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if 'show_in_kanban' not in columns:
        print("Adding 'show_in_kanban' column...")
        # SQLite uses 0/1 for boolean
        cursor.execute("ALTER TABLE project ADD COLUMN show_in_kanban BOOLEAN DEFAULT 1 NOT NULL")
        conn.commit()
        print("Migration successful.")
    else:
        print("Column 'show_in_kanban' already exists.")
        
    conn.close()
except Exception as e:
    print(f"Error during migration: {e}")
