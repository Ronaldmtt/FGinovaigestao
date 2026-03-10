from flask import render_template, request, jsonify
from flask_login import login_required, current_user
import datetime as dt
from sqlalchemy import func
from models import db, FinCostCenter, FinAccount, FinTransaction, FinGoal

def register_finance_routes(app):
    
    # ==========================
    # VIEWS (HTML)
    # ==========================
    @app.route('/financeiro/dashboard')
    @login_required
    def finance_dashboard():
        if not current_user.is_admin: return "Acesso Negado", 403
        return render_template('financeiro/dashboard.html')

    @app.route('/financeiro/contas')
    @login_required
    def finance_accounts():
        if not current_user.is_admin: return "Acesso Negado", 403
        return render_template('financeiro/accounts.html')

    @app.route('/financeiro/centros-custo')
    @login_required
    def finance_cost_centers():
        if not current_user.is_admin: return "Acesso Negado", 403
        return render_template('financeiro/cost_centers.html')

    @app.route('/financeiro/lancamentos')
    @login_required
    def finance_transactions():
        if not current_user.is_admin: return "Acesso Negado", 403
        return render_template('financeiro/transactions.html')

    @app.route('/financeiro/relatorios')
    @login_required
    def finance_reports():
        if not current_user.is_admin: return "Acesso Negado", 403
        return render_template('financeiro/reports.html')

    @app.route('/financeiro/metas')
    @login_required
    def finance_goals():
        if not current_user.is_admin: return "Acesso Negado", 403
        return render_template('financeiro/goals.html')

    # ==========================
    # REST API - COST CENTERS
    # ==========================
    @app.route('/api/financeiro/cost-centers', methods=['GET', 'POST'])
    @login_required
    def api_cost_centers():
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        
        if request.method == 'GET':
            centros = FinCostCenter.query.filter_by(is_active=True).all()
            return jsonify([{'id': c.id, 'nome': c.nome, 'icone': c.icone, 'cor': c.cor} for c in centros])
            
        if request.method == 'POST':
            data = request.get_json()
            nome = data.get('nome')
            if not nome: return jsonify({'success': False, 'message': 'Nome obrigatório'}), 400
            
            novo_cc = FinCostCenter(nome=nome, icone=data.get('icone', 'fas fa-tag'), cor=data.get('cor', '#cccccc'))
            db.session.add(novo_cc)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Centro de custo criado'})

    @app.route('/api/financeiro/cost-centers/<int:cc_id>', methods=['DELETE'])
    @login_required
    def api_cost_centers_del(cc_id):
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        cc = FinCostCenter.query.get_or_404(cc_id)
        cc.is_active = False # Soft delete
        db.session.commit()
        return jsonify({'success': True, 'message': 'Centro de custo arquivado'})

    # ==========================
    # REST API - ACCOUNTS (WALLETS & CARDS)
    # ==========================
    @app.route('/api/financeiro/accounts', methods=['GET', 'POST'])
    @login_required
    def api_accounts():
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        
        if request.method == 'GET':
            contas = FinAccount.query.filter_by(is_active=True).all()
            result = []
            for a in contas:
                if a.tipo == 'card':
                    hoje = dt.date.today()
                    # Calculate current invoice (sum of expenses for this card in current month)
                    fatura_atual = sum(t.valor for t in a.transactions if t.tipo == 'expense' and t.data.month == hoje.month and t.data.year == hoje.year)
                else:
                    fatura_atual = 0.0
                
                result.append({
                    'id': a.id,
                    'nome': a.nome,
                    'tipo': a.tipo,
                    'saldo_inicial': a.saldo_inicial,
                    'saldo_atual': a.saldo_atual if a.tipo == 'wallet' else 0,
                    'limite_credito': a.limite_credito if a.tipo == 'card' else 0,
                    'fatura_atual': fatura_atual,
                    'dia_vencimento': a.dia_vencimento if a.tipo == 'card' else None,
                    'icone': a.icone,
                    'cor': a.cor
                })
            return jsonify(result)
            
        if request.method == 'POST':
            data = request.get_json()
            nome = data.get('nome')
            tipo = data.get('tipo', 'wallet')
            
            if not nome or not tipo: return jsonify({'success': False, 'message': 'Nome e tipo são obrigatórios'}), 400
            
            nova_conta = FinAccount(
                nome=nome, 
                tipo=tipo,
                saldo_inicial=float(data.get('saldo_inicial', 0.0)),
                limite_credito=float(data.get('limite_credito', 0.0)) if tipo == 'credit_card' else 0.0,
                dia_vencimento=int(data.get('dia_vencimento')) if data.get('dia_vencimento') and tipo == 'credit_card' else None,
                dia_fechamento=int(data.get('dia_fechamento')) if data.get('dia_fechamento') and tipo == 'credit_card' else None
            )
            db.session.add(nova_conta)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Conta cadastrada com sucesso'})

    @app.route('/api/financeiro/accounts/<int:a_id>', methods=['DELETE'])
    @login_required
    def api_accounts_del(a_id):
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        acc = FinAccount.query.get_or_404(a_id)
        acc.is_active = False # Soft delete
        db.session.commit()
        return jsonify({'success': True})

    # ==========================
    # REST API - TRANSACTIONS
    # ==========================
    @app.route('/api/financeiro/transactions', methods=['GET', 'POST'])
    @login_required
    def api_transactions():
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        
        if request.method == 'GET':
            transacoes = FinTransaction.query.order_by(FinTransaction.data.desc(), FinTransaction.created_at.desc()).limit(100).all()
            return jsonify([{
                'id': t.id,
                'tipo': t.tipo,
                'valor': t.valor,
                'data': t.data.isoformat() if t.data else None,
                'descricao': t.descricao,
                'conta': t.account.nome if t.account else '-',
                'centro_custo': t.cost_center.nome if t.cost_center else '-',
                'cor_cc': t.cost_center.cor if t.cost_center else '#ccc'
            } for t in transacoes])
            
        if request.method == 'POST':
            data = request.get_json()
            
            if not all([data.get('tipo'), data.get('valor'), data.get('data'), data.get('descricao'), data.get('account_id')]):
                return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatórios'}), 400
                
            try:
                parsed_date = dt.datetime.strptime(data.get('data'), '%Y-%m-%d').date()
            except:
                parsed_date = dt.date.today()
                
            trans = FinTransaction(
                tipo=data.get('tipo'),
                valor=float(data.get('valor', 0.0)),
                data=parsed_date,
                descricao=data.get('descricao'),
                account_id=data.get('account_id'),
                cost_center_id=data.get('cost_center_id') or None,
                user_id=current_user.id
            )
            db.session.add(trans)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Lançamento registrado'})

    @app.route('/api/financeiro/transactions/<int:t_id>', methods=['DELETE'])
    @login_required
    def api_transaction_detail(t_id):
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        trans = FinTransaction.query.get_or_404(t_id)
        db.session.delete(trans)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Lançamento deletado (Hard delete)'})

    # ==========================
    # REST API - DASHBOARD STATS
    # ==========================
    @app.route('/api/financeiro/dashboard-stats', methods=['GET'])
    @login_required
    def api_dashboard_stats():
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        
        hoje = dt.date.today()
        primeiro_dia_mes = dt.date(hoje.year, hoje.month, 1)
        
        wallets = FinAccount.query.filter_by(tipo='wallet', is_active=True).all()
        saldo_caixa = sum(w.saldo_atual for w in wallets)
        
        todos_lanc_mes = FinTransaction.query.filter(FinTransaction.data >= primeiro_dia_mes).all()
        receitas_mes = sum(t.valor for t in todos_lanc_mes if t.tipo == 'income')
        despesas_mes = sum(t.valor for t in todos_lanc_mes if t.tipo == 'expense')
        balanco = receitas_mes - despesas_mes
        
        ultimos_5 = FinTransaction.query.order_by(FinTransaction.data.desc(), FinTransaction.created_at.desc()).limit(5).all()
        ultimos_5_serializados = [{
            'data': t.data.isoformat() if t.data else None,
            'descricao': t.descricao,
            'valor': t.valor,
            'tipo': t.tipo,
            'conta': t.account.nome if t.account else '-',
            'centro_custo': t.cost_center.nome if t.cost_center else '-'
        } for t in ultimos_5]

        return jsonify({
            'saldo_wallets': saldo_caixa,
            'receitas_mes': receitas_mes,
            'despesas_mes': despesas_mes,
            'balanco_mes': balanco,
            'recent_transactions': ultimos_5_serializados
        })

    # ==========================
    # REST API - REPORTS DATA
    # ==========================
    @app.route('/api/financeiro/relatorios-dados', methods=['GET'])
    @login_required
    def api_reports_data():
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        
        hoje = dt.date.today()
        primeiro_dia_mes = dt.date(hoje.year, hoje.month, 1)
        
        gastos = db.session.query(
            FinCostCenter.nome.label('categoria'),
            FinCostCenter.cor,
            func.sum(FinTransaction.valor).label('total')
        ).join(FinTransaction, FinTransaction.cost_center_id == FinCostCenter.id)\
         .filter(FinTransaction.tipo == 'expense', FinTransaction.data >= primeiro_dia_mes)\
         .group_by(FinCostCenter.id).all()
         
        grafico_centros = {
            'labels': [g.categoria for g in gastos] if gastos else ['Sem Dados'],
            'data': [float(g.total) for g in gastos] if gastos else [1],
            'colors': [g.cor for g in gastos] if gastos else ['#333']
        }
        
        meses_str = []
        receitas_trends = []
        despesas_trends = []
        
        for i in range(5, -1, -1):
            m = (hoje.month - i - 1) % 12 + 1
            y = hoje.year + ((hoje.month - i - 1) // 12)
            meses_str.append(f"{m:02d}/{y}")
            
            inicio = dt.date(y, m, 1)
            fim = dt.date(y+1, 1, 1) if m == 12 else dt.date(y, m+1, 1)
                
            trans = FinTransaction.query.filter(FinTransaction.data >= inicio, FinTransaction.data < fim).all()
            rec = sum(t.valor for t in trans if t.tipo == 'income')
            desp = sum(t.valor for t in trans if t.tipo == 'expense')
            
            receitas_trends.append(float(rec))
            despesas_trends.append(float(desp))

        return jsonify({
            'cost_centers': grafico_centros,
            'trends': {
                'labels': meses_str,
                'receitas': receitas_trends,
                'despesas': despesas_trends
            }
        })

    # ==========================
    # REST API - GOALS
    # ==========================
    @app.route('/api/financeiro/goals', methods=['GET', 'POST'])
    @login_required
    def api_goals():
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        
        if request.method == 'GET':
            metas = FinGoal.query.order_by(FinGoal.prazo.asc()).all()
            return jsonify([{
                'id': m.id,
                'nome': m.nome,
                'valor_alvo': m.valor_alvo,
                'valor_atual': m.valor_atual,
                'prazo': m.prazo.isoformat() if m.prazo else None,
                'icone': m.icone,
                'cor': m.cor,
                'porcentagem': m.progress_percent
            } for m in metas])
            
        if request.method == 'POST':
            data = request.get_json()
            nome = data.get('nome')
            valor_alvo = float(data.get('valor_alvo', 0.0))
            if not nome or not valor_alvo: return jsonify({'success': False, 'message': 'Nome e Valor Alvo obrigatórios'}), 400
                
            try:
                prazo_date = dt.datetime.strptime(data.get('prazo'), '%Y-%m-%d').date() if data.get('prazo') else None
            except:
                prazo_date = None
                    
            meta = FinGoal(
                nome=nome,
                valor_alvo=valor_alvo,
                valor_atual=float(data.get('valor_atual', 0.0)),
                prazo=prazo_date,
                cor=data.get('cor', '#10b981'),
                icone=data.get('icone', 'fas fa-bullseye')
            )
            db.session.add(meta)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Meta registrada'})

    @app.route('/api/financeiro/goals/<int:g_id>', methods=['PUT', 'DELETE'])
    @login_required
    def api_goal_detail(g_id):
        if not current_user.is_admin: return jsonify({'error': 'Acesso negado'}), 403
        meta = FinGoal.query.get_or_404(g_id)
        if request.method == 'PUT':
            data = request.get_json()
            meta.valor_atual = float(data.get('valor_atual', meta.valor_atual))
            db.session.commit()
            return jsonify({'success': True, 'message': 'Progresso atualizado'})
            
        if request.method == 'DELETE':
            db.session.delete(meta)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Meta apagada'})
