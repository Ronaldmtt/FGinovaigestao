"""
Migração: adiciona coluna parent_id na tabela project para suporte a projetos vinculados.
Execute na VM: python add_project_parent.py
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL', '')
if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrada no .env")
    exit(1)

# Adaptar URL para psycopg2
if DATABASE_URL.startswith('postgresql+psycopg2://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql+psycopg2://', 'postgresql://')

print(f"Conectando ao banco de dados...")
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

# Verificar se a coluna já existe
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name = 'project' AND column_name = 'parent_id';
""")
exists = cur.fetchone()

if exists:
    print("✅ Coluna parent_id já existe na tabela project. Nada a fazer.")
else:
    print("➕ Adicionando coluna parent_id...")
    cur.execute("""
        ALTER TABLE project
        ADD COLUMN parent_id INTEGER REFERENCES project(id) ON DELETE SET NULL;
    """)
    print("✅ Coluna parent_id adicionada com sucesso!")

# Conferir resultado
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'project' AND column_name = 'parent_id';
""")
row = cur.fetchone()
if row:
    print(f"   → Coluna: {row[0]}, Tipo: {row[1]}, Nullable: {row[2]}")

cur.close()
conn.close()
print("\n✅ Migração concluída. Reinicie o gunicorn: sudo systemctl restart gunicorn")
