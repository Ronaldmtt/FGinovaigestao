from app import app, db
from sqlalchemy import text, MetaData
from datetime import datetime

def test_insert():
    with app.app_context():
        # Clean
        db.drop_all()
        db.create_all()
        
        metadata = MetaData()
        metadata.reflect(bind=db.engine)
        user_table = metadata.tables.get('user')
        
        row_dict = {
            'id': '1', 
            'nome': 'Administrador', 
            'sobrenome': 'Sistema', 
            'email': 'admin@inovaigestao.com.br', 
            'password_hash': 'scrypt:32768:8:1$kY...', 
            'is_admin': True, 
            'created_at': '2025-10-13 16:41:46.685397', 
            'reset_token': None, 
            'reset_token_expires': None,
            'acesso_clientes': True,
            'acesso_projetos': True,
            'acesso_tarefas': True,
            'acesso_kanban': True,
            'acesso_crm': True,
            'receber_notificacoes': True
        }
        
        print("Attempting insert...")
        try:
            db.session.execute(user_table.insert(), [row_dict])
            db.session.commit()
            print("Insert SUCCESS")
        except Exception as e:
            print(f"Insert FAILED: {repr(e)}")
            # import traceback
            # traceback.print_exc()

if __name__ == "__main__":
    test_insert()
