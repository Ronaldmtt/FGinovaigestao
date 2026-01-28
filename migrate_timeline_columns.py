import sqlite3
import os
from datetime import datetime

db_path = os.path.join('instance', 'database.db')
print(f"Migrating database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Add data_inicio column
    try:
        cursor.execute("ALTER TABLE project ADD COLUMN data_inicio DATE")
        print("Added column: data_inicio")
    except sqlite3.OperationalError as e:
        print(f"Column data_inicio might already exist: {e}")

    # 2. Add data_fim column
    try:
        cursor.execute("ALTER TABLE project ADD COLUMN data_fim DATE")
        print("Added column: data_fim")
    except sqlite3.OperationalError as e:
        print(f"Column data_fim might already exist: {e}")

    # 3. Set default data_inicio for existing projects ('2025-12-01')
    default_start_date = '2025-12-01'
    cursor.execute("UPDATE project SET data_inicio = ? WHERE data_inicio IS NULL", (default_start_date,))
    affected_start = cursor.rowcount
    print(f"Updated {affected_start} projects with default start date: {default_start_date}")

    conn.commit()
    conn.close()
    print("Migration completed successfully.")

except Exception as e:
    print(f"Error during migration: {e}")
