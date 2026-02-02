import os
import psycopg2
from urllib.parse import urlparse

# Obter URL do banco da variável de ambiente
DATABASE_URL = os.getenv('DATABASE_URL')

def migrate_postgres():
    if not DATABASE_URL:
        print("Erro: DATABASE_URL não encontrada no ambiente.")
        return

    try:
        # Parse da URL para conexão com psycopg2
        result = urlparse(DATABASE_URL)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port
        
        print(f"Conectando ao banco {database} em {hostname}...")
        
        conn = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # 1. Adicionar colunas na tabela 'project'
        print("Verificando colunas na tabela 'project'...")
        
        # has_env
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='project' AND column_name='has_env'")
        if not cursor.fetchone():
            print("Adicionando coluna has_env...")
            cursor.execute("ALTER TABLE project ADD COLUMN has_env BOOLEAN DEFAULT FALSE NOT NULL")
        else:
            print("Coluna has_env já existe.")

        # has_backup_db
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='project' AND column_name='has_backup_db'")
        if not cursor.fetchone():
            print("Adicionando coluna has_backup_db...")
            cursor.execute("ALTER TABLE project ADD COLUMN has_backup_db BOOLEAN DEFAULT FALSE NOT NULL")
        else:
            print("Coluna has_backup_db já existe.")

        # 2. Adicionar novas categorias de arquivos
        print("Verificando categorias de arquivos...")
        
        new_categories = [
            {'nome': '.ENV', 'icone': 'fa-file-code', 'cor': '#fbbf24'}, 
            {'nome': 'BACKUP BANCO DE DADOS', 'icone': 'fa-database', 'cor': '#ef4444'}
        ]

        for cat in new_categories:
            cursor.execute("SELECT id FROM file_categories WHERE nome = %s", (cat['nome'],))
            exists = cursor.fetchone()
            
            if not exists:
                # Pegar próxima ordem
                cursor.execute("SELECT COALESCE(MAX(ordem), 0) + 1 FROM file_categories")
                next_order = cursor.fetchone()[0]
                
                print(f"Inserindo categoria: {cat['nome']}")
                cursor.execute(
                    "INSERT INTO file_categories (nome, icone, cor, ordem, created_at) VALUES (%s, %s, %s, %s, NOW())",
                    (cat['nome'], cat['icone'], cat['cor'], next_order)
                )
            else:
                print(f"Categoria {cat['nome']} já existe.")

        conn.close()
        print("\nMigração concluída com sucesso!")

    except Exception as e:
        print(f"\nErro durante a migração: {e}")

if __name__ == "__main__":
    migrate_postgres()
