
import os

routes_file = 'c:\\Users\\User\\projetos antigravity\\FGinovaigestao\\routes.py'

new_generate_pdf_code = """
@app.route('/reports/generate_pdf', methods=['GET', 'POST'])
@login_required
def generate_pdf():
    projects = []
    
    if request.method == 'POST':
        data = request.get_json()
        project_ids = data.get('project_ids', [])
        
        # Filtro de segurança: garantir que o usuário tem acesso a esses IDs
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
            return jsonify({'error': 'Nenhum projeto selecionado ou encontrado'}), 404
        flash('Nenhum projeto encontrado para gerar relatório.', 'warning')
        return redirect(url_for('reports'))

    # Configuração do PDF
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
        sintese = generate_project_report_summary(
            project.nome,
            project.descricao_resumida,
            project.problema_oportunidade,
            project.objetivos
        )
        
        # Tratamento básico de quebras de linha para o PDF
        sintese_pdf = sintese.replace('\\n', '<br/>')
        
        elements.append(Paragraph("RESUMO EXECUTIVO", label_style))
        elements.append(Paragraph(sintese_pdf, body_style))
        
        # Responsável (opcional, fora do texto da IA)
        if project.responsible:
             elements.append(Paragraph(f"<b>Responsável Técnico:</b> {project.responsible.full_name}", body_style))
            
        elements.append(PageBreak())
    
    if projects_processed == 0:
        if request.method == 'POST':
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
            return jsonify({'error': 'Erro interno ao gerar PDF'}), 500
        flash('Erro ao gerar arquivo PDF.', 'error')
        return redirect(url_for('reports'))
"""

# Read file lines
with open(routes_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Truncate at line 4153 (index 4152) because 4153 is where the function starts
# Checked via view_file: line 4153 is @app.route...
print(f"Total lines: {len(lines)}")
# Keep lines 0 to 4151 (so 4152 lines)
# Lines list is 0-indexed. Line 4153 is index 4152.
keep_lines = lines[:4152]

# Write back
with open(routes_file, 'w', encoding='utf-8') as f:
    f.writelines(keep_lines)
    f.write(new_generate_pdf_code)

print("routes.py definitely updated this time.")
