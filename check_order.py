import re

sql_file = r"C:\Users\User\projetos antigravity\FGinovaigestao\backup_producao_inovaigestao (3).sql"
print("Scanning for COPY statements...")
with open(sql_file, 'r', encoding='utf8') as f:
    for i, line in enumerate(f):
        if line.strip().startswith("COPY public."):
            print(f"Line {i+1}: {line.strip()}")
