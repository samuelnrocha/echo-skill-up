"""
Componente de Sidebar reutilizável para área interna
"""

import streamlit as st
from src.frontend.components.theme import apply_theme

def render_sidebar():
    """Renderiza a sidebar da área interna"""
    with st.sidebar:
        # Logo e título
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='color: #00D4AA; margin: 0;'>🌱 Eco-Skill Up</h2>
            <p style='color: #6C757D; font-size: 0.9rem; margin: 0;'>Plataforma de Aprendizado</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navegação principal
        st.markdown("### 📊 Menu Principal")
        
        page = st.selectbox(
            "Navegar para:",
            [
                "🏠 Dashboard",
                "❓ Quizzes",
                "📚 Gerenciar Conteúdo",
                "📈 Estatísticas",
                "🏆 Placar de Líderes",
                "⚙️ Administração",
                "👤 Perfil"
            ],
            key="nav_select"
        )
        
        st.divider()
        
        # Informações do usuário
        if st.session_state.get('current_user'):
            st.markdown(f"**👤 Usuário:** {st.session_state.current_user.get('username', 'Demo User')}")
            st.markdown(f"**🎯 Pontuação Total:** {st.session_state.current_user.get('total_score', 0)}")
        
        st.divider()
        
        # Toggle de tema
        theme_label = "🌙 Modo Escuro" if st.session_state.get('theme', 'light') == 'light' else "☀️ Modo Claro"
        if st.button(theme_label, use_container_width=True):
            if st.session_state.theme == 'light':
                st.session_state.theme = 'dark'
            else:
                st.session_state.theme = 'light'
            st.rerun()
        
        # Botão de logout
        if st.button("🚪 Sair", use_container_width=True, type="secondary"):
            st.session_state.is_authenticated = False
            st.session_state.current_user = None
            st.rerun()
        
        return page

def get_page_route(page_name):
    """Mapeia o nome da página para a rota"""
    routes = {
        "🏠 Dashboard": "1_Dashboard.py",
        "❓ Quizzes": "2_Quizzes.py",
        "📚 Gerenciar Conteúdo": "3_Gerenciar_Conteudo.py",
        "📈 Estatísticas": "4_Estatisticas.py",
        "🏆 Placar de Líderes": "5_Placar.py",
        "⚙️ Administração": "6_Administracao.py",
        "👤 Perfil": "7_Perfil.py"
    }
    return routes.get(page_name, "1_Dashboard.py")

