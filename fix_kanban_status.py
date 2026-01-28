import sqlite3
import os

db_path = os.path.join('instance', 'database.db')
print(f"Fixing database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Set show_in_kanban = 0 (False) for all completed projects
    cursor.execute("UPDATE project SET show_in_kanban = 0 WHERE status = 'concluido'")
    affected = cursor.rowcount
    
    conn.commit()
    print(f"Fix successful. Updated {affected} projects.")
        
    conn.close()
except Exception as e:
    print(f"Error during fix: {e}")
