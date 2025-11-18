"""
Página de Perfil do Usuário
"""

import streamlit as st
from datetime import datetime
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication
from src.frontend.utils.api import api_request  

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

# Busca dados do usuário
user_response = api_request("GET", "/users/me")
user_data = user_response.json() if user_response and user_response.status_code == 200 else {}

# Busca estatísticas
stats_response = api_request("GET", "/users/me/stats")
stats = stats_response.json() if stats_response and stats_response.status_code == 200 else {}

# Calcula nível
total_score = stats.get("total_score", 0)
if total_score < 50:
    level = "Iniciante"
elif total_score < 150:
    level = "Intermediário"
elif total_score < 300:
    level = "Avançado"
else:
    level = "Expert"

# Formata data de criação
created_at = user_data.get('created_at', '')
if created_at:
    try:
        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        created_str = dt.strftime("%b %Y")
    except:
        created_str = "Recentemente"
else:
    created_str = "Recentemente"

# ==================== INFORMAÇÕES DO PERFIL ====================
col1, col2 = st.columns([1, 2])

with col1:
    username = user_data.get('username', st.session_state.current_user.get('username', 'Usuário'))
    full_name = user_data.get('full_name', username)
    
    st.markdown(f"""
    <div style='background: white; padding: 2rem; border-radius: 16px; 
                border: 1px solid #E0E0E0; text-align: center;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>👤</div>
        <h3 style='color: #1E1E1E; margin: 0.5rem 0;'>
            {full_name}
        </h3>
        <p style='color: #6C757D; margin: 0.5rem 0;'>Membro desde {created_str}</p>
        <div style='background: #00D4AA; color: white; padding: 0.5rem 1rem; 
                    border-radius: 8px; margin: 1rem 0; display: inline-block;'>
            {level}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                border: 1px solid #E0E0E0; margin-top: 1rem;'>
        <h4 style='color: #1E1E1E; margin: 0 0 1rem 0;'>📊 Estatísticas Rápidas</h4>
        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
            <span style='color: #6C757D;'>Pontuação Total:</span>
            <strong style='color: #00D4AA;'>{int(stats.get('total_score', 0)):,}</strong>
        </div>
        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
            <span style='color: #6C757D;'>Quizzes:</span>
            <strong style='color: #00D4AA;'>{stats.get('quizzes_completed', 0)}</strong>
        </div>
        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
            <span style='color: #6C757D;'>Taxa de Acerto:</span>
            <strong style='color: #00D4AA;'>{stats.get('accuracy', 0):.1f}%</strong>
        </div>
        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
            <span style='color: #6C757D;'>Pontuação Média:</span>
            <strong style='color: #00D4AA;'>{stats.get('average_score', 0):.1f}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Formulário de edição
    st.markdown("### ✏️ Editar Informações")
    
    with st.form("edit_profile"):
        full_name = st.text_input("Nome Completo", value=user_data.get('full_name', ''))
        email = st.text_input("Email", value=user_data.get('email', ''))
        phone = st.text_input("Telefone", value=user_data.get('phone', ''))
        bio = st.text_area("Biografia", value=user_data.get('bio', ''), placeholder="Conte um pouco sobre você...", height=100)
        
        submitted = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
        
        if submitted:
            # Atualiza perfil
            update_data = {}
            if full_name:
                update_data['full_name'] = full_name
            if email:
                update_data['email'] = email
            if phone:
                update_data['phone'] = phone
            if bio:
                update_data['bio'] = bio
            
            if update_data:
                update_response = api_request("PUT", "/users/me", json=update_data)
                if update_response and update_response.status_code == 200:
                    st.success("✅ Perfil atualizado com sucesso!")
                    # Atualiza dados na sessão
                    updated_user = update_response.json()
                    st.session_state.current_user.update(updated_user)
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar perfil. Tente novamente.")
            else:
                st.info("Nenhuma alteração foi feita.")

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

activities_response = api_request("GET", "/users/me/activities", params={"limit": 10})
if activities_response and activities_response.status_code == 200:
    activities = activities_response.json()
    
    if activities:
        for activity in activities:
            timestamp = activity.get('timestamp', '')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    date_str = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    date_str = timestamp
            else:
                date_str = "Recentemente"
            
            score = activity.get('score', 0)
            points_str = f"+{int(score)}" if score > 0 else ""
            
            st.markdown(f"""
            <div style='background: white; padding: 1rem; border-radius: 12px; 
                        border: 1px solid #E0E0E0; margin: 0.5rem 0; 
                        display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <strong style='color: #1E1E1E;'>{activity.get('action', 'Quiz completado')}</strong>
                    <p style='color: #6C757D; margin: 0.3rem 0 0 0; font-size: 0.9rem;'>
                        {activity.get('topic', 'N/A')} - {activity.get('difficulty', 'N/A')}
                    </p>
                </div>
                <div style='text-align: right;'>
                    {f"<span style='color: #00D4AA; font-weight: bold;'>{points_str}</span>" if points_str else ""}
                    <p style='color: #6C757D; margin: 0.3rem 0 0 0; font-size: 0.8rem;'>{date_str}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma atividade registrada ainda.")
else:
    st.info("Não foi possível carregar o histórico de atividades.")

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

