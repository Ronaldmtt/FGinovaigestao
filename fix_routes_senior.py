
import os
import sys

path = r'c:\Users\User\projetos antigravity\FGinovaigestao\routes.py'

print(f"Reading {path}...")
try:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# Find cut index
cut_index = -1

# Strategy: Find "def generate_pdf():" and look backwards for the route decorator
for i in range(len(lines) - 1, -1, -1):
    if "def generate_pdf():" in lines[i]:
        # Found the function definition
        # Now look upwards for the @app.route
        # It should be within the last 5 lines before this
        for j in range(1, 6):
            if i - j >= 0:
                if "@app.route" in lines[i-j] and "generate_pdf" in lines[i-j]:
                    cut_index = i - j
                    print(f"Found cut point at line {cut_index + 1}: {lines[cut_index].strip()}")
                    break
        if cut_index != -1:
            break

if cut_index == -1:
    print("Could not find the function start. Dumping last 10 lines for debug:")
    for l in lines[-10:]:
        print(repr(l))
    sys.exit(1)

# Full new code block
new_code = """@app.route('/reports/generate_pdf', methods=['GET', 'POST'])
@login_required
def generate_pdf():
    projects = []
    
    if request.method == 'POST':
        data = request.get_json()
        project_ids = data.get('project_ids', [])
        
        # Filtro de segurança: garantir que o usuário tem acesso a esses IDs
        if not project_ids:
             projects = []
        else:
            query = Project.query.filter(Project.id.in_(project_ids))
            
            if not current_user.is_admin:
                 query = query.filter(
                    (Project.responsible_id == current_user.id) |
                    (Project.team_members.contains(current_user))
                )
            
            # Manter a ordem dos IDs selecionados se possível, ou ordenar alfabeticamente
            projects = query.join(Client).order_by(Client.nome, Project.nome).all()
        
    else:
        # Fallback para GET (filtros antigos ou geração direta)
        project_id = request.args.get('project_id')
        client_id = request.args.get('client_id')
        user_id = request.args.get('user_id')
        
        query = Project.query.join(Client)
        
        if project_id:
            query = query.filter(Project.id == project_id)
        if client_id:
            query = query.filter(Project.client_id == client_id)
        if user_id:
            query = query.filter(Project.responsible_id == user_id)
            
        if not current_user.is_admin:
             query = query.filter(
                (Project.responsible_id == current_user.id) |
                (Project.team_members.contains(current_user))
            )
             
        projects = query.order_by(Client.nome, Project.nome).all()
    
    if not projects:
        if request.method == 'POST':
            from flask import jsonify
            return jsonify({'error': 'Nenhum projeto selecionado ou encontrado'}), 404
        flash('Nenhum projeto encontrado para gerar relatório.', 'warning')
        return redirect(url_for('reports'))

    # Configuração do PDF
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from io import BytesIO
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=10,
        textColor=colors.HexColor('#2c3e50')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=20,
        textColor=colors.HexColor('#7f8c8d')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=15,
        alignment=4 # Justified
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#95a5a6'),
        spaceAfter=2
    )

    projects_processed = 0
    
    for project in projects:
        # Verificar dados mínimos
        has_data = project.descricao_resumida and project.problema_oportunidade and project.objetivos
        if not has_data:
            continue
            
        projects_processed += 1
            
        # Header: Cliente | Projeto
        client_name = project.client.nome if project.client else "Cliente Desconhecido"
        project_name = project.nome
        
        elements.append(Paragraph(f"{client_name}", subtitle_style))
        elements.append(Paragraph(f"{project_name}", title_style))
        
        # Gerar Síntese com IA
        # Aqui chamamos o serviço de IA para reescrever os campos
        try:
            sintese = generate_project_report_summary(
                project.nome,
                project.descricao_resumida,
                project.problema_oportunidade,
                project.objetivos
            )
        except NameError:
             # Fallback caso a função não importada
             sintese = f"{project.descricao_resumida}. {project.problema_oportunidade}. {project.objetivos}"
        
        # Tratamento básico de quebras de linha para o PDF
        if sintese:
            sintese_pdf = sintese.replace('\\n', '<br/>')
        else:
            sintese_pdf = "Sem resumo disponível."
        
        elements.append(Paragraph("RESUMO EXECUTIVO", label_style))
        elements.append(Paragraph(sintese_pdf, body_style))
        
        # Responsável (opcional)
        if project.responsible:
             elements.append(Paragraph(f"<b>Responsável Técnico:</b> {project.responsible.full_name}", body_style))
            
        elements.append(PageBreak())
    
    if projects_processed == 0:
        if request.method == 'POST':
             from flask import jsonify
             return jsonify({'error': 'Nenhum dos projetos selecionados possui dados completos'}), 400
        flash('Nenhum projeto completo para gerar.', 'warning')
        return redirect(url_for('reports'))

    try:
        doc.build(elements)
        buffer.seek(0)
        filename = f"relatorio_projetos_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')
    except Exception as e:
        rpa_log.error(f"Erro ao gerar PDF: {str(e)}", regiao="relatorios")
        if request.method == 'POST':
            from flask import jsonify
            return jsonify({'error': 'Erro interno ao gerar PDF'}), 500
        flash('Erro ao gerar arquivo PDF.', 'error')
        return redirect(url_for('reports'))
"""

# Construct new content
# Keep lines up to cut_index
final_lines = lines[:cut_index]
# Ensure we end with a newline before appending
if final_lines and not final_lines[-1].endswith('\n'):
    final_lines[-1] += '\n'

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)
    f.write(new_code)
    f.write('\n')

print("Routes.py rewritten successfully.")

# Self-verification
with open(path, 'r', encoding='utf-8') as f:
    verify_content = f.read()

if "methods=['GET', 'POST']" in verify_content:
    print("VERIFICATION PASS: POST method is present.")
else:
    print("VERIFICATION FAIL: POST method NOT found.")
    sys.exit(1)
