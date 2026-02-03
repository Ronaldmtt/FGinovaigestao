from app import app, db
from models import Project

with app.app_context():
    projects = Project.query.all()
    print("-" * 60)
    print(f"{'ID':<5} | {'Name':<30} | {'Desc. Len':<10} | {'Status'}")
    print("-" * 60)
    for p in projects:
        desc_len = len(p.descricao_resumida) if p.descricao_resumida else 0
        print(f"{p.id:<5} | {p.nome[:30]:<30} | {desc_len:<10} | {p.status}")
    print("-" * 60)
