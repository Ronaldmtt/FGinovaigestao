"""
Proposal PDF Service — Gera PDFs profissionais para propostas comerciais usando ReportLab.
"""
import os
from datetime import datetime


def gerar_pdf_proposta(proposal, lead):
    """
    Gera um PDF profissional para a proposta comercial.
    
    Args:
        proposal: Crm2Proposal instance
        lead: Crm2Lead instance
    
    Returns:
        str - Caminho relativo do PDF gerado, ou None se falhar
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm, mm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        
        # Garantir diretório
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'proposals')
        os.makedirs(base_dir, exist_ok=True)
        
        filename = f"proposta_{proposal.id}_{lead.id}.pdf"
        filepath = os.path.join(base_dir, filename)
        relative_path = f"static/proposals/{filename}"
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Cores
        primary = HexColor('#6366f1')
        dark = HexColor('#1e1b4b')
        gray = HexColor('#64748b')
        light_bg = HexColor('#f8fafc')
        
        # Estilos
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'ProposalTitle',
            parent=styles['Title'],
            fontSize=20,
            textColor=dark,
            spaceAfter=6*mm,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'ProposalSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=gray,
            alignment=TA_CENTER,
            spaceAfter=10*mm
        )
        
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=primary,
            spaceBefore=8*mm,
            spaceAfter=4*mm,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontSize=10,
            textColor=dark,
            spaceAfter=3*mm,
            alignment=TA_JUSTIFY,
            leading=14
        )
        
        small_style = ParagraphStyle(
            'SmallText',
            parent=styles['Normal'],
            fontSize=9,
            textColor=gray,
            alignment=TA_CENTER
        )
        
        # Construir elementos
        elements = []
        
        # Header
        elements.append(Spacer(1, 5*mm))
        elements.append(Paragraph("PROPOSTA COMERCIAL", title_style))
        
        today = datetime.now().strftime("%d/%m/%Y")
        elements.append(Paragraph(f"{lead.nome_empresa} — {today}", subtitle_style))
        
        # Linha decorativa
        elements.append(HRFlowable(width="100%", thickness=2, color=primary, spaceAfter=5*mm))
        
        # Info do Lead
        elements.append(Paragraph("DADOS DO CLIENTE", section_style))
        
        info_data = [
            ["Empresa:", lead.nome_empresa],
            ["Contato:", lead.nome_contato],
            ["Email:", lead.email or "—"],
            ["Telefone:", lead.telefone or "—"],
        ]
        
        info_table = Table(info_data, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), gray),
            ('TEXTCOLOR', (1, 0), (1, -1), dark),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(info_table)
        
        # Título da Proposta
        if proposal.titulo:
            elements.append(Paragraph("TÍTULO", section_style))
            elements.append(Paragraph(proposal.titulo, body_style))
        
        # Descrição
        if proposal.descricao:
            elements.append(Paragraph("DESCRIÇÃO", section_style))
            # Quebrar em parágrafos
            for para in proposal.descricao.split('\n'):
                if para.strip():
                    elements.append(Paragraph(para.strip(), body_style))
        
        # Escopo
        if proposal.escopo:
            elements.append(Paragraph("ESCOPO DO TRABALHO", section_style))
            for line in proposal.escopo.split('\n'):
                if line.strip():
                    elements.append(Paragraph(f"• {line.strip()}" if not line.strip().startswith('•') else line.strip(), body_style))
        
        # Valor e Prazo
        elements.append(Paragraph("INVESTIMENTO E PRAZO", section_style))
        
        valor_data = [
            ["Valor:", proposal.valor or "A definir"],
            ["Prazo:", proposal.prazo or "A definir"],
        ]
        
        valor_table = Table(valor_data, colWidths=[4*cm, 12*cm])
        valor_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), dark),
            ('TEXTCOLOR', (1, 0), (1, -1), primary),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (-1, -1), light_bg),
            ('BOX', (0, 0), (-1, -1), 1, primary),
        ]))
        elements.append(valor_table)
        
        # Cronograma
        if proposal.cronograma:
            elements.append(Paragraph("CRONOGRAMA", section_style))
            for line in proposal.cronograma.split('\n'):
                if line.strip():
                    elements.append(Paragraph(line.strip(), body_style))
        
        # Justificativa
        if proposal.justificativa:
            elements.append(Paragraph("JUSTIFICATIVA", section_style))
            for para in proposal.justificativa.split('\n'):
                if para.strip():
                    elements.append(Paragraph(para.strip(), body_style))
        
        # Rodapé
        elements.append(Spacer(1, 15*mm))
        elements.append(HRFlowable(width="100%", thickness=1, color=gray, spaceAfter=5*mm))
        elements.append(Paragraph(
            f"Proposta gerada em {today} | Válida por 30 dias | Ref: PROP-{proposal.id:04d}",
            small_style
        ))
        
        # Gerar PDF
        doc.build(elements)
        print(f"[proposal_pdf] PDF gerado: {filepath}")
        return relative_path
        
    except ImportError:
        print("[proposal_pdf] Pacote 'reportlab' não instalado.")
        return None
    except Exception as e:
        print(f"[proposal_pdf] Erro ao gerar PDF: {e}")
        return None


def gerar_pdf_contrato(contract, lead):
    """
    Gera um PDF profissional para o contrato.
    Sections são lidas do contract.sections_json (JSON array).
    
    Args:
        contract: Crm2Contract instance
        lead: Crm2Lead instance
    
    Returns:
        str - Caminho relativo do PDF gerado, ou None se falhar
    """
    try:
        import json
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm, mm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
        
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'contracts')
        os.makedirs(base_dir, exist_ok=True)
        
        filename = f"contrato_{contract.id}_{lead.id}.pdf"
        filepath = os.path.join(base_dir, filename)
        relative_path = f"static/contracts/{filename}"
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2*cm
        )
        
        # Cores
        dark = HexColor('#1e1b4b')
        gray = HexColor('#64748b')
        primary = HexColor('#1e3a5f')
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'ContractTitle',
            parent=styles['Title'],
            fontSize=18,
            textColor=dark,
            spaceAfter=4*mm,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'ContractSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=gray,
            alignment=TA_CENTER,
            spaceAfter=8*mm
        )
        
        clause_title_style = ParagraphStyle(
            'ClauseTitle',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=dark,
            spaceBefore=6*mm,
            spaceAfter=3*mm,
            fontName='Helvetica-Bold'
        )
        
        clause_body_style = ParagraphStyle(
            'ClauseBody',
            parent=styles['Normal'],
            fontSize=10,
            textColor=dark,
            spaceAfter=2*mm,
            alignment=TA_JUSTIFY,
            leading=14
        )
        
        small_style = ParagraphStyle(
            'SmallText',
            parent=styles['Normal'],
            fontSize=9,
            textColor=gray,
            alignment=TA_CENTER
        )
        
        signature_style = ParagraphStyle(
            'Signature',
            parent=styles['Normal'],
            fontSize=10,
            textColor=dark,
            alignment=TA_CENTER,
            spaceBefore=3*mm
        )
        
        # Construir elementos
        elements = []
        
        # Header
        elements.append(Spacer(1, 3*mm))
        elements.append(Paragraph(contract.titulo or "CONTRATO DE PRESTAÇÃO DE SERVIÇOS", title_style))
        
        today = datetime.now().strftime("%d/%m/%Y")
        elements.append(Paragraph(f"{lead.nome_empresa} — {today}", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=2, color=HexColor('#1e3a5f'), spaceAfter=5*mm))
        
        # Seções dinâmicas
        sections = []
        if contract.sections_json:
            try:
                sections = json.loads(contract.sections_json)
            except:
                sections = []
        
        for section in sections:
            s_type = section.get('type', 'description')
            s_content = section.get('content', '')
            if not s_content:
                continue
            
            if s_type == 'title':
                elements.append(Paragraph(s_content.upper(), clause_title_style))
            else:
                elements.append(Paragraph(s_content, clause_body_style))
        
        # Bloco de assinatura
        elements.append(Spacer(1, 20*mm))
        elements.append(HRFlowable(width="100%", thickness=1, color=gray, spaceAfter=10*mm))
        
        elements.append(Paragraph("LOCAL E DATA", clause_title_style))
        elements.append(Paragraph(f"__________________, {today}", clause_body_style))
        elements.append(Spacer(1, 15*mm))
        
        # Assinatura CONTRATANTE
        elements.append(Paragraph("_" * 50, signature_style))
        elements.append(Paragraph(f"<b>CONTRATANTE:</b> {lead.nome_empresa}", signature_style))
        elements.append(Paragraph(f"{lead.nome_contato}", signature_style))
        
        elements.append(Spacer(1, 12*mm))
        
        # Assinatura CONTRATADA
        elements.append(Paragraph("_" * 50, signature_style))
        elements.append(Paragraph("<b>CONTRATADA</b>", signature_style))
        
        # Rodapé
        elements.append(Spacer(1, 15*mm))
        elements.append(HRFlowable(width="100%", thickness=1, color=gray, spaceAfter=3*mm))
        elements.append(Paragraph(
            f"Contrato gerado em {today} | Ref: CONTR-{contract.id:04d}",
            small_style
        ))
        
        doc.build(elements)
        print(f"[contract_pdf] PDF gerado: {filepath}")
        return relative_path
        
    except ImportError:
        print("[contract_pdf] Pacote 'reportlab' não instalado.")
        return None
    except Exception as e:
        print(f"[contract_pdf] Erro ao gerar PDF do contrato: {e}")
        return None

