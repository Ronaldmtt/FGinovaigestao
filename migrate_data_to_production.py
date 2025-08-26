#!/usr/bin/env python3
"""
Script para migrar dados do desenvolvimento para produção
Execute este script no ambiente de produção após o deploy
"""

import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Client, Project, Task, TodoItem

def migrate_data_to_production():
    """Migra dados essenciais para produção"""
    
    print("🔄 Iniciando migração de dados para produção...")
    
    with app.app_context():
        try:
            # 1. USUÁRIOS
            print("\n👥 Migrando usuários...")
            
            users_data = [
                {"nome": "Administrador", "sobrenome": "Sistema", "email": "admin@sistema.com", "is_admin": True, "password": "admin123"},
                {"nome": "felipe", "sobrenome": "gomes", "email": "felipe@inovailab.com", "is_admin": False, "password": "temp123"},
                {"nome": "aldo", "sobrenome": "lorenzo", "email": "aldo@inovailab.com", "is_admin": False, "password": "temp123"},
                {"nome": "vitor", "sobrenome": "gomes", "email": "vitor@inovailab.com", "is_admin": False, "password": "temp123"},
                {"nome": "Renan", "sobrenome": "Gomes", "email": "renan@inovailab.com", "is_admin": False, "password": "temp123"},
                {"nome": "Daniel", "sobrenome": "Libar", "email": "daniel@inovailab.com", "is_admin": False, "password": "temp123"},
            ]
            
            user_mapping = {}  # Para mapear emails para IDs
            
            for user_data in users_data:
                existing_user = User.query.filter_by(email=user_data["email"]).first()
                if not existing_user:
                    user = User(
                        nome=user_data["nome"],
                        sobrenome=user_data["sobrenome"],
                        email=user_data["email"],
                        password_hash=generate_password_hash(user_data["password"]),
                        is_admin=user_data["is_admin"]
                    )
                    db.session.add(user)
                    db.session.flush()  # Para obter o ID
                    user_mapping[user_data["email"]] = user.id
                    print(f"   ✅ Usuário criado: {user_data['email']}")
                else:
                    user_mapping[user_data["email"]] = existing_user.id
                    print(f"   ⚠️  Usuário já existe: {user_data['email']}")
            
            # 2. CLIENTES
            print("\n🏢 Migrando clientes...")
            
            clients_data = [
                {"nome": "Sá Cavalcante", "email": "sa@sacavalcante.com.br", "telefone": "", "endereco": "", "public_code": "76GMPAFU"},
                {"nome": "inovai.lab", "email": "inovai@inovailab.com", "telefone": "21971497710", "endereco": "Rua Major Rubens Vaz, 536, Gávea. ", "public_code": "1WNK9F97"},
                {"nome": "BoraBaila", "email": "borabailar@borabailar.com.br", "telefone": "2199999-8888", "endereco": "", "public_code": "II5Y8XAO"},
                {"nome": "AvSales-Aeropool", "email": "humberto@avsales.com", "telefone": "21999996565", "endereco": "Rua Major Rubens Vaz, 536", "public_code": ""},
            ]
            
            client_mapping = {}
            admin_id = user_mapping["admin@sistema.com"]
            
            for client_data in clients_data:
                existing_client = Client.query.filter_by(nome=client_data["nome"]).first()
                if not existing_client:
                    client = Client(
                        nome=client_data["nome"],
                        email=client_data["email"],
                        telefone=client_data["telefone"],
                        endereco=client_data["endereco"],
                        public_code=client_data["public_code"] if client_data["public_code"] else None,
                        creator_id=admin_id
                    )
                    db.session.add(client)
                    db.session.flush()
                    client_mapping[client_data["nome"]] = client.id
                    print(f"   ✅ Cliente criado: {client_data['nome']}")
                else:
                    client_mapping[client_data["nome"]] = existing_client.id
                    print(f"   ⚠️  Cliente já existe: {client_data['nome']}")
            
            # 3. PROJETOS (exemplos principais)
            print("\n📋 Migrando projetos principais...")
            
            projects_data = [
                {
                    "nome": "RPA de Conciliação de Shoppings",
                    "cliente": "Sá Cavalcante",
                    "responsavel": "felipe@inovailab.com",
                    "status": "em_andamento",
                    "descricao": "Sistema de automação para conciliação de dados financeiros dos shoppings"
                },
                {
                    "nome": "RPA de Faturamento Sá Cavalcante", 
                    "cliente": "Sá Cavalcante",
                    "responsavel": "felipe@inovailab.com",
                    "status": "em_andamento",
                    "descricao": "Automação do processo de faturamento"
                },
                {
                    "nome": "Conselheiro IA da Presidência",
                    "cliente": "Sá Cavalcante", 
                    "responsavel": "vitor@inovailab.com",
                    "status": "em_andamento",
                    "descricao": "Sistema de IA para apoio à tomada de decisões"
                }
            ]
            
            for project_data in projects_data:
                existing_project = Project.query.filter_by(nome=project_data["nome"]).first()
                if not existing_project:
                    project = Project(
                        nome=project_data["nome"],
                        client_id=client_mapping[project_data["cliente"]],
                        responsible_id=user_mapping[project_data["responsavel"]],
                        status=project_data["status"],
                        descricao_resumida=project_data["descricao"]
                    )
                    db.session.add(project)
                    print(f"   ✅ Projeto criado: {project_data['nome']}")
                else:
                    print(f"   ⚠️  Projeto já existe: {project_data['nome']}")
            
            db.session.commit()
            print("\n🎉 Migração concluída com sucesso!")
            
            # Estatísticas finais
            print(f"\n📊 Estatísticas finais:")
            print(f"   Usuários: {User.query.count()}")
            print(f"   Clientes: {Client.query.count()}")
            print(f"   Projetos: {Project.query.count()}")
            
            print(f"\n🔑 CREDENCIAIS IMPORTANTES:")
            print(f"   Admin: admin@sistema.com / admin123")
            print(f"   Outros usuários: [email] / temp123")
            print(f"\n⚠️  IMPORTANTE: Altere as senhas após o login!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro na migração: {e}")
            raise

if __name__ == "__main__":
    migrate_data_to_production()