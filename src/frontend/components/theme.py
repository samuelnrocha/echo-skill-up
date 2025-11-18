"""
Sistema de temas claro/escuro para a aplicação Streamlit
"""

import streamlit as st

def init_theme():
    """Inicializa o sistema de temas"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

def get_theme_css(theme='light'):
    """Retorna o CSS customizado baseado no tema"""
    if theme == 'dark':
        return """
        <style>
        :root {
            --primary-color: #00D4AA;
            --secondary-color: #006B5A;
            --background-color: #0E1117;
            --surface-color: #262730;
            --text-primary: #FAFAFA;
            --text-secondary: #B0B0B0;
            --border-color: #3A3A4A;
            --success-color: #00D4AA;
            --warning-color: #FFB800;
            --error-color: #FF4444;
        }
        
        .stApp {
            background-color: var(--background-color);
            color: var(--text-primary);
        }
        
        .main .block-container {
            background-color: var(--background-color);
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
        }
        
        .card {
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .metric-card {
            background: linear-gradient(135deg, var(--surface-color) 0%, var(--border-color) 100%);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }
        </style>
        """
    else:
        return """
        <style>
        :root {
            --primary-color: #00D4AA;
            --secondary-color: #006B5A;
            --background-color: #FFFFFF;
            --surface-color: #F8F9FA;
            --text-primary: #1E1E1E;
            --text-secondary: #6C757D;
            --border-color: #E0E0E0;
            --success-color: #00D4AA;
            --warning-color: #FFB800;
            --error-color: #FF4444;
        }
        
        .stApp {
            background-color: var(--background-color);
            color: var(--text-primary);
        }
        
        .main .block-container {
            background-color: var(--background-color);
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
        }
        
        .card {
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .metric-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .hero-section {
            background: linear-gradient(135deg, #00D4AA 0%, #006B5A 100%);
            color: white;
            padding: 4rem 2rem;
            border-radius: 16px;
            margin: 2rem 0;
        }
        </style>
        """

def apply_theme(theme='light'):
    """Aplica o tema à página"""
    css = get_theme_css(theme)
    st.markdown(css, unsafe_allow_html=True)

def toggle_theme():
    """Alterna entre tema claro e escuro"""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

