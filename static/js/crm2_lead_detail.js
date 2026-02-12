/* crm2_lead_detail.js — JS lógica para Contratos, Propostas, Clientes e Reuniões */
const LEAD_ID = window.location.pathname.split('/').pop();

/* ========== Observações ========== */
function saveObservacoes() {
    const obs = document.getElementById('obsText').value;
    fetch(`/api/crm2/lead/${LEAD_ID}/observacoes`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({observacoes: obs})
    }).then(r => r.json()).then(d => {
        if (d.success) {
            const el = document.getElementById('obsSaved');
            el.style.display = 'inline'; setTimeout(() => el.style.display = 'none', 2000);
        } else alert(d.message || 'Erro ao salvar');
    }).catch(() => alert('Erro de conexão'));
}

/* ========== Reunião ========== */
function openMeetingModal() { new bootstrap.Modal(document.getElementById('meetingModal')).show(); }

function createMeeting() {
    const btn = document.getElementById('btnCreateMeeting');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Criando...';
    fetch(`/api/crm2/lead/${LEAD_ID}/meeting`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            titulo: document.getElementById('mtgTitle').value,
            data: document.getElementById('mtgDate').value,
            horario_inicio: document.getElementById('mtgStart').value,
            horario_fim: document.getElementById('mtgEnd').value,
            guests: document.getElementById('mtgGuests').value,
            descricao: document.getElementById('mtgDescription').value,
            pauta: document.getElementById('mtgAgenda').value
        })
    }).then(r => r.json()).then(d => {
        if (d.success) location.reload(); else { alert(d.message); btn.disabled = false; btn.innerHTML = '<i class="fas fa-paper-plane me-1"></i>Criar'; }
    }).catch(() => { alert('Erro de conexão'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-paper-plane me-1"></i>Criar'; });
}

/* ========== Chamado ========== */
function openChamadoModal() { new bootstrap.Modal(document.getElementById('chamadoModal')).show(); }

function createChamado() {
    const btn = document.getElementById('btnCreateChamado');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Enviando...';
    fetch(`/api/crm2/lead/${LEAD_ID}/chamado`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            user_id: document.getElementById('chamadoUser').value,
            titulo: document.getElementById('chamadoTitle').value,
            data: document.getElementById('chamadoDate').value,
            horario_inicio: document.getElementById('chamadoStart').value,
            horario_fim: document.getElementById('chamadoEnd').value,
            guests: document.getElementById('chamadoGuests').value,
            descricao: document.getElementById('chamadoDesc').value,
            pauta: document.getElementById('chamadoPauta').value
        })
    }).then(r => r.json()).then(d => {
        if (d.success) location.reload(); else { alert(d.message); btn.disabled = false; btn.innerHTML = '<i class="fas fa-paper-plane me-1"></i>Enviar'; }
    }).catch(() => { alert('Erro de conexão'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-paper-plane me-1"></i>Enviar'; });
}

/* ========== Transcrição ========== */
function refreshTranscript(meetingId, btn) {
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Buscando...';
    fetch(`/api/crm2/meeting/${meetingId}/refresh-transcript`, {method: 'POST'})
        .then(r => r.json()).then(d => { if (d.success) location.reload(); else { alert(d.message || 'Erro ao buscar'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-sync-alt me-1"></i>Buscar Transcrição'; }})
        .catch(() => { alert('Erro de conexão'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-sync-alt me-1"></i>Buscar Transcrição'; });
}

/* ========== Proposta: Advance / Generate / Save ========== */
function advanceToProposta() {
    if (!confirm('Mover lead para Proposta?')) return;
    fetch(`/api/crm2/lead/${LEAD_ID}/advance-proposta`, {method: 'POST'})
        .then(r => r.json()).then(d => { if (d.success) location.reload(); else alert(d.message); });
}

function generateProposalIA() {
    const btn = document.getElementById('btnGenProposta');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Gerando IA...';
    fetch(`/api/crm2/lead/${LEAD_ID}/generate-proposal`, {method: 'POST'})
        .then(r => r.json()).then(d => {
            btn.disabled = false; btn.innerHTML = '<i class="fas fa-brain me-1"></i>Gerar Proposta IA';
            if (d.success && d.proposal) {
                const p = d.proposal;
                document.getElementById('propTitulo').value = p.titulo || '';
                document.getElementById('propDescricao').value = p.descricao || '';
                document.getElementById('propEscopo').value = p.escopo || '';
                document.getElementById('propValor').value = p.valor_sugerido || p.valor || '';
                document.getElementById('propPrazo').value = p.prazo || '';
                document.getElementById('propCronograma').value = p.cronograma || '';
                document.getElementById('propJustificativa').value = p.justificativa || '';
                new bootstrap.Modal(document.getElementById('proposalModal')).show();
            } else alert(d.message || 'Erro ao gerar proposta');
        }).catch(() => { alert('Erro de conexão'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-brain me-1"></i>Gerar Proposta IA'; });
}

function saveProposal() {
    const btn = document.getElementById('btnSaveProposal');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Salvando...';
    fetch(`/api/crm2/lead/${LEAD_ID}/save-proposal`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            titulo: document.getElementById('propTitulo').value,
            descricao: document.getElementById('propDescricao').value,
            escopo: document.getElementById('propEscopo').value,
            valor: document.getElementById('propValor').value,
            prazo: document.getElementById('propPrazo').value,
            cronograma: document.getElementById('propCronograma').value,
            justificativa: document.getElementById('propJustificativa').value
        })
    }).then(r => r.json()).then(d => {
        if (d.success) location.reload(); else { alert(d.message); btn.disabled = false; btn.innerHTML = '<i class="fas fa-save me-1"></i>Salvar Proposta'; }
    }).catch(() => { alert('Erro'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-save me-1"></i>Salvar Proposta'; });
}

function sendProposalPDF(id) {
    if (!confirm('Enviar proposta por email?')) return;
    fetch(`/api/crm2/proposal/${id}/send`, {method: 'POST'})
        .then(r => r.json()).then(d => alert(d.message)).catch(() => alert('Erro'));
}

function acceptProposal(id) {
    if (!confirm('Aceitar proposta e avançar para Contrato?')) return;
    fetch(`/api/crm2/proposal/${id}/accept`, {method: 'POST'})
        .then(r => r.json()).then(d => { if (d.success) location.reload(); else alert(d.message); });
}

function rejectProposal(id) {
    if (!confirm('Recusar proposta? Ela será removida.')) return;
    fetch(`/api/crm2/proposal/${id}/reject`, {method: 'POST'})
        .then(r => r.json()).then(d => { if (d.success) location.reload(); else alert(d.message); });
}

/* ========== Contrato: Generate / Save / Send / Accept / Reject ========== */
let contractSections = [];

function generateContractIA() {
    const btn = document.getElementById('btnGenContrato');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Gerando IA...';
    fetch(`/api/crm2/lead/${LEAD_ID}/generate-contract`, {method: 'POST'})
        .then(r => r.json()).then(d => {
            btn.disabled = false; btn.innerHTML = '<i class="fas fa-brain me-1"></i>Gerar Contrato IA';
            if (d.success && d.contract) {
                document.getElementById('contractTitulo').value = d.contract.titulo || '';
                contractSections = d.contract.sections || [];
                renderContractSections();
                new bootstrap.Modal(document.getElementById('contractModal')).show();
            } else alert(d.message || 'Erro ao gerar contrato');
        }).catch(() => { alert('Erro de conexão'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-brain me-1"></i>Gerar Contrato IA'; });
}

function renderContractSections() {
    const container = document.getElementById('contractSections');
    container.innerHTML = '';
    contractSections.forEach((s, i) => {
        const div = document.createElement('div');
        div.className = 'contract-section-item';
        const label = s.type === 'title' ? '📌 Título' : '📝 Descrição';
        const tag = s.type === 'title' ? 'input' : 'textarea';
        const rows = s.type === 'title' ? '' : ' rows="3"';
        div.innerHTML = `
            <small class="text-muted d-block mb-1">${label}</small>
            <button class="remove-section" onclick="removeContractSection(${i})" title="Remover"><i class="fas fa-times"></i></button>
            <${tag} class="form-control form-control-sm" data-idx="${i}"${rows}>${s.content || ''}</${tag}>
        `;
        container.appendChild(div);
    });
}

function openAddSectionModal() {
    new bootstrap.Modal(document.getElementById('addSectionModal')).show();
}

function addContractSection(type) {
    contractSections.push({type: type, content: ''});
    renderContractSections();
    bootstrap.Modal.getInstance(document.getElementById('addSectionModal'))?.hide();
    // scroll to bottom
    const container = document.getElementById('contractSections');
    container.lastElementChild?.scrollIntoView({behavior: 'smooth', block: 'nearest'});
}

function removeContractSection(idx) {
    contractSections.splice(idx, 1);
    renderContractSections();
}

function collectContractSections() {
    const items = document.querySelectorAll('#contractSections .contract-section-item');
    const sections = [];
    items.forEach((item, i) => {
        const el = item.querySelector('input, textarea');
        sections.push({type: contractSections[i].type, content: el.value});
    });
    return sections;
}

function saveContract() {
    const btn = document.getElementById('btnSaveContract');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Salvando...';
    const sections = collectContractSections();
    fetch(`/api/crm2/lead/${LEAD_ID}/save-contract`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            titulo: document.getElementById('contractTitulo').value,
            sections: sections
        })
    }).then(r => r.json()).then(d => {
        if (d.success) location.reload(); else { alert(d.message); btn.disabled = false; btn.innerHTML = '<i class="fas fa-save me-1"></i>Salvar Contrato'; }
    }).catch(() => { alert('Erro'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-save me-1"></i>Salvar Contrato'; });
}

function sendContract(id) {
    if (!confirm('Enviar contrato por email?')) return;
    fetch(`/api/crm2/contract/${id}/send`, {method: 'POST'})
        .then(r => r.json()).then(d => alert(d.message)).catch(() => alert('Erro'));
}

function acceptContract(id) {
    if (!confirm('Marcar contrato como ASSINADO e mover para Cliente?')) return;
    fetch(`/api/crm2/contract/${id}/accept`, {method: 'POST'})
        .then(r => r.json()).then(d => { if (d.success) location.reload(); else alert(d.message); });
}

function rejectContract(id) {
    if (!confirm('Recusar contrato? Ele será removido.')) return;
    fetch(`/api/crm2/contract/${id}/reject`, {method: 'POST'})
        .then(r => r.json()).then(d => { if (d.success) location.reload(); else alert(d.message); });
}

/* ========== Cliente ========== */
function openCreateClientModal() {
    new bootstrap.Modal(document.getElementById('createClientModal')).show();
}

function createClient() {
    const btn = document.getElementById('btnCreateClient');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Criando...';
    fetch(`/api/crm2/lead/${LEAD_ID}/create-client`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            nome: document.getElementById('clientNome').value,
            email: document.getElementById('clientEmail').value,
            telefone: document.getElementById('clientTelefone').value,
            empresa: document.getElementById('clientEmpresa').value,
            endereco: document.getElementById('clientEndereco').value,
            observacoes: document.getElementById('clientObs').value
        })
    }).then(r => r.json()).then(d => {
        if (d.success) {
            alert(d.message);
            location.reload();
        } else { alert(d.message); btn.disabled = false; btn.innerHTML = '<i class="fas fa-user-plus me-1"></i>Criar'; }
    }).catch(() => { alert('Erro de conexão'); btn.disabled = false; btn.innerHTML = '<i class="fas fa-user-plus me-1"></i>Criar'; });
}
