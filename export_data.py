#!/usr/bin/env python3
"""
Script para EXPORTAR dados do banco de desenvolvimento
Execute este script no ambiente de desenvolvimento
"""

import json
import os
from datetime import datetime
from app import app
from extensions import db
from models import User, Client, Project, Task, TodoItem

def export_database_data():
    """Exporta todos os dados do banco para um arquivo JSON"""
    
    print("📤 Exportando dados do banco de desenvolvimento...")
    
    with app.app_context():
        try:
            export_data = {
                'export_date': datetime.now().isoformat(),
                'users': [],
                'clients': [],
                'projects': [],
                'tasks': [],
                'todos': []
            }
            
            # 1. EXPORTAR USUÁRIOS
            print("👥 Exportando usuários...")
            users = User.query.all()
            for user in users:
                export_data['users'].append({
                    'id': user.id,
                    'nome': user.nome,
                    'sobrenome': user.sobrenome,
                    'email': user.email,
                    'password_hash': user.password_hash,
                    'is_admin': user.is_admin,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                })
            print(f"   ✅ {len(users)} usuários exportados")
            
            # 2. EXPORTAR CLIENTES
            print("🏢 Exportando clientes...")
            clients = Client.query.all()
            for client in clients:
                export_data['clients'].append({
                    'id': client.id,
                    'nome': client.nome,
                    'email': client.email,
                    'telefone': client.telefone,
                    'endereco': client.endereco,
                    'public_code': client.public_code,
                    'creator_id': client.creator_id,
                    'created_at': client.created_at.isoformat() if client.created_at else None
                })
            print(f"   ✅ {len(clients)} clientes exportados")
            
            # 3. EXPORTAR PROJETOS
            print("📋 Exportando projetos...")
            projects = Project.query.all()
            for project in projects:
                # Exportar membros da equipe
                team_member_ids = [member.id for member in project.team_members]
                
                export_data['projects'].append({
                    'id': project.id,
                    'nome': project.nome,
                    'transcricao': project.transcricao,
                    'status': project.status,
                    'client_id': project.client_id,
                    'responsible_id': project.responsible_id,
                    'team_member_ids': team_member_ids,
                    'contexto_justificativa': project.contexto_justificativa,
                    'descricao_resumida': project.descricao_resumida,
                    'problema_oportunidade': project.problema_oportunidade,
                    'objetivos': project.objetivos,
                    'alinhamento_estrategico': project.alinhamento_estrategico,
                    'escopo_projeto': project.escopo_projeto,
                    'fora_escopo': project.fora_escopo,
                    'premissas': project.premissas,
                    'restricoes': project.restricoes,
                    'created_at': project.created_at.isoformat() if project.created_at else None
                })
            print(f"   ✅ {len(projects)} projetos exportados")
            
            # 4. EXPORTAR TAREFAS
            print("📝 Exportando tarefas...")
            tasks = Task.query.all()
            for task in tasks:
                export_data['tasks'].append({
                    'id': task.id,
                    'titulo': task.titulo,
                    'descricao': task.descricao,
                    'status': task.status,
                    'project_id': task.project_id,
                    'assigned_user_id': task.assigned_user_id,
                    'data_conclusao': task.data_conclusao.isoformat() if task.data_conclusao else None,
                    'created_at': task.created_at.isoformat() if task.created_at else None,
                    'completed_at': task.completed_at.isoformat() if task.completed_at else None
                })
            print(f"   ✅ {len(tasks)} tarefas exportadas")
            
            # 5. EXPORTAR TODOs
            print("✅ Exportando itens de ToDo...")
            todos = TodoItem.query.all()
            for todo in todos:
                export_data['todos'].append({
                    'id': todo.id,
                    'texto': todo.texto,
                    'completed': todo.completed,
                    'task_id': todo.task_id,
                    'created_at': todo.created_at.isoformat() if todo.created_at else None,
                    'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
                })
            print(f"   ✅ {len(todos)} itens de todo exportados")
            
            # SALVAR ARQUIVO
            filename = f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n🎉 Exportação concluída!")
            print(f"📁 Arquivo salvo: {filename}")
            print(f"📊 Resumo da exportação:")
            print(f"   - Usuários: {len(export_data['users'])}")
            print(f"   - Clientes: {len(export_data['clients'])}")
            print(f"   - Projetos: {len(export_data['projects'])}")
            print(f"   - Tarefas: {len(export_data['tasks'])}")
            print(f"   - ToDos: {len(export_data['todos'])}")
            
            return filename
            
        except Exception as e:
            print(f"❌ Erro na exportação: {e}")
            raise

if __name__ == "__main__":
    export_database_data()