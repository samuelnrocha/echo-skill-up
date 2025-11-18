"""
Sistema de autenticação simples para a aplicação
"""

import streamlit as st

def login_page():
    """Renderiza a página de login"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 5rem auto;
        padding: 2rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #00D4AA;'>🌱 Eco-Skill Up</h1>
            <p style='color: #6C757D;'>Sistema Gamificado de Aprendizado</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            
            submitted = st.form_submit_button("Entrar", use_container_width=True, type="primary")
            
            if submitted:
                # Autenticação simples (em produção, usar hash e banco de dados)
                if username and password:
                    # Para demo, aceita qualquer usuário/senha
                    st.session_state.is_authenticated = True
                    st.session_state.current_user = {
                        'username': username,
                        'id': 1,
                        'total_score': 0
                    }
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos.")
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #6C757D; font-size: 0.9rem;'>
            <p>💡 <strong>Demo:</strong> Use qualquer usuário e senha para entrar</p>
        </div>
        """, unsafe_allow_html=True)

def check_authentication():
    """Verifica se o usuário está autenticado"""
    if not st.session_state.get('is_authenticated', False):
        login_page()
        return False
    return True

