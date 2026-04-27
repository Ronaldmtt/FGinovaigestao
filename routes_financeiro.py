from flask import render_template, request, jsonify
from flask_login import login_required, current_user
import datetime as dt
import os
import uuid
from calendar import monthrange
from werkzeug.utils import secure_filename
from sqlalchemy import func
from models import db, FinCostCenter, FinAccount, FinTransaction, FinGoal, FinSupplier, FinClientContract, Client

def register_finance_routes(app):
    
    def finance_access_denied(is_api=False):
        if current_user.is_admin or getattr(current_user, 'acesso_financeiro', False):
            return None
        return (jsonify({'error': 'Acesso negado'}), 403) if is_api else ("Acesso Negado", 403)

    def add_months(base_date, months_to_add):
        month_index = base_date.month - 1 + months_to_add
        year = base_date.year + month_index // 12
        month = month_index % 12 + 1
        day = min(base_date.day, monthrange(year, month)[1])
        return dt.date(year, month, day)

    def parse_money(value, default=0.0):
        if value is None:
            return default
        raw = str(value).strip().replace('R$', '').replace(' ', '')
        if not raw:
            return default
        if ',' in raw:
            raw = raw.replace('.', '').replace(',', '.')
        try:
            return float(raw)
        except (TypeError, ValueError):
            return default

    # ==========================
    # VIEWS (HTML)
    # ==========================
    @app.route('/financeiro/dashboard')
    @login_required
    def finance_dashboard():
        denied = finance_access_denied()
        if denied: return denied
        return render_template('financeiro/dashboard.html')

    @app.route('/financeiro/contas')
    @login_required
    def finance_accounts():
        denied = finance_access_denied()
        if denied: return denied
        return render_template('financeiro/accounts.html')

    @app.route('/financeiro/centros-custo')
    @login_required
    def finance_cost_centers():
        denied = finance_access_denied()
        if denied: return denied
        return render_template('financeiro/cost_centers.html')

    @app.route('/financeiro/lancamentos')
    @login_required
    def finance_transactions():
        denied = finance_access_denied()
        if denied: return denied
        return render_template('financeiro/transactions.html')

    @app.route('/financeiro/relatorios')
    @login_required
    def finance_reports():
        denied = finance_access_denied()
        if denied: return denied
        return render_template('financeiro/reports.html')

    @app.route('/financeiro/metas')
    @login_required
    def finance_goals():
        denied = finance_access_denied()
        if denied: return denied
        return render_template('financeiro/goals.html')

    @app.route('/financeiro/fornecedores')
    @login_required
    def finance_suppliers():
        denied = finance_access_denied()
        if denied: return denied
        return render_template('financeiro/suppliers.html')

    @app.route('/financeiro/clientes')
    @login_required
    def finance_clients():
        denied = finance_access_denied()
        if denied: return denied
        return render_template('financeiro/clients.html')

    # ==========================
    # REST API - SUPPLIERS
    # ==========================
    @app.route('/api/financeiro/suppliers', methods=['GET', 'POST'])
    @login_required
    def api_suppliers():
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        
        if request.method == 'GET':
            suppliers = FinSupplier.query.filter_by(is_active=True).all()
            return jsonify([{'id': s.id, 'nome': s.nome, 'email': s.email, 'telefone': s.telefone} for s in suppliers])
        
        if request.method == 'POST':
            data = request.get_json()
            nome = data.get('nome')
            if not nome: return jsonify({'success': False, 'message': 'Nome é obrigatório'}), 400
            
            novoS = FinSupplier(nome=nome, email=data.get('email'), telefone=data.get('telefone'))
            db.session.add(novoS)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Fornecedor cadastrado'})

    @app.route('/api/financeiro/suppliers/<int:s_id>', methods=['PUT', 'DELETE'])
    @login_required
    def api_suppliers_detail(s_id):
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        sup = FinSupplier.query.get_or_404(s_id)
        
        if request.method == 'PUT':
            data = request.get_json()
            sup.nome = data.get('nome', sup.nome)
            sup.email = data.get('email', sup.email)
            sup.telefone = data.get('telefone', sup.telefone)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Fornecedor atualizado'})
            
        if request.method == 'DELETE':
            sup.is_active = False # Soft delete
            db.session.commit()
            return jsonify({'success': True})

    # ==========================
    # REST API - CLIENTS (FOR FINANCEIRO)
    # ==========================
    @app.route('/api/financeiro/clients', methods=['GET'])
    @login_required
    def api_finance_clients():
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        clientes = Client.query.all()
        return jsonify([{'id': c.id, 'nome': getattr(c, 'nome', f'Cliente #{c.id}')} for c in clientes])

    @app.route('/api/financeiro/client-contracts', methods=['GET', 'POST'])
    @login_required
    def api_finance_client_contracts():
        denied = finance_access_denied(is_api=True)
        if denied: return denied

        if request.method == 'GET':
            contracts = FinClientContract.query.filter_by(is_active=True).order_by(FinClientContract.created_at.desc()).all()
            return jsonify([{
                'id': c.id,
                'client_id': c.client_id,
                'client_name': c.client.nome if c.client else f'Cliente #{c.client_id}',
                'account_name': c.account.nome if c.account else '-',
                'cost_center_name': c.cost_center.nome if c.cost_center else '-',
                'contract_file_url': c.contract_file_url,
                'valor_mensal': c.valor_mensal,
                'primeiro_vencimento': c.primeiro_vencimento.isoformat() if c.primeiro_vencimento else None,
                'quantidade_titulos': c.quantidade_titulos,
                'prazo_observacao': c.prazo_observacao,
                'titles_generated': bool(c.titles_generated),
                'installment_group': c.installment_group,
                'created_at': c.created_at.isoformat() if c.created_at else None,
            } for c in contracts])

        data = request.form
        client_id = data.get('client_id', type=int)
        account_id = data.get('account_id', type=int)
        cost_center_id = data.get('cost_center_id', type=int)
        valor_mensal = parse_money(data.get('valor_mensal'))
        try:
            quantidade_titulos = max(int(data.get('quantidade_titulos') or 1), 1)
        except (TypeError, ValueError):
            quantidade_titulos = 1
        quantidade_titulos = min(quantidade_titulos, 120)
        primeiro_vencimento_raw = (data.get('primeiro_vencimento') or '').strip()
        gerar_titulos = str(data.get('gerar_titulos', '')).strip().lower() in ['1', 'true', 'on', 'yes', 'sim']

        if not client_id:
            return jsonify({'success': False, 'message': 'Selecione um cliente.'}), 400
        if gerar_titulos and (not account_id or valor_mensal <= 0 or not primeiro_vencimento_raw):
            return jsonify({'success': False, 'message': 'Para gerar títulos, informe conta, valor mensal e primeiro vencimento.'}), 400

        primeiro_vencimento = None
        if primeiro_vencimento_raw:
            try:
                primeiro_vencimento = dt.datetime.strptime(primeiro_vencimento_raw, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Data de vencimento inválida.'}), 400

        contract_filename = None
        file = request.files.get('contract_file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filename = f"fin_contract_{client_id}_{int(dt.datetime.utcnow().timestamp())}_{filename}"
            from flask import current_app
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            contract_filename = filename

        installment_group = str(uuid.uuid4()) if gerar_titulos else None
        contract = FinClientContract(
            client_id=client_id,
            account_id=account_id or None,
            cost_center_id=cost_center_id or None,
            contract_file_url=contract_filename,
            valor_mensal=valor_mensal if valor_mensal > 0 else None,
            primeiro_vencimento=primeiro_vencimento,
            quantidade_titulos=quantidade_titulos if gerar_titulos else None,
            prazo_observacao=(data.get('prazo_observacao') or '').strip() or None,
            titles_generated=gerar_titulos,
            installment_group=installment_group,
            created_by_id=current_user.id,
        )
        db.session.add(contract)

        generated_count = 0
        if gerar_titulos:
            client = Client.query.get(client_id)
            client_name = client.nome if client else f'Cliente #{client_id}'
            for idx in range(quantidade_titulos):
                due_date = add_months(primeiro_vencimento, idx)
                trans = FinTransaction(
                    tipo='income',
                    valor=valor_mensal,
                    data=due_date,
                    descricao=f'Contrato {client_name} ({idx + 1}/{quantidade_titulos})',
                    is_realized=False,
                    installment_group=installment_group,
                    installment_number=idx + 1,
                    installment_total=quantidade_titulos,
                    account_id=account_id,
                    cost_center_id=cost_center_id or None,
                    user_id=current_user.id,
                    comprovante_url=contract_filename if idx == 0 else None,
                    client_id=client_id,
                )
                db.session.add(trans)
                generated_count += 1

        db.session.commit()
        message = 'Cliente financeiro cadastrado.'
        if generated_count:
            message = f'Cliente financeiro cadastrado e {generated_count} título(s) criado(s).'
        return jsonify({'success': True, 'message': message, 'id': contract.id, 'generated_titles': generated_count})

    @app.route('/api/financeiro/client-contracts/<int:contract_id>', methods=['DELETE'])
    @login_required
    def api_finance_client_contract_detail(contract_id):
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        contract = FinClientContract.query.get_or_404(contract_id)
        contract.is_active = False
        db.session.commit()
        return jsonify({'success': True, 'message': 'Cliente financeiro arquivado.'})

    # ==========================
    # REST API - COST CENTERS
    # ==========================
    @app.route('/api/financeiro/cost-centers', methods=['GET', 'POST'])
    @login_required
    def api_cost_centers():
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        
        if request.method == 'GET':
            centros = FinCostCenter.query.filter_by(is_active=True).all()
            return jsonify([{'id': c.id, 'nome': c.nome, 'icone': c.icone, 'cor': c.cor} for c in centros])
            
        if request.method == 'POST':
            data = request.get_json(silent=True) or {}
            nome = (data.get('nome') or '').strip()
            if not nome: return jsonify({'success': False, 'message': 'Nome obrigatório'}), 400
            
            novo_cc = FinCostCenter(nome=nome, icone=data.get('icone', 'fas fa-tag'), cor=data.get('cor', '#cccccc'))
            db.session.add(novo_cc)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Centro de custo criado'})

    @app.route('/api/financeiro/cost-centers/<int:cc_id>', methods=['DELETE'])
    @login_required
    def api_cost_centers_del(cc_id):
        denied = finance_access_denied(is_api=True)
        if denied: return denied
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
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        
        if request.method == 'GET':
            contas = FinAccount.query.filter_by(is_active=True).all()
            result = []
            for a in contas:
                if a.tipo == 'credit_card':
                    hoje = dt.date.today()
                    # Calculate current invoice only for realized expenses in current month
                    fatura_atual = sum(
                        t.valor for t in a.transactions
                        if t.tipo == 'expense' and t.is_realized and t.data.month == hoje.month and t.data.year == hoje.year
                    )
                else:
                    fatura_atual = 0.0
                
                result.append({
                    'id': a.id,
                    'nome': a.nome,
                    'tipo': a.tipo,
                    'saldo_inicial': a.saldo_inicial,
                    'saldo_atual': getattr(a, 'saldo_atual', 0.0) if a.tipo == 'wallet' else 0,
                    'limite_credito': a.limite_credito if a.tipo == 'credit_card' else 0,
                    'fatura_atual': fatura_atual,
                    'dia_vencimento': a.dia_vencimento if a.tipo == 'credit_card' else None,
                    'icone': 'fas fa-wallet' if a.tipo == 'wallet' else 'fas fa-credit-card',
                    'cor': '#333333'
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

    @app.route('/api/financeiro/accounts/<int:a_id>', methods=['DELETE', 'PUT'])
    @login_required
    def api_accounts_del(a_id):
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        acc = FinAccount.query.get_or_404(a_id)
        
        if request.method == 'PUT':
            data = request.get_json()
            acc.nome = data.get('nome', acc.nome)
            if 'saldo_inicial' in data:
                acc.saldo_inicial = float(data['saldo_inicial'])
            if acc.tipo == 'credit_card':
                if 'limite_credito' in data:
                    acc.limite_credito = float(data['limite_credito'])
                if 'dia_vencimento' in data:
                    acc.dia_vencimento = int(data['dia_vencimento']) if data['dia_vencimento'] else None
                if 'dia_fechamento' in data:
                    acc.dia_fechamento = int(data['dia_fechamento']) if data['dia_fechamento'] else None
            db.session.commit()
            return jsonify({'success': True, 'message': 'Conta atualizada com sucesso'})
        
        if request.method == 'DELETE':
            acc.is_active = False # Soft delete
            db.session.commit()
            return jsonify({'success': True})

    # ==========================
    # REST API - TRANSACTIONS
    # ==========================
    @app.route('/api/financeiro/transactions', methods=['GET', 'POST'])
    @login_required
    def api_transactions():
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        
        if request.method == 'GET':
            status_filter = request.args.get('status')
            tipo_filter = request.args.get('tipo')
            account_filter = request.args.get('account_id', type=int)

            query = FinTransaction.query
            if status_filter == 'realized':
                query = query.filter(FinTransaction.is_realized.is_(True))
            elif status_filter == 'pending':
                query = query.filter(FinTransaction.is_realized.is_(False))

            if tipo_filter in ['income', 'expense']:
                query = query.filter(FinTransaction.tipo == tipo_filter)
            if account_filter:
                query = query.filter(FinTransaction.account_id == account_filter)

            transacoes = query.order_by(FinTransaction.data.desc(), FinTransaction.created_at.desc()).limit(300).all()
            return jsonify([{
                'id': t.id,
                'tipo': t.tipo,
                'valor': t.valor,
                'data': t.data.isoformat() if t.data else None,
                'descricao': t.descricao,
                'conta': t.account.nome if t.account else '-',
                'centro_custo': t.cost_center.nome if t.cost_center else '-',
                'cor_cc': t.cost_center.cor if t.cost_center else '#ccc',
                'comprovante_url': t.comprovante_url,
                'cliente': t.client.nome if t.client else None,
                'fornecedor': t.supplier.nome if t.supplier else None,
                'is_realized': bool(t.is_realized),
                'installment_group': t.installment_group,
                'installment_number': t.installment_number,
                'installment_total': t.installment_total
            } for t in transacoes])
            
        if request.method == 'POST':
            # Support both json and multipart
            if request.is_json: data = request.get_json()
            else: data = request.form
            
            if not all([data.get('tipo'), data.get('valor'), data.get('data'), data.get('descricao'), data.get('account_id')]):
                return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatórios'}), 400
                
            try:
                parsed_date = dt.datetime.strptime(data.get('data'), '%Y-%m-%d').date()
            except:
                parsed_date = dt.date.today()
                
            # Tratar File Upload
            comprovante_filename = None
            if 'file' in request.files:
                file = request.files['file']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    import time
                    filename = f"fin_{int(time.time())}_{filename}"
                    from flask import current_app
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    comprovante_filename = filename
                
            is_realized_raw = str(data.get('is_realized', '')).strip().lower()
            is_realized = is_realized_raw in ['1', 'true', 'on', 'yes', 'sim']
            installments = max(int(data.get('installments', 1) or 1), 1)
            installment_group = str(uuid.uuid4()) if installments > 1 else None
            total_value = float(data.get('valor', 0.0))
            base_value = round(total_value / installments, 2)
            generated = []

            for idx in range(installments):
                parcela_valor = base_value
                if idx == installments - 1:
                    parcela_valor = round(total_value - (base_value * (installments - 1)), 2)

                trans = FinTransaction(
                    tipo=data.get('tipo'),
                    valor=parcela_valor,
                    data=add_months(parsed_date, idx),
                    descricao=data.get('descricao') if installments == 1 else f"{data.get('descricao')} ({idx + 1}/{installments})",
                    is_realized=is_realized if idx == 0 else False,
                    installment_group=installment_group,
                    installment_number=(idx + 1) if installments > 1 else None,
                    installment_total=installments if installments > 1 else None,
                    account_id=data.get('account_id'),
                    cost_center_id=data.get('cost_center_id') or None,
                    user_id=current_user.id,
                    comprovante_url=comprovante_filename if idx == 0 else None,
                    client_id=int(data.get('client_id')) if data.get('client_id') else None,
                    supplier_id=int(data.get('supplier_id')) if data.get('supplier_id') else None
                )
                db.session.add(trans)
                generated.append(trans)

            db.session.commit()
            if installments > 1:
                return jsonify({'success': True, 'message': f'{installments} parcelas registradas com sucesso'})
            return jsonify({'success': True, 'message': 'Lançamento registrado'})

    @app.route('/api/financeiro/transactions/<int:t_id>', methods=['PUT', 'DELETE'])
    @login_required
    def api_transaction_detail(t_id):
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        trans = FinTransaction.query.get_or_404(t_id)

        if request.method == 'PUT':
            data = request.get_json() or {}
            if 'is_realized' in data:
                trans.is_realized = bool(data.get('is_realized'))
            if 'data' in data and data.get('data'):
                try:
                    trans.data = dt.datetime.strptime(data.get('data'), '%Y-%m-%d').date()
                except Exception:
                    pass
            db.session.commit()
            return jsonify({'success': True, 'message': 'Lançamento atualizado'})

        db.session.delete(trans)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Lançamento deletado (Hard delete)'})

    # ==========================
    # REST API - DASHBOARD STATS
    # ==========================
    @app.route('/uploads/financeiro/<filename>')
    @login_required
    def finance_upload(filename):
        from flask import current_app, send_from_directory
        denied = finance_access_denied()
        if denied: return denied
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
        
    @app.route('/api/financeiro/dashboard-stats', methods=['GET'])
    @login_required
    def api_dashboard_stats():
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        
        hoje = dt.date.today()
        primeiro_dia_mes = dt.date(hoje.year, hoje.month, 1)
        
        wallets = FinAccount.query.filter_by(tipo='wallet', is_active=True).all()
        saldo_caixa = sum(w.saldo_atual for w in wallets)
        
        todos_lanc_mes = FinTransaction.query.filter(FinTransaction.data >= primeiro_dia_mes).all()
        lanc_realizados_mes = [t for t in todos_lanc_mes if t.is_realized]
        receitas_mes = sum(t.valor for t in lanc_realizados_mes if t.tipo == 'income')
        despesas_mes = sum(t.valor for t in lanc_realizados_mes if t.tipo == 'expense')
        balanco = receitas_mes - despesas_mes
        
        ultimos_5 = FinTransaction.query.order_by(FinTransaction.data.desc(), FinTransaction.created_at.desc()).limit(5).all()
        ultimos_5_serializados = [{
            'data': t.data.isoformat() if t.data else None,
            'descricao': t.descricao,
            'valor': t.valor,
            'tipo': t.tipo,
            'conta': t.account.nome if t.account else '-',
            'centro_custo': t.cost_center.nome if t.cost_center else '-',
            'is_realized': bool(t.is_realized)
        } for t in ultimos_5]

        pending_income = sum(t.valor for t in todos_lanc_mes if t.tipo == 'income' and not t.is_realized)
        pending_expense = sum(t.valor for t in todos_lanc_mes if t.tipo == 'expense' and not t.is_realized)

        return jsonify({
            'saldo_wallets': saldo_caixa,
            'receitas_mes': receitas_mes,
            'despesas_mes': despesas_mes,
            'balanco_mes': balanco,
            'pending_income': pending_income,
            'pending_expense': pending_expense,
            'recent_transactions': ultimos_5_serializados
        })

    # ==========================
    # REST API - REPORTS DATA
    # ==========================
    @app.route('/api/financeiro/relatorios-dados', methods=['GET'])
    @login_required
    def api_reports_data():
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        
        hoje = dt.date.today()
        primeiro_dia_mes = dt.date(hoje.year, hoje.month, 1)
        
        gastos = db.session.query(
            FinCostCenter.nome.label('categoria'),
            FinCostCenter.cor,
            func.sum(FinTransaction.valor).label('total')
        ).join(FinTransaction, FinTransaction.cost_center_id == FinCostCenter.id)\
         .filter(FinTransaction.tipo == 'expense', FinTransaction.is_realized.is_(True), FinTransaction.data >= primeiro_dia_mes)\
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
                
            trans = FinTransaction.query.filter(FinTransaction.data >= inicio, FinTransaction.data < fim, FinTransaction.is_realized.is_(True)).all()
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
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        
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
        denied = finance_access_denied(is_api=True)
        if denied: return denied
        meta = FinGoal.query.get_or_404(g_id)
        if request.method == 'PUT':
            data = request.get_json()
            if 'nome' in data: meta.nome = data['nome']
            if 'valor_alvo' in data: meta.valor_alvo = float(data['valor_alvo'])
            if 'valor_atual' in data: meta.valor_atual = float(data['valor_atual'])
            if 'prazo' in data:
                try: meta.prazo = dt.datetime.strptime(data['prazo'], '%Y-%m-%d').date() if data['prazo'] else None
                except: pass
            if 'cor' in data: meta.cor = data['cor']
            if 'icone' in data: meta.icone = data['icone']
            db.session.commit()
            return jsonify({'success': True, 'message': 'Meta atualizada'})
            
        if request.method == 'DELETE':
            db.session.delete(meta)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Meta apagada'})
