import psycopg2
import os

# Connect to database using configuration from .env or default fallback
database_url = os.environ.get("DATABASE_URL", "postgresql://usuario:senha@localhost/gestao_inovailab")

# Basic parser if needed or directly pass it to psycopg2
print(f"Connecting to {database_url}...")
try:
    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Adicionando coluna 'ativo'
    try:
        cursor.execute('ALTER TABLE "user" ADD COLUMN ativo BOOLEAN NOT NULL DEFAULT TRUE;')
        print("Coluna 'ativo' adicionada com sucesso.")
    except Exception as e:
        print(f"Aviso ao adicionar 'ativo': {e}")
        
    # Adicionando coluna 'ultimo_acesso'
    try:
        cursor.execute('ALTER TABLE "user" ADD COLUMN ultimo_acesso TIMESTAMP;')
        print("Coluna 'ultimo_acesso' adicionada com sucesso.")
    except Exception as e:
        print(f"Aviso ao adicionar 'ultimo_acesso': {e}")

    cursor.close()
    conn.close()
    print("Migrações concluídas.")
except Exception as e:
    print(f"Error: {e}")
