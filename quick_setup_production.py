#!/usr/bin/env python3
"""
Setup rápido para produção - Execute este arquivo na produção
"""

import os
from werkzeug.security import generate_password_hash

def setup_production_data():
    """Setup básico dos dados essenciais"""
    
    print("🚀 Setup rápido da produção...")
    
    # Instruções SQL para executar manualmente
    sql_commands = """
-- 1. Criar usuários essenciais
INSERT INTO "user" (nome, sobrenome, email, password_hash, is_admin, created_at) VALUES
('Administrador', 'Sistema', 'admin@sistema.com', '{admin_hash}', true, NOW()),
('felipe', 'gomes', 'felipe@inovailab.com', '{user_hash}', false, NOW()),
('vitor', 'gomes', 'vitor@inovailab.com', '{user_hash}', false, NOW())
ON CONFLICT (email) DO NOTHING;

-- 2. Criar cliente principal
INSERT INTO client (nome, email, telefone, endereco, public_code, created_at, creator_id) VALUES
('Sá Cavalcante', 'sa@sacavalcante.com.br', '', '', '76GMPAFU', NOW(), 
 (SELECT id FROM "user" WHERE email = 'admin@sistema.com'))
ON CONFLICT DO NOTHING;

-- 3. Criar projeto exemplo
INSERT INTO project (nome, client_id, responsible_id, status, descricao_resumida, created_at) VALUES
('RPA de Conciliação de Shoppings', 
 (SELECT id FROM client WHERE nome = 'Sá Cavalcante'),
 (SELECT id FROM "user" WHERE email = 'felipe@inovailab.com'),
 'em_andamento',
 'Sistema de automação para conciliação de dados financeiros dos shoppings',
 NOW())
ON CONFLICT DO NOTHING;
    """.format(
        admin_hash=generate_password_hash('admin123'),
        user_hash=generate_password_hash('temp123')
    )
    
    print("📋 Execute os seguintes comandos SQL na sua base de produção:")
    print("="*60)
    print(sql_commands)
    print("="*60)
    print("\n🔑 Credenciais após execução:")
    print("   Admin: admin@sistema.com / admin123") 
    print("   Felipe: felipe@inovailab.com / temp123")
    print("   Vitor: vitor@inovailab.com / temp123")
    print("\n⚠️  ALTERE AS SENHAS após fazer login!")

if __name__ == "__main__":
    setup_production_data()