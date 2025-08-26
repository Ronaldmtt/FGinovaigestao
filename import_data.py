#!/usr/bin/env python3
"""
Script para IMPORTAR dados para o banco de produção
Execute este script no ambiente de produção
"""

import json
import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Client, Project, Task, TodoItem, project_users

def import_database_data(filename=None):
    """Importa dados de um arquivo JSON para o banco"""
    
    if not filename:
        # Procurar pelo arquivo de export mais recente
        import glob
        files = glob.glob("database_export_*.json")
        if not files:
            print("❌ Nenhum arquivo de exportação encontrado!")
            print("💡 Execute primeiro o export_data.py no ambiente de desenvolvimento")
            return
        filename = max(files)  # Arquivo mais recente
    
    if not os.path.exists(filename):
        print(f"❌ Arquivo não encontrado: {filename}")
        return
    
    print(f"📥 Importando dados de: {filename}")
    
    with app.app_context():
        try:
            # Carregar dados do arquivo
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📅 Dados exportados em: {data['export_date']}")
            
            # Mapear IDs antigos para novos
            user_id_map = {}
            client_id_map = {}
            project_id_map = {}
            task_id_map = {}
            
            # 1. IMPORTAR USUÁRIOS
            print("\n👥 Importando usuários...")
            for user_data in data['users']:
                existing_user = User.query.filter_by(email=user_data['email']).first()
                if existing_user:
                    user_id_map[user_data['id']] = existing_user.id
                    print(f"   ⚠️  Usuário já existe: {user_data['email']}")
                else:
                    user = User(
                        nome=user_data['nome'],
                        sobrenome=user_data['sobrenome'],
                        email=user_data['email'],
                        password_hash=user_data['password_hash'],
                        is_admin=user_data['is_admin'],
                        created_at=datetime.fromisoformat(user_data['created_at']) if user_data['created_at'] else datetime.now()
                    )
                    db.session.add(user)
                    db.session.flush()  # Para obter o ID
                    user_id_map[user_data['id']] = user.id
                    print(f"   ✅ Usuário importado: {user_data['email']}")
            
            # 2. IMPORTAR CLIENTES
            print("\n🏢 Importando clientes...")
            for client_data in data['clients']:
                existing_client = Client.query.filter_by(nome=client_data['nome']).first()
                if existing_client:
                    client_id_map[client_data['id']] = existing_client.id
                    print(f"   ⚠️  Cliente já existe: {client_data['nome']}")
                else:
                    client = Client(
                        nome=client_data['nome'],
                        email=client_data['email'],
                        telefone=client_data['telefone'],
                        endereco=client_data['endereco'],
                        public_code=client_data['public_code'],
                        creator_id=user_id_map.get(client_data['creator_id'], 1),  # Default para admin
                        created_at=datetime.fromisoformat(client_data['created_at']) if client_data['created_at'] else datetime.now()
                    )
                    db.session.add(client)
                    db.session.flush()
                    client_id_map[client_data['id']] = client.id
                    print(f"   ✅ Cliente importado: {client_data['nome']}")
            
            # 3. IMPORTAR PROJETOS
            print("\n📋 Importando projetos...")
            for project_data in data['projects']:
                existing_project = Project.query.filter_by(nome=project_data['nome']).first()
                if existing_project:
                    project_id_map[project_data['id']] = existing_project.id
                    print(f"   ⚠️  Projeto já existe: {project_data['nome']}")
                else:
                    project = Project(
                        nome=project_data['nome'],
                        transcricao=project_data['transcricao'],
                        status=project_data['status'],
                        client_id=client_id_map.get(project_data['client_id']),
                        responsible_id=user_id_map.get(project_data['responsible_id']),
                        contexto_justificativa=project_data.get('contexto_justificativa'),
                        descricao_resumida=project_data.get('descricao_resumida'),
                        problema_oportunidade=project_data.get('problema_oportunidade'),
                        objetivos=project_data.get('objetivos'),
                        alinhamento_estrategico=project_data.get('alinhamento_estrategico'),
                        escopo_projeto=project_data.get('escopo_projeto'),
                        fora_escopo=project_data.get('fora_escopo'),
                        premissas=project_data.get('premissas'),
                        restricoes=project_data.get('restricoes'),
                        created_at=datetime.fromisoformat(project_data['created_at']) if project_data['created_at'] else datetime.now()
                    )
                    db.session.add(project)
                    db.session.flush()
                    project_id_map[project_data['id']] = project.id
                    
                    # Adicionar membros da equipe
                    for old_member_id in project_data.get('team_member_ids', []):
                        new_member_id = user_id_map.get(old_member_id)
                        if new_member_id:
                            member = User.query.get(new_member_id)
                            if member:
                                project.team_members.append(member)
                    
                    print(f"   ✅ Projeto importado: {project_data['nome']}")
            
            # 4. IMPORTAR TAREFAS
            print("\n📝 Importando tarefas...")
            for task_data in data['tasks']:
                project_id = project_id_map.get(task_data['project_id'])
                if not project_id:
                    print(f"   ⚠️  Projeto não encontrado para tarefa: {task_data['titulo']}")
                    continue
                    
                task = Task(
                    titulo=task_data['titulo'],
                    descricao=task_data['descricao'],
                    status=task_data['status'],
                    project_id=project_id,
                    assigned_user_id=user_id_map.get(task_data['assigned_user_id']) if task_data['assigned_user_id'] else None,
                    data_conclusao=datetime.fromisoformat(task_data['data_conclusao']).date() if task_data['data_conclusao'] else None,
                    created_at=datetime.fromisoformat(task_data['created_at']) if task_data['created_at'] else datetime.now(),
                    completed_at=datetime.fromisoformat(task_data['completed_at']) if task_data['completed_at'] else None
                )
                db.session.add(task)
                db.session.flush()
                task_id_map[task_data['id']] = task.id
                print(f"   ✅ Tarefa importada: {task_data['titulo']}")
            
            # 5. IMPORTAR TODOs
            print("\n✅ Importando itens de ToDo...")
            for todo_data in data['todos']:
                task_id = task_id_map.get(todo_data['task_id'])
                if not task_id:
                    print(f"   ⚠️  Tarefa não encontrada para todo: {todo_data['texto']}")
                    continue
                    
                todo = TodoItem(
                    texto=todo_data['texto'],
                    completed=todo_data['completed'],
                    task_id=task_id,
                    created_at=datetime.fromisoformat(todo_data['created_at']) if todo_data['created_at'] else datetime.now(),
                    completed_at=datetime.fromisoformat(todo_data['completed_at']) if todo_data['completed_at'] else None
                )
                db.session.add(todo)
                print(f"   ✅ Todo importado: {todo_data['texto'][:50]}...")
            
            # COMMIT FINAL
            db.session.commit()
            
            print(f"\n🎉 Importação concluída com sucesso!")
            print(f"📊 Estatísticas finais:")
            print(f"   - Usuários: {User.query.count()}")
            print(f"   - Clientes: {Client.query.count()}")
            print(f"   - Projetos: {Project.query.count()}")
            print(f"   - Tarefas: {Task.query.count()}")
            print(f"   - ToDos: {TodoItem.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro na importação: {e}")
            raise

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    import_database_data(filename)