"""
Sistema de autenticação integrado com API
"""

import streamlit as st
from src.frontend.utils.api import login, register

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
        
        # Tabs para Login e Registro
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Registrar"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                
                submitted = st.form_submit_button("Entrar", use_container_width=True, type="primary")
                
                if submitted:
                    if username and password:
                        if login(username, password):
                            st.success("Login realizado com sucesso!")
                            st.rerun()
                    else:
                        st.error("Por favor, preencha todos os campos.")
        
        with tab2:
            with st.form("register_form"):
                st.markdown("### Criar Nova Conta")
                
                col1, col2 = st.columns(2)
                with col1:
                    username = st.text_input("👤 Usuário", placeholder="Escolha um usuário", key="reg_username")
                    email = st.text_input("📧 Email", placeholder="seu@email.com", key="reg_email")
                    password = st.text_input("🔒 Senha", type="password", placeholder="Mínimo 6 caracteres", key="reg_password")
                
                with col2:
                    full_name = st.text_input("👨‍💼 Nome Completo", placeholder="Seu nome", key="reg_full_name")
                    phone = st.text_input("📱 Telefone", placeholder="(11) 99999-9999", key="reg_phone")
                    confirm_password = st.text_input("🔒 Confirmar Senha", type="password", placeholder="Digite novamente", key="reg_confirm_password")
                
                submitted = st.form_submit_button("Criar Conta", use_container_width=True, type="primary")
                
                if submitted:
                    if not username or not email or not password:
                        st.error("Por favor, preencha pelo menos usuário, email e senha.")
                    elif password != confirm_password:
                        st.error("As senhas não coincidem.")
                    elif len(password) < 6:
                        st.error("A senha deve ter pelo menos 6 caracteres.")
                    else:
                        user_data = {
                            "username": username,
                            "email": email,
                            "password": password,
                            "full_name": full_name if full_name else None,
                            "phone": phone if phone else None
                        }
                        if register(user_data):
                            st.success("Conta criada com sucesso! Você já está logado.")
                            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #6C757D; font-size: 0.9rem;'>
            <p>💡 Use as credenciais criadas no seed para fazer login</p>
        </div>
        """, unsafe_allow_html=True)

def check_authentication():
    """Verifica se o usuário está autenticado"""
    if not st.session_state.get('is_authenticated', False):
        login_page()
        return False
    return True

