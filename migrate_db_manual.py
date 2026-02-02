import sqlite3
import os

DB_PATH = 'instance/database.db'

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check table name
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='project'")
    if not cursor.fetchone():
        print("Table 'project' not found.")
        conn.close()
        return

    print("Table 'project' found.")

    # Get existing columns
    cursor.execute("PRAGMA table_info(project)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Existing columns: {columns}")

    if 'has_github' not in columns:
        print("Adding 'has_github' column...")
        cursor.execute("ALTER TABLE project ADD COLUMN has_github BOOLEAN DEFAULT 0 NOT NULL")
        print("Column 'has_github' added.")
    else:
        print("'has_github' already exists.")

    if 'has_drive' not in columns:
        print("Adding 'has_drive' column...")
        cursor.execute("ALTER TABLE project ADD COLUMN has_drive BOOLEAN DEFAULT 0 NOT NULL")
        print("Column 'has_drive' added.")
    else:
        print("'has_drive' already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
