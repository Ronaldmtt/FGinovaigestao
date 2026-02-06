
import os
import sys

# Set explicit path
routes_file = 'c:\\Users\\User\\projetos antigravity\\FGinovaigestao\\routes.py'

print(f"Target file: {routes_file}")

# Try reading with different encodings
content_lines = []
encoding_used = 'utf-8'
try:
    with open(routes_file, 'r', encoding='utf-8') as f:
        content_lines = f.readlines()
except UnicodeDecodeError:
    print("UTF-8 read failed, trying latin-1")
    encoding_used = 'latin-1'
    with open(routes_file, 'r', encoding='latin-1') as f:
        content_lines = f.readlines()

print(f"Read {len(content_lines)} lines using {encoding_used} encoding.")

# Find the start of the old function to truncate
# We look for the specific decorator line
start_index = -1
target_line = "@app.route('/reports/generate_pdf')"

for i, line in enumerate(content_lines):
    if target_line in line and "methods" not in line: # Ensure we don't catch the fixed version if it was partially written
        start_index = i
        print(f"Found target start at line {i+1}: {line.strip()}")
        break

if start_index == -1:
    # Check if it's already fixed?
    for i, line in enumerate(content_lines):
         if "@app.route('/reports/generate_pdf', methods=['GET', 'POST'])" in line:
             print("File appears to be already fixed? Found correct decorator.")
             # We will overwrite anyway to be sure about the body and logs
             start_index = i
             print(f"Overwriting from line {i+1}")
             break

if start_index == -1:
    print("CRITICAL ERROR: Could not find the generate_pdf route definition. Aborting safely.")
    # Dump some lines to debug
    print("First 10 lines:", content_lines[:10])
    sys.exit(1)

# Keep everything before the function
lines_to_keep = content_lines[:start_index]

# New code with LOGGING
new_code_block = """@app.route('/reports/generate_pdf', methods=['GET', 'POST'])
@login_required
def generate_pdf():
    # Debug info for system logs (journalctl)
    print(f"DEBUG: generate_pdf called. Method: {request.method}, Args: {request.args}, User: {current_user.email}")
    
    projects = []
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(f"DEBUG: POST data received: {data}")
            project_ids = data.get('project_ids', [])
            
            if not project_ids:
                 print("DEBUG: No project_ids provided in POST")
                 projects = []
            else:
                # Security filter
                query = Project.query.filter(Project.id.in_(project_ids))
                
                if not current_user.is_admin:
                     query = query.filter(
                        (Project.responsible_id == current_user.id) |
                        (Project.team_members.contains(current_user))
                    )
                
                projects = query.join(Client).order_by(Client.nome, Project.nome).all()
                print(f"DEBUG: Found {len(projects)} projects from IDs: {project_ids}")
        except Exception as e:
            print(f"DEBUG: Error processing POST data: {e}")
            rpa_log.error(f"Erro processando POST relatorios: {str(e)}", regiao="relatorios")
            return jsonify({'error': 'Invalid JSON or data'}), 400
        
    else:
        # Fallback GET
        print("DEBUG: Processing GET request")
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
        print(f"DEBUG: Found {len(projects)} projects via GET filters")
    
    if not projects:
        if request.method == 'POST':
            return jsonify({'error': 'Nenhum projeto selecionado ou encontrado'}), 404
        flash('Nenhum projeto encontrado para gerar relatório.', 'warning')
        print("DEBUG: Redirecting due to no projects")
        return redirect(url_for('reports'))

    # Configuração do PDF
    try:
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
            # Dados mínimos
            has_data = project.descricao_resumida and project.problema_oportunidade and project.objetivos
            if not has_data:
                print(f"DEBUG: Skipping project {project.id} due to missing data")
                continue
                
            projects_processed += 1
                
            client_name = project.client.nome if project.client else "Cliente Desconhecido"
            project_name = project.nome
            
            elements.append(Paragraph(f"{client_name}", subtitle_style))
            elements.append(Paragraph(f"{project_name}", title_style))
            
            # AI Synthesis
            try:
                sintese = generate_project_report_summary(
                    project.nome,
                    project.descricao_resumida,
                    project.problema_oportunidade,
                    project.objetivos
                )
            except NameError:
                 sintese = f"{project.descricao_resumida}. {project.problema_oportunidade}. {project.objetivos}"
            except Exception as e:
                print(f"DEBUG: AI Error for project {project.id}: {e}")
                sintese = f"{project.descricao_resumida}. {project.problema_oportunidade}. {project.objetivos}"
            
            sintese_pdf = sintese.replace('\\n', '<br/>')
            
            elements.append(Paragraph("RESUMO EXECUTIVO", label_style))
            elements.append(Paragraph(sintese_pdf, body_style))
            
            if project.responsible:
                 elements.append(Paragraph(f"<b>Responsável Técnico:</b> {project.responsible.full_name}", body_style))
                
            elements.append(PageBreak())
        
        if projects_processed == 0:
            if request.method == 'POST':
                 return jsonify({'error': 'Nenhum dos projetos selecionados possui dados completos'}), 400
            flash('Nenhum projeto completo para gerar.', 'warning')
            return redirect(url_for('reports'))

        doc.build(elements)
        buffer.seek(0)
        filename = f"relatorio_projetos_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        print(f"DEBUG: Sending PDF {filename}")
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

    except Exception as e:
        print(f"DEBUG: Critical error generating PDF: {e}")
        rpa_log.error(f"Erro ao gerar PDF: {str(e)}", regiao="relatorios")
        if request.method == 'POST':
            return jsonify({'error': 'Erro interno ao gerar PDF'}), 500
        flash('Erro ao gerar arquivo PDF.', 'error')
        return redirect(url_for('reports'))
"""

# Write
with open(routes_file, 'w', encoding=encoding_used) as f:
    f.writelines(lines_to_keep)
    f.write(new_code_block)
    f.write('\n')

print("File written.")

# VERIFICATION
print("Verifying file content on disk...")
with open(routes_file, 'r', encoding=encoding_used) as f:
    verify_content = f.read()

if "methods=['GET', 'POST']" in verify_content:
    print("SUCCESS: POST method found in file.")
    if "DEBUG: generate_pdf called" in verify_content:
        print("SUCCESS: Debug logs found in file.")
    else:
        print("WARNING: Debug logs NOT found.")
else:
    print("FAILURE: POST method NOT found in file.")
    sys.exit(1)
