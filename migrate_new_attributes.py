import sqlite3
import os

DB_PATH = 'instance/database.db'

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. Add columns to Project table
        print("Checking Project table columns...")
        cursor.execute("PRAGMA table_info(project)")
        columns = [info[1] for info in cursor.fetchall()]

        if 'has_env' not in columns:
            print("Adding has_env column...")
            cursor.execute("ALTER TABLE project ADD COLUMN has_env BOOLEAN DEFAULT 0")
        else:
            print("has_env already exists.")

        if 'has_backup_db' not in columns:
            print("Adding has_backup_db column...")
            cursor.execute("ALTER TABLE project ADD COLUMN has_backup_db BOOLEAN DEFAULT 0")
        else:
            print("has_backup_db already exists.")

        # 2. Add new File Categories
        print("Checking File Categories...")
        # Get max order
        cursor.execute("SELECT MAX(ordem) FROM file_categories")
        result = cursor.fetchone()
        max_order = result[0] if result and result[0] is not None else 0
        
        new_categories = [
            {'nome': '.ENV', 'icone': 'fa-file-code', 'cor': '#fbbf24'}, # Amber for env
            {'nome': 'BACKUP BANCO DE DADOS', 'icone': 'fa-database', 'cor': '#ef4444'} # Red/Danger for backup
        ]

        for cat in new_categories:
            cursor.execute("SELECT id FROM file_categories WHERE nome = ?", (cat['nome'],))
            exists = cursor.fetchone()
            if not exists:
                max_order += 1
                print(f"Adding category: {cat['nome']}")
                cursor.execute(
                    "INSERT INTO file_categories (nome, icone, cor, ordem) VALUES (?, ?, ?, ?)",
                    (cat['nome'], cat['icone'], cat['cor'], max_order)
                )
            else:
                print(f"Category {cat['nome']} already exists.")

        conn.commit()
        print("Migration and seeding completed successfully.")

    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
