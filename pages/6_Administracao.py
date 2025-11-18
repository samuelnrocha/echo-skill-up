"""
Página de Administração
"""

import streamlit as st
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication

# Configuração
st.set_page_config(
    page_title="Administração - Eco-Skill Up",
    page_icon="⚙️",
    layout="wide"
)

# Inicializa tema
init_theme()
apply_theme(st.session_state.get('theme', 'light'))

# Verifica autenticação
if not check_authentication():
    st.stop()

# Sidebar
page = render_sidebar()

# Header
render_header("⚙️ Administração", "Gerencie usuários, configurações e sistema")

is_admin = st.session_state.current_user.get('role') == 'admin'

if not is_admin:
    st.warning("⚠️ Apenas administradores podem acessar a página de Administração.")
    st.stop()

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs(["👥 Usuários", "🔧 Configurações", "📊 Relatórios", "🔐 Segurança"])

# ==================== TAB 1: USUÁRIOS ====================
with tab1:
    st.markdown("### 👥 Gerenciamento de Usuários")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_user = st.text_input("🔍 Buscar usuário", placeholder="Digite o nome ou email...")
    
    with col2:
        filter_role = st.selectbox("Filtrar por perfil", ["Todos", "Admin", "Usuário", "Instrutor"])
    
    # Tabela de usuários (mockada)
    users_data = {
        'ID': [1, 2, 3, 4, 5],
        'Nome': ['Ana Silva', 'Carlos Santos', 'Maria Oliveira', 'João Pereira', 'Lucia Costa'],
        'Email': ['ana@email.com', 'carlos@email.com', 'maria@email.com', 'joao@email.com', 'lucia@email.com'],
        'Perfil': ['Admin', 'Usuário', 'Usuário', 'Instrutor', 'Usuário'],
        'Status': ['Ativo', 'Ativo', 'Ativo', 'Ativo', 'Inativo'],
        'Último Acesso': ['2025-01-15', '2025-01-14', '2025-01-15', '2025-01-13', '2025-01-10']
    }
    
    import pandas as pd
    df_users = pd.DataFrame(users_data)
    
    if search_user:
        df_users = df_users[df_users['Nome'].str.contains(search_user, case=False) | 
                           df_users['Email'].str.contains(search_user, case=False)]
    
    if filter_role != "Todos":
        df_users = df_users[df_users['Perfil'] == filter_role]
    
    st.dataframe(df_users, use_container_width=True, hide_index=True)
    
    # Ações
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Adicionar Usuário", use_container_width=True):
            st.info("Funcionalidade de adicionar usuário será implementada")
    with col2:
        if st.button("✏️ Editar Selecionado", use_container_width=True):
            st.info("Selecione um usuário para editar")
    with col3:
        if st.button("🗑️ Remover Selecionado", use_container_width=True, type="secondary"):
            st.warning("Funcionalidade de remoção será implementada")

# ==================== TAB 2: CONFIGURAÇÕES ====================
with tab2:
    st.markdown("### 🔧 Configurações do Sistema")
    
    with st.form("system_settings"):
        st.markdown("#### Configurações Gerais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            site_name = st.text_input("Nome do Site", value="Eco-Skill Up")
            maintenance_mode = st.checkbox("Modo de Manutenção")
            allow_registration = st.checkbox("Permitir Registro de Novos Usuários", value=True)
        
        with col2:
            max_quizzes_per_day = st.number_input("Máximo de Quizzes por Dia", min_value=1, max_value=100, value=10)
            default_difficulty = st.selectbox("Dificuldade Padrão", ["Fácil", "Médio", "Difícil"])
            enable_notifications = st.checkbox("Habilitar Notificações", value=True)
        
        st.markdown("#### Configurações de Email")
        smtp_server = st.text_input("Servidor SMTP", value="smtp.example.com")
        smtp_port = st.number_input("Porta SMTP", min_value=1, max_value=65535, value=587)
        email_from = st.text_input("Email Remetente", value="noreply@ecoskillup.com")
        
        submitted = st.form_submit_button("💾 Salvar Configurações", type="primary", use_container_width=True)
        
        if submitted:
            st.success("✅ Configurações salvas com sucesso!")

# ==================== TAB 3: RELATÓRIOS ====================
with tab3:
    st.markdown("### 📊 Relatórios do Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Tipo de Relatório",
            ["Relatório de Usuários", "Relatório de Quizzes", "Relatório de Desempenho", "Relatório Financeiro"]
        )
        
        date_from = st.date_input("Data Inicial")
        date_to = st.date_input("Data Final")
    
    with col2:
        format_type = st.selectbox("Formato", ["PDF", "Excel", "CSV"])
        
        include_charts = st.checkbox("Incluir Gráficos", value=True)
        include_details = st.checkbox("Incluir Detalhes", value=True)
    
    if st.button("📥 Gerar Relatório", type="primary", use_container_width=True):
        st.success(f"✅ Relatório '{report_type}' gerado com sucesso! (Funcionalidade será implementada)")
        st.info("📄 O relatório seria baixado aqui no formato selecionado.")

# ==================== TAB 4: SEGURANÇA ====================
with tab4:
    st.markdown("### 🔐 Configurações de Segurança")
    
    st.markdown("#### Políticas de Senha")
    
    with st.form("security_settings"):
        min_password_length = st.number_input("Tamanho Mínimo da Senha", min_value=6, max_value=20, value=8)
        require_uppercase = st.checkbox("Requerer Letra Maiúscula", value=True)
        require_lowercase = st.checkbox("Requerer Letra Minúscula", value=True)
        require_numbers = st.checkbox("Requerer Números", value=True)
        require_special = st.checkbox("Requerer Caracteres Especiais", value=True)
        password_expiry_days = st.number_input("Dias para Expiração da Senha", min_value=0, max_value=365, value=90)
        
        st.markdown("#### Autenticação")
        enable_2fa = st.checkbox("Habilitar Autenticação de Dois Fatores", value=False)
        session_timeout = st.number_input("Timeout de Sessão (minutos)", min_value=5, max_value=480, value=30)
        
        st.markdown("#### Logs e Auditoria")
        enable_audit_log = st.checkbox("Habilitar Log de Auditoria", value=True)
        log_retention_days = st.number_input("Dias de Retenção de Logs", min_value=30, max_value=365, value=90)
        
        submitted = st.form_submit_button("💾 Salvar Configurações de Segurança", type="primary", use_container_width=True)
        
        if submitted:
            st.success("✅ Configurações de segurança salvas com sucesso!")

# ==================== ESTATÍSTICAS DO SISTEMA ====================
st.markdown("---")
st.markdown("### 📊 Estatísticas do Sistema")

col1, col2, col3, col4 = st.columns(4)

system_stats = [
    {"label": "Usuários Totais", "value": "156", "icon": "👥"},
    {"label": "Quizzes Ativos", "value": "24", "icon": "❓"},
    {"label": "Acessos Hoje", "value": "342", "icon": "📈"},
    {"label": "Uptime", "value": "99.9%", "icon": "⚡"}
]

for i, stat in enumerate(system_stats):
    with [col1, col2, col3, col4][i]:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                    padding: 1.5rem; border-radius: 12px; text-align: center; 
                    border: 1px solid #E0E0E0;'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{stat['icon']}</div>
            <h3 style='color: #00D4AA; font-size: 2rem; margin: 0.5rem 0;'>{stat['value']}</h3>
            <p style='color: #6C757D; margin: 0; font-size: 0.9rem;'>{stat['label']}</p>
        </div>
        """, unsafe_allow_html=True)

