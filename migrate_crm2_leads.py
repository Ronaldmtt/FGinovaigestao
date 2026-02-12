"""
Migration: Copiar contatos existentes do CRM 1 para a nova tabela crm2_leads.
Os contatos são copiados com estagio='Lead' para ficarem disponíveis na aba Leads do CRM 2.
"""
from app import app
from extensions import db
from models import Contato, Crm2Lead

def migrate():
    with app.app_context():
        # Criar tabela se não existir
        db.create_all()
        
        # Verificar quantos leads já existem
        existing = Crm2Lead.query.count()
        if existing > 0:
            print(f"Tabela crm2_leads já possui {existing} registros. Pulando migração.")
            return
        
        # Buscar todos os contatos do CRM 1
        contatos = Contato.query.all()
        print(f"Encontrados {len(contatos)} contatos no CRM 1.")
        
        count = 0
        for c in contatos:
            lead = Crm2Lead(
                nome_empresa=c.nome_empresa,
                nome_contato=c.nome_contato,
                email=c.email or '',
                telefone=c.telefone or '',
                estagio='Lead',  # Todos entram como 'Lead' no CRM 2
                data_criacao=c.data_criacao,
                data_atualizacao=c.data_atualizacao
            )
            db.session.add(lead)
            count += 1
        
        db.session.commit()
        print(f"Migração concluída! {count} contatos copiados para crm2_leads como 'Lead'.")

if __name__ == '__main__':
    migrate()
