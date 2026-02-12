"""
AI Analysis Service — Análise de transcrições usando OpenAI.
Gera overview, itens da pauta, notas e ações sugeridas.
"""
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def analisar_transcricao(transcription_text):
    """
    Gera análise estruturada de uma transcrição de reunião usando OpenAI.
    
    Args:
        transcription_text: str - Texto completo da transcrição
    
    Returns:
        str - Análise formatada em markdown, ou None se falhar
    """
    if not OPENAI_API_KEY:
        print("[ai_analysis] OPENAI_API_KEY não configurada")
        return None
    
    if not transcription_text or len(transcription_text.strip()) < 50:
        print("[ai_analysis] Transcrição muito curta para análise")
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = (
            "Você é um analista sênior de negócios. Analise a transcrição da reunião abaixo e gere um relatório "
            "estruturado em português do Brasil. O relatório deve conter:\n\n"
            "## Overview\n"
            "Resumo dos principais pontos abordados na reunião.\n\n"
            "## Itens da Pauta\n"
            "Liste os tópicos discutidos.\n\n"
            "## Notas Importantes\n"
            "Pontos-chave, decisões tomadas e acordos.\n\n"
            "## Ações Sugeridas\n"
            "Próximos passos e tarefas com responsáveis, quando mencionados.\n\n"
            "---\n\n"
            f"Transcrição:\n{transcription_text}"
        )
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Você é um analista sênior. Responda em português do Brasil. Use formato markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        analysis = response.choices[0].message.content
        print(f"[ai_analysis] Análise gerada com sucesso ({len(analysis)} chars)")
        return analysis
        
    except ImportError:
        print("[ai_analysis] Pacote 'openai' não instalado. Use: pip install openai")
        return None
    except Exception as e:
        print(f"[ai_analysis] Erro ao gerar análise: {e}")
        return None


def gerar_proposta_ia(lead_nome, lead_empresa, observacoes, reunioes_data):
    """
    Gera campos estruturados para uma proposta comercial com base em todo o histórico do lead.
    
    Args:
        lead_nome: str - Nome do contato
        lead_empresa: str - Nome da empresa
        observacoes: str - Observações do lead
        reunioes_data: list[dict] - Lista com {titulo, transcricao, analise, pauta} de cada reunião
    
    Returns:
        dict - Campos da proposta {titulo, descricao, escopo, valor_sugerido, prazo, cronograma, justificativa}
        ou None se falhar
    """
    if not OPENAI_API_KEY:
        print("[ai_analysis] OPENAI_API_KEY não configurada")
        return None
    
    # Montar contexto completo
    context_parts = [f"Empresa: {lead_empresa}", f"Contato: {lead_nome}"]
    
    if observacoes:
        context_parts.append(f"\n--- OBSERVAÇÕES DO LEAD ---\n{observacoes}")
    
    for i, r in enumerate(reunioes_data, 1):
        context_parts.append(f"\n--- REUNIÃO {i}: {r.get('titulo', '')} ---")
        if r.get('pauta'):
            context_parts.append(f"Pauta: {r['pauta']}")
        if r.get('transcricao'):
            context_parts.append(f"Transcrição:\n{r['transcricao'][:3000]}")
        if r.get('analise'):
            context_parts.append(f"Análise:\n{r['analise'][:2000]}")
    
    full_context = "\n".join(context_parts)
    
    try:
        import json
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = (
            "Com base em todo o histórico de reuniões e informações desse lead abaixo, "
            "gere uma proposta comercial estruturada em JSON com os seguintes campos:\n\n"
            "- titulo: Título da proposta (ex: 'Proposta de Desenvolvimento de Sistema para [Empresa]')\n"
            "- descricao: Descrição detalhada do que será entregue\n"
            "- escopo: Escopo do trabalho / serviços incluídos\n"
            "- valor_sugerido: Valor sugerido (formato: 'R$ X.XXX,XX')\n"
            "- prazo: Prazo estimado de entrega (ex: '45 dias úteis')\n"
            "- cronograma: Cronograma dividido em fases/etapas\n"
            "- justificativa: Justificativa da proposta com base nas necessidades identificadas nas reuniões\n\n"
            "IMPORTANTE: Considere que nosso time é capaz e ágil, mas a proposta deve refletir um cronograma "
            "profissional e realista para o cliente. NÃO subestime o valor do trabalho.\n"
            "Responda APENAS com o JSON válido, sem texto adicional.\n\n"
            f"Dados do lead:\n{full_context}"
        )
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Você é um consultor de negócios sênior. Gere propostas em português do Brasil. Responda APENAS em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2500
        )
        
        content = response.choices[0].message.content.strip()
        # Limpar possíveis marcadores de código
        if content.startswith("```"):
            content = content.split("\n", 1)[1] if "\n" in content else content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        result = json.loads(content)
        print(f"[ai_analysis] Proposta IA gerada com sucesso para {lead_empresa}")
        return result
        
    except ImportError:
        print("[ai_analysis] Pacote 'openai' não instalado.")
        return None
    except json.JSONDecodeError as e:
        print(f"[ai_analysis] Erro ao parsear JSON da proposta: {e}")
        # Tentar retornar valores padrão
        return {
            "titulo": f"Proposta Comercial — {lead_empresa}",
            "descricao": "Proposta gerada automaticamente. Edite os campos conforme necessário.",
            "escopo": "",
            "valor_sugerido": "R$ 0,00",
            "prazo": "30 dias úteis",
            "cronograma": "",
            "justificativa": ""
        }
    except Exception as e:
        print(f"[ai_analysis] Erro ao gerar proposta: {e}")
        return None


def gerar_contrato_ia(lead_nome, lead_empresa, proposta_data):
    """
    Analisa a proposta e gera seções de contrato profissional via OpenAI.
    Retorna: { titulo: str, sections: [{type:'title'|'description', content:str}] }
    """
    if not OPENAI_API_KEY:
        print("[ai_analysis] OPENAI_API_KEY não configurada")
        return None
    
    proposta_context = (
        f"Empresa: {lead_empresa}\n"
        f"Contato: {lead_nome}\n"
        f"Título da Proposta: {proposta_data.get('titulo', '')}\n"
        f"Descrição: {proposta_data.get('descricao', '')}\n"
        f"Escopo: {proposta_data.get('escopo', '')}\n"
        f"Valor: {proposta_data.get('valor', '')}\n"
        f"Prazo: {proposta_data.get('prazo', '')}\n"
        f"Cronograma: {proposta_data.get('cronograma', '')}\n"
        f"Justificativa: {proposta_data.get('justificativa', '')}\n"
    )
    
    try:
        import json
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = (
            "Com base na proposta comercial abaixo, gere um CONTRATO PROFISSIONAL estruturado.\n"
            "Responda em JSON com os campos:\n"
            "- titulo: Título do contrato (ex: 'Contrato de Prestação de Serviços — [Empresa]')\n"
            "- sections: Array de objetos {type, content} onde type é 'title' ou 'description'\n\n"
            "O contrato DEVE conter as seguintes seções (cada uma como um 'title' seguido de 'description'):\n"
            "1. DAS PARTES — Identificação das partes contratantes (CONTRATANTE e CONTRATADA)\n"
            "2. DO OBJETO — Descrição do objeto do contrato baseado na proposta\n"
            "3. DO ESCOPO DOS SERVIÇOS — Detalhamento dos serviços a serem prestados\n"
            "4. DO PRAZO — Prazo de vigência e execução\n"
            "5. DO VALOR E CONDIÇÕES DE PAGAMENTO — Valor total, forma e parcelamento\n"
            "6. DAS OBRIGAÇÕES DA CONTRATADA — Obrigações da prestadora de serviço\n"
            "7. DAS OBRIGAÇÕES DO CONTRATANTE — Obrigações do contratante\n"
            "8. DA CONFIDENCIALIDADE — Cláusula de sigilo\n"
            "9. DA PROPRIEDADE INTELECTUAL — Direitos sobre entregáveis\n"
            "10. DA RESCISÃO — Condições de rescisão contratual\n"
            "11. DAS PENALIDADES — Multas e penalidades\n"
            "12. DO FORO — Eleição de foro\n\n"
            "Use linguagem jurídica formal em português do Brasil. Cada 'description' deve ser um parágrafo completo.\n"
            "Responda APENAS com JSON válido.\n\n"
            f"Proposta:\n{proposta_context}"
        )
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Você é um advogado corporativo sênior. Gere contratos profissionais em português do Brasil. Responda APENAS em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1] if "\n" in content else content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        result = json.loads(content)
        print(f"[ai_analysis] Contrato IA gerado com sucesso para {lead_empresa}")
        return result
        
    except ImportError:
        print("[ai_analysis] Pacote 'openai' não instalado.")
        return None
    except json.JSONDecodeError as e:
        print(f"[ai_analysis] Erro ao parsear JSON do contrato: {e}")
        return {
            "titulo": f"Contrato de Prestação de Serviços — {lead_empresa}",
            "sections": [
                {"type": "title", "content": "DAS PARTES"},
                {"type": "description", "content": "Contrato gerado automaticamente. Edite os campos conforme necessário."}
            ]
        }
    except Exception as e:
        print(f"[ai_analysis] Erro ao gerar contrato: {e}")
        return None

