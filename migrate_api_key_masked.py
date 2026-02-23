"""
Migração: Ampliar coluna api_key_masked de VARCHAR(50) para VARCHAR(200)
Motivo: Chaves OpenAI (sk-proj-...) têm ~100 chars e o mascaramento excedia o limite.

Execute: python migrate_api_key_masked.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não encontrado no .env")

import psycopg2

def run_migration():
    print(f"Conectando ao banco...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        # Verifica tipo atual da coluna
        cur.execute("""
            SELECT character_maximum_length
            FROM information_schema.columns
            WHERE table_name = 'project_api_credentials'
              AND column_name = 'api_key_masked';
        """)
        row = cur.fetchone()
        if not row:
            print("ERRO: Coluna api_key_masked não encontrada!")
            return

        current_limit = row[0]
        print(f"Tamanho atual da coluna api_key_masked: VARCHAR({current_limit})")

        if current_limit is not None and current_limit >= 200:
            print("Coluna já tem tamanho adequado (>= 200). Nenhuma alteração necessária.")
            return

        print("Alterando coluna api_key_masked para VARCHAR(200)...")
        cur.execute("""
            ALTER TABLE project_api_credentials
            ALTER COLUMN api_key_masked TYPE character varying(200);
        """)
        conn.commit()
        print("✅ Migração aplicada com sucesso! Coluna alterada para VARCHAR(200).")

    except Exception as e:
        conn.rollback()
        print(f"❌ Erro na migração: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    run_migration()
