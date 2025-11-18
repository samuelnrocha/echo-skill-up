"""
Página de Perfil do Usuário
"""

import streamlit as st
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication

# Configuração
st.set_page_config(
    page_title="Perfil - Eco-Skill Up",
    page_icon="👤",
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
render_header("👤 Meu Perfil", "Gerencie suas informações pessoais e preferências")

# ==================== INFORMAÇÕES DO PERFIL ====================
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 16px; 
                border: 1px solid #E0E0E0; text-align: center;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>👤</div>
        <h3 style='color: #1E1E1E; margin: 0.5rem 0;'>
            {username}
        </h3>
        <p style='color: #6C757D; margin: 0.5rem 0;'>Membro desde Jan 2025</p>
        <div style='background: #00D4AA; color: white; padding: 0.5rem 1rem; 
                    border-radius: 8px; margin: 1rem 0; display: inline-block;'>
            Nível Avançado
        </div>
    </div>
    """.format(username=st.session_state.current_user.get('username', 'Usuário')), unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                border: 1px solid #E0E0E0; margin-top: 1rem;'>
        <h4 style='color: #1E1E1E; margin: 0 0 1rem 0;'>📊 Estatísticas Rápidas</h4>
        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
            <span style='color: #6C757D;'>Pontuação Total:</span>
            <strong style='color: #00D4AA;'>1,250</strong>
        </div>
        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
            <span style='color: #6C757D;'>Quizzes:</span>
            <strong style='color: #00D4AA;'>24</strong>
        </div>
        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
            <span style='color: #6C757D;'>Conquistas:</span>
            <strong style='color: #00D4AA;'>8</strong>
        </div>
        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
            <span style='color: #6C757D;'>Ranking:</span>
            <strong style='color: #00D4AA;'>#12</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Formulário de edição
    st.markdown("### ✏️ Editar Informações")
    
    with st.form("edit_profile"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("Nome", value="Demo")
            email = st.text_input("Email", value="demo@email.com")
            phone = st.text_input("Telefone", value="(11) 99999-9999")
        
        with col2:
            last_name = st.text_input("Sobrenome", value="User")
            username = st.text_input("Usuário", value=st.session_state.current_user.get('username', 'demo_user'))
            birth_date = st.date_input("Data de Nascimento")
        
        bio = st.text_area("Biografia", placeholder="Conte um pouco sobre você...", height=100)
        
        st.markdown("#### Preferências de Aprendizado")
        
        col1, col2 = st.columns(2)
        with col1:
            preferred_topics = st.multiselect(
                "Tópicos de Interesse",
                ["Prompt Engineering", "Python", "IA", "Machine Learning", 
                 "Banco de Dados", "R", "Sustentabilidade", "Economia Verde"],
                default=["Python", "IA"]
            )
            difficulty_preference = st.selectbox(
                "Dificuldade Preferida",
                ["Fácil", "Médio", "Difícil", "Avançado"]
            )
        
        with col2:
            daily_goal = st.number_input("Meta Diária de Quizzes", min_value=1, max_value=20, value=5)
            notification_preference = st.selectbox(
                "Preferência de Notificações",
                ["Todas", "Apenas Importantes", "Nenhuma"]
            )
        
        submitted = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
        
        if submitted:
            st.success("✅ Perfil atualizado com sucesso!")

# ==================== CONQUISTAS ====================
st.markdown("---")
st.markdown("### 🏅 Conquistas e Badges")

col1, col2, col3, col4 = st.columns(4)

badges = [
    {"name": "Primeiro Quiz", "icon": "🎯", "earned": True, "date": "2025-01-01"},
    {"name": "10 Quizzes", "icon": "⭐", "earned": True, "date": "2025-01-05"},
    {"name": "Mestre Python", "icon": "🐍", "earned": True, "date": "2025-01-10"},
    {"name": "Sustentabilidade", "icon": "🌱", "earned": True, "date": "2025-01-12"},
    {"name": "50 Quizzes", "icon": "🔥", "earned": False, "date": None},
    {"name": "Perfeccionista", "icon": "💯", "earned": False, "date": None},
    {"name": "Velocista", "icon": "⚡", "earned": False, "date": None},
    {"name": "Lenda", "icon": "👑", "earned": False, "date": None}
]

for i, badge in enumerate(badges):
    with [col1, col2, col3, col4][i % 4]:
        opacity = "1" if badge['earned'] else "0.3"
        border_color = "#00D4AA" if badge['earned'] else "#E0E0E0"
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                    border: 2px solid {border_color}; text-align: center; opacity: {opacity};'>
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>{badge['icon']}</div>
            <h4 style='color: #1E1E1E; margin: 0.5rem 0;'>{badge['name']}</h4>
            {f"<p style='color: #6C757D; font-size: 0.8rem; margin: 0;'>Conquistado em {badge['date']}</p>" if badge['earned'] else "<p style='color: #6C757D; font-size: 0.8rem; margin: 0;'>Bloqueado</p>"}
        </div>
        """, unsafe_allow_html=True)

# ==================== HISTÓRICO DE ATIVIDADES ====================
st.markdown("---")
st.markdown("### 📜 Histórico de Atividades")

activities = [
    {"action": "Quiz completado", "details": "Sustentabilidade - Nível Médio", "points": "+10", "date": "2025-01-15 14:30"},
    {"action": "Conquista desbloqueada", "details": "Mestre Python", "points": "", "date": "2025-01-10 10:15"},
    {"action": "Nível aumentado", "details": "Avançado", "points": "", "date": "2025-01-08 16:45"},
    {"action": "Quiz completado", "details": "Machine Learning - Nível Difícil", "points": "+8", "date": "2025-01-05 09:20"},
]

for activity in activities:
    st.markdown(f"""
    <div style='background: white; padding: 1rem; border-radius: 12px; 
                border: 1px solid #E0E0E0; margin: 0.5rem 0; 
                display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #1E1E1E;'>{activity['action']}</strong>
            <p style='color: #6C757D; margin: 0.3rem 0 0 0; font-size: 0.9rem;'>{activity['details']}</p>
        </div>
        <div style='text-align: right;'>
            {f"<span style='color: #00D4AA; font-weight: bold;'>{activity['points']}</span>" if activity['points'] else ""}
            <p style='color: #6C757D; margin: 0.3rem 0 0 0; font-size: 0.8rem;'>{activity['date']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== CONFIGURAÇÕES DE CONTA ====================
st.markdown("---")
st.markdown("### ⚙️ Configurações de Conta")

with st.expander("🔐 Alterar Senha"):
    with st.form("change_password"):
        current_password = st.text_input("Senha Atual", type="password")
        new_password = st.text_input("Nova Senha", type="password")
        confirm_password = st.text_input("Confirmar Nova Senha", type="password")
        
        if st.form_submit_button("🔒 Alterar Senha", type="primary"):
            if new_password == confirm_password:
                st.success("✅ Senha alterada com sucesso!")
            else:
                st.error("❌ As senhas não coincidem.")

with st.expander("🗑️ Excluir Conta"):
    st.warning("⚠️ Esta ação é irreversível. Todos os seus dados serão permanentemente removidos.")
    if st.button("🗑️ Excluir Minha Conta", type="secondary"):
        st.error("Funcionalidade de exclusão será implementada com confirmação adicional.")

