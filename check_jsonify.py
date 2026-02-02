
filename = 'routes.py'
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'jsonify' in line and ('project' in line or 'data' in line):
        print(f"Line {i+1}: {line.strip()}")
        # Check surrounding lines for @app.route
        for offset in range(1, 10):
            if i - offset >= 0:
                prev_line = lines[i - offset]
                if '@app.route' in prev_line:
                    print(f"  Route: {prev_line.strip()}")
                    break
