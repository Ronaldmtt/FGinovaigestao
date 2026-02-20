"""
Migração: Adicionar colunas faltantes na tabela todo_item (PostgreSQL local)

Execute no servidor (ou localmente):
    python migrate_todoitem_columns.py
"""

import psycopg2
import os

# Conectar ao banco local
DB_URL = os.environ.get('DATABASE_URL', 'postgresql://gestao_user:Omega801@localhost/gestao_inovailab')
# Remover prefixo postgres:// se necessário
if DB_URL.startswith('postgres://'):
    DB_URL = DB_URL.replace('postgres://', 'postgresql://', 1)

print(f"Conectando a: {DB_URL}")

try:
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cursor = conn.cursor()

    print("\n=== Migração: todo_item - verificando colunas ===\n")

    # Verificar quais colunas já existem
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'todo_item'
        ORDER BY ordinal_position
    """)
    existing_cols = {row[0] for row in cursor.fetchall()}
    print(f"Colunas existentes: {sorted(existing_cols)}\n")

    migrations_applied = 0

    # 1. comentario (Text)
    if 'comentario' not in existing_cols:
        print("[ADD] Adicionando coluna 'comentario'...")
        cursor.execute("ALTER TABLE todo_item ADD COLUMN comentario TEXT")
        print("[OK] 'comentario' adicionada.")
        migrations_applied += 1
    else:
        print("[OK] 'comentario' já existe.")

    # 2. due_date (Date)
    if 'due_date' not in existing_cols:
        print("[ADD] Adicionando coluna 'due_date'...")
        cursor.execute("ALTER TABLE todo_item ADD COLUMN due_date DATE")
        print("[OK] 'due_date' adicionada.")
        migrations_applied += 1
    else:
        print("[OK] 'due_date' já existe.")

    # 3. completed_at (Timestamp)
    if 'completed_at' not in existing_cols:
        print("[ADD] Adicionando coluna 'completed_at'...")
        cursor.execute("ALTER TABLE todo_item ADD COLUMN completed_at TIMESTAMP")
        print("[OK] 'completed_at' adicionada.")
        migrations_applied += 1
    else:
        print("[OK] 'completed_at' já existe.")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n=== Migração concluída: {migrations_applied} coluna(s) adicionada(s) ===")
    if migrations_applied > 0:
        print("Reinicie o servidor para aplicar as mudanças.")
    else:
        print("Banco já estava atualizado. Cheque outras causas se o problema persistir.")

except Exception as e:
    print(f"\n[ERRO FATAL] {e}")
    raise
