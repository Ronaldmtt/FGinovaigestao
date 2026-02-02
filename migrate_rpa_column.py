import os
import sqlite3
import psycopg2
from urllib.parse import urlparse

# Tentar pegar URL do PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')

def migrate_sqlite():
    print("--- Migrando SQLite ---")
    db_path = os.path.join('instance', 'database.db')
    if not os.path.exists(db_path):
        print(f"Banco SQLite não encontrado em: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se coluna existe
        cursor.execute("PRAGMA table_info(project)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'rpa_identifier' not in columns:
            print("Adicionando coluna rpa_identifier...")
            cursor.execute("ALTER TABLE project ADD COLUMN rpa_identifier TEXT")
            conn.commit()
            print("Coluna adicionada com sucesso.")
        else:
            print("Coluna rpa_identifier já existe.")
            
        conn.close()
    except Exception as e:
        print(f"Erro no SQLite: {e}")

def migrate_postgres():
    print("\n--- Migrando PostgreSQL ---")
    if not DATABASE_URL or 'sqlite' in DATABASE_URL:
        print("DATABASE_URL não configurada ou é SQLite. Pulando PostgreSQL.")
        return

    try:
        result = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Verificar se coluna existe
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='project' AND column_name='rpa_identifier'")
        if not cursor.fetchone():
            print("Adicionando coluna rpa_identifier...")
            cursor.execute("ALTER TABLE project ADD COLUMN rpa_identifier VARCHAR(100)")
            print("Coluna adicionada com sucesso.")
        else:
            print("Coluna rpa_identifier já existe.")

        conn.close()
    except Exception as e:
        print(f"Erro no PostgreSQL: {e}")

if __name__ == "__main__":
    migrate_sqlite()
    migrate_postgres()
