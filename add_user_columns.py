from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # PostgreSQL syntax for adding columns
        print("Adicionando coluna 'ativo'...")
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN ativo BOOLEAN NOT NULL DEFAULT TRUE'))
        db.session.commit()
        print("Coluna 'ativo' adicionada com sucesso.")
    except Exception as e:
        db.session.rollback()
        print(f"Aviso ao adicionar 'ativo': {e}")
        
    try:
        print("Adicionando coluna 'ultimo_acesso'...")
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN ultimo_acesso TIMESTAMP'))
        db.session.commit()
        print("Coluna 'ultimo_acesso' adicionada com sucesso.")
    except Exception as e:
        db.session.rollback()
        print(f"Aviso ao adicionar 'ultimo_acesso': {e}")
        
    print("Migrações concluídas.")
