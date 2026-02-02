
filename = 'routes.py'
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/data' in line and 'project' in line:
        print(f"Line {i+1}: {line.strip()}")
        # Print surrounding lines
        for j in range(max(0, i-2), min(len(lines), i+3)):
             print(f"  {j+1}: {lines[j].strip()}")
