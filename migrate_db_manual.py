import os
import sys

def migrate():
    # Load env vars
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv not installed, skipping .env load")

    db_url = os.environ.get("DATABASE_URL", "")
    
    # Logic for PostgreSQL
    if "postgres" in db_url:
        print("Detected PostgreSQL database.")
        try:
            import psycopg2
        except ImportError:
            print("Error: psycopg2 module not found. Please install it to migrate Postgres.")
            return

        try:
            conn = psycopg2.connect(db_url)
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Check for columns
            print("Checking existing columns in 'project' table...")
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='project';")
            existing_columns = [row[0] for row in cursor.fetchall()]
            print(f"Existing columns: {existing_columns}")

            if 'has_github' not in existing_columns:
                print("Adding 'has_github' column...")
                cursor.execute("ALTER TABLE project ADD COLUMN has_github BOOLEAN DEFAULT FALSE;")
                print("Column 'has_github' added.")
            else:
                print("'has_github' already exists.")

            if 'has_drive' not in existing_columns:
                print("Adding 'has_drive' column...")
                cursor.execute("ALTER TABLE project ADD COLUMN has_drive BOOLEAN DEFAULT FALSE;")
                print("Column 'has_drive' added.")
            else:
                print("'has_drive' already exists.")

            conn.close()
            print("Migration finished (PostgreSQL).")

        except Exception as e:
            print(f"PostgreSQL Migration Failed: {e}")
        return

    # Logic for SQLite (Local/Default)
    import sqlite3
    print("Detected SQLite database (or no DATABASE_URL set).")
    
    # Find DB Path
    db_path = None
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    if not db_path and db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
    
    if not db_path:
        # Try common paths
        for path in ['instance/database.db', 'database.db', 'gestao_app.db']:
            if os.path.exists(path):
                db_path = path
                break
    
    if not db_path:
         print("SQLite database not found. Usage: python migrate_db_manual.py <path_to_db>")
         return

    print(f"Migrating SQLite database at: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(project)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Existing columns: {columns}")

        if 'has_github' not in columns:
            print("Adding 'has_github' column...")
            cursor.execute("ALTER TABLE project ADD COLUMN has_github BOOLEAN DEFAULT 0 NOT NULL")
            print("Column 'has_github' added.")

        if 'has_drive' not in columns:
            print("Adding 'has_drive' column...")
            cursor.execute("ALTER TABLE project ADD COLUMN has_drive BOOLEAN DEFAULT 0 NOT NULL")
            print("Column 'has_drive' added.")

        conn.commit()
        conn.close()
        print("Migration finished (SQLite).")
    except Exception as e:
         print(f"SQLite Migration Failed: {e}")

if __name__ == "__main__":
    migrate()
