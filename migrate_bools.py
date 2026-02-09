
import sqlite3
import traceback
import os
import re

DB_PATH = r'C:/Users/User/projetos antigravity/FGinovaigestao/instance/database.db'

def run():
    print(f"Checking DB at: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("DB File NOT FOUND at absolute path!")
        # Try relative
        rel_path = 'instance/database.db'
        if os.path.exists(rel_path):
            print(f"Found relative: {rel_path}")
            db_file = rel_path
        else:
            print("DB not found.")
            return
    else:
        db_file = DB_PATH

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # Check columns
        c.execute("PRAGMA table_info(project)")
        cols = c.fetchall()
        
        has_env_col = next((x for x in cols if x[1] == 'has_env'), None)
        has_backup_col = next((x for x in cols if x[1] == 'has_backup_db'), None)
        
        needed = False
        if has_env_col:
            print(f"Current has_env: {has_env_col}")
            if has_env_col[3] != 0: # notnull != 0 means it is NOT NULL
                needed = True
        
        if not needed and has_env_col:
             print("has_env is already nullable.")
        
        if has_backup_col:
             if has_backup_col[3] != 0:
                 needed = True

        if not needed:
            print("Migration not needed or columns missing.")
            # Verify if columns exist
            if not has_env_col or not has_backup_col:
                print("Columns missing from table!")
            conn.close()
            return

        print("Starting migration...")
        
        # 1. Rename
        c.execute("DROP TABLE IF EXISTS project_backup_raw")
        c.execute("ALTER TABLE project RENAME TO project_backup_raw")
        
        # 2. Get SQL
        c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='project_backup_raw'")
        original_sql = c.fetchone()[0]
        
        # 3. Regex replace
        # Replace "has_env BOOLEAN NOT NULL" -> "has_env BOOLEAN"
        # Be loose on type mapping.
        
        new_sql = original_sql.replace("project_backup_raw", "project")
        
        # Regex: find column def and remove NOT NULL
        # pattern: (name\s+type)\s+NOT\s+NULL
        
        new_sql = re.sub(r'(has_env\s+[\w\(\)]+)\s+NOT\s+NULL', r'\1', new_sql, flags=re.IGNORECASE)
        new_sql = re.sub(r'(has_backup_db\s+[\w\(\)]+)\s+NOT\s+NULL', r'\1', new_sql, flags=re.IGNORECASE)
        
        # Also fix any "DEFAULT 0" or similar if we want to change default?
        # For now keeping default is fine, as long as it accepts NULL.
        # Assuming removing NOT NULL is sufficient.
        
        print("Creating new table...")
        c.execute(new_sql)
        
        # 4. Copy data
        print("Copying data...")
        c.execute("INSERT INTO project SELECT * FROM project_backup_raw")
        
        conn.commit()
        print("Migration COMPLETED SUCCESSFULLY.")
        conn.close()
        
    except Exception:
        print("CRITICAL ERROR IN MIGRATION:")
        print(traceback.format_exc())

if __name__ == "__main__":
    run()
