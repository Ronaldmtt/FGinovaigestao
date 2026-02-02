import sqlite3
import os

DB_PATHS = ['instance/database.db', 'database.db', 'gestao_app.db']

import sys

def get_db_path():
    # If path provided via argument
    if len(sys.argv) > 1:
        arg_path = sys.argv[1]
        if os.path.exists(arg_path):
            return arg_path
        print(f"Provided argument '{arg_path}' not found.")

    # Try from env var first
    try:
        from dotenv import load_dotenv
        load_dotenv()
        db_url = os.environ.get("DATABASE_URL")
        if db_url and db_url.startswith("sqlite:///"):
            path = db_url.replace("sqlite:///", "")
            if os.path.exists(path):
                return path
    except ImportError:
        pass
    
    # Try common paths
    for path in DB_PATHS:
        if os.path.exists(path):
            return path
    return None

def migrate():
    db_path = get_db_path()
    if not db_path:
        print("Database not found in common locations.")
        print(f"Searched: {DB_PATHS} and DATABASE_URL env var")
        return

    print(f"Migrating database at: {db_path}")
    conn = sqlite3.connect(db_path)
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
