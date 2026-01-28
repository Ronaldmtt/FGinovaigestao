import re

sql_file = r"C:\Users\User\projetos antigravity\FGinovaigestao\backup_producao_inovaigestao (3).sql"

with open(sql_file, 'r', encoding='utf8') as f:
    for line in f:
        line = line.strip()
        if "COPY public." in line:
            print(f"Checking line: {line}")
            match = re.match(r'COPY public\.([^\s(]+)\s*\((.*?)\) FROM stdin;', line)
            if match:
                raw = match.group(1)
                clean = raw.replace('"', '')
                print(f"MATCHED: raw='{raw}', clean='{clean}'")
            else:
                print("NO MATCH")
