import os
import sqlite3
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

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
        
        # Obter colunas existentes
        cursor.execute("PRAGMA table_info(project)")
        columns = [info[1] for info in cursor.fetchall()]
        
        new_columns = {
            'has_github': 'BOOLEAN DEFAULT 0',
            'has_drive': 'BOOLEAN DEFAULT 0',
            'has_env': 'BOOLEAN DEFAULT 0',
            'has_backup_db': 'BOOLEAN DEFAULT 0',
            'rpa_identifier': 'TEXT'
        }

        for col, dtype in new_columns.items():
            if col not in columns:
                print(f"Adicionando coluna {col}...")
                cursor.execute(f"ALTER TABLE project ADD COLUMN {col} {dtype}")
                conn.commit()
                print(f"Coluna {col} adicionada.")
            else:
                print(f"Coluna {col} já existe.")
            
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

        new_columns = {
            'has_github': 'BOOLEAN DEFAULT FALSE',
            'has_drive': 'BOOLEAN DEFAULT FALSE',
            'has_env': 'BOOLEAN DEFAULT FALSE',
            'has_backup_db': 'BOOLEAN DEFAULT FALSE',
            'rpa_identifier': 'VARCHAR(100)'
        }

        for col, dtype in new_columns.items():
            # Verificar se coluna existe
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='project' AND column_name='{col}'")
            if not cursor.fetchone():
                print(f"Adicionando coluna {col}...")
                cursor.execute(f"ALTER TABLE project ADD COLUMN {col} {dtype}")
                print(f"Coluna {col} adicionada com sucesso.")
            else:
                print(f"Coluna {col} já existe.")

        conn.close()
    except Exception as e:
        print(f"Erro no PostgreSQL: {e}")

if __name__ == "__main__":
    migrate_sqlite()
    migrate_postgres()
