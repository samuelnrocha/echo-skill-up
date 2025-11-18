"""
Página de Gerenciamento de Conteúdo
"""

import streamlit as st
import requests
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication

# Configuração
st.set_page_config(
    page_title="Gerenciar Conteúdo - Eco-Skill Up",
    page_icon="📚",
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
render_header("📚 Gerenciar Conteúdo", "Crie e gerencie quizzes, módulos e materiais educacionais")

# URL da API
API_URL = "http://127.0.0.1:8000"

# ==================== TABS ====================
tab1, tab2, tab3 = st.tabs(["➕ Criar Quiz", "📋 Listar Conteúdo", "✏️ Editar Conteúdo"])

# ==================== TAB 1: CRIAR QUIZ ====================
with tab1:
    st.markdown("### ➕ Criar Novo Quiz")
    
    with st.form("create_quiz_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.selectbox(
                "Tópico",
                ["Prompt Engineering", "Python", "IA", "Machine Learning", 
                 "Banco de Dados", "R", "Sustentabilidade", "Economia Verde"]
            )
            difficulty = st.selectbox(
                "Dificuldade",
                ["Fácil", "Médio", "Difícil"]
            )
        
        with col2:
            question = st.text_area(
                "Pergunta",
                placeholder="Digite a pergunta do quiz...",
                height=100
            )
        
        st.markdown("#### Opções de Resposta")
        
        col1, col2 = st.columns(2)
        with col1:
            option1 = st.text_input("Opção 1", key="opt1")
            option2 = st.text_input("Opção 2", key="opt2")
        with col2:
            option3 = st.text_input("Opção 3", key="opt3")
            option4 = st.text_input("Opção 4", key="opt4")
        
        correct_answer = st.radio(
            "Resposta Correta",
            ["Opção 1", "Opção 2", "Opção 3", "Opção 4"]
        )
        
        submitted = st.form_submit_button("💾 Salvar Quiz", type="primary", use_container_width=True)
        
        if submitted:
            if question and option1 and option2 and option3 and option4:
                st.success("✅ Quiz criado com sucesso! (Funcionalidade de criação via API será implementada)")
            else:
                st.error("⚠️ Por favor, preencha todos os campos.")

# ==================== TAB 2: LISTAR CONTEÚDO ====================
with tab2:
    st.markdown("### 📋 Conteúdo Disponível")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_topic = st.selectbox(
            "Filtrar por Tópico",
            ["Todos"] + ["Prompt Engineering", "Python", "IA", "Machine Learning", 
                        "Banco de Dados", "R", "Sustentabilidade", "Economia Verde"]
        )
    with col2:
        filter_difficulty = st.selectbox(
            "Filtrar por Dificuldade",
            ["Todas", "Fácil", "Médio", "Difícil"]
        )
    with col3:
        search = st.text_input("🔍 Buscar", placeholder="Digite para buscar...")
    
    # Lista de quizzes (mockado)
    quizzes = [
        {"id": 1, "question": "O que é um prompt em sistemas de IA?", "topic": "Prompt Engineering", "difficulty": "Médio", "status": "Ativo"},
        {"id": 2, "question": "Qual é a forma correta de criar uma lista em Python?", "topic": "Python", "difficulty": "Fácil", "status": "Ativo"},
        {"id": 3, "question": "O que significa 'Economia Verde'?", "topic": "Sustentabilidade", "difficulty": "Fácil", "status": "Ativo"},
        {"id": 4, "question": "Qual é a diferença entre regressão e classificação?", "topic": "Machine Learning", "difficulty": "Difícil", "status": "Ativo"},
    ]
    
    # Aplica filtros
    filtered_quizzes = quizzes
    if filter_topic != "Todos":
        filtered_quizzes = [q for q in filtered_quizzes if q['topic'] == filter_topic]
    if filter_difficulty != "Todas":
        filtered_quizzes = [q for q in filtered_quizzes if q['difficulty'] == filter_difficulty]
    if search:
        filtered_quizzes = [q for q in filtered_quizzes if search.lower() in q['question'].lower()]
    
    # Exibe quizzes
    for quiz in filtered_quizzes:
        with st.expander(f"📝 {quiz['question'][:60]}..."):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**Pergunta completa:** {quiz['question']}")
            with col2:
                st.write(f"**Tópico:** {quiz['topic']}")
                st.write(f"**Dificuldade:** {quiz['difficulty']}")
            with col3:
                st.write(f"**Status:** {quiz['status']}")
                if st.button("✏️ Editar", key=f"edit_{quiz['id']}"):
                    st.info("Funcionalidade de edição será implementada")

# ==================== TAB 3: EDITAR CONTEÚDO ====================
with tab3:
    st.markdown("### ✏️ Editar Conteúdo Existente")
    
    quiz_to_edit = st.selectbox(
        "Selecione o quiz para editar",
        ["Selecione um quiz..."] + [f"Quiz {i}: {q['question'][:50]}..." for i, q in enumerate(quizzes, 1)]
    )
    
    if quiz_to_edit != "Selecione um quiz...":
        st.info("📝 Formulário de edição será carregado aqui. (Funcionalidade será implementada)")

# ==================== ESTATÍSTICAS DE CONTEÚDO ====================
st.markdown("---")
st.markdown("### 📊 Estatísticas de Conteúdo")

col1, col2, col3, col4 = st.columns(4)

content_stats = [
    {"label": "Total de Quizzes", "value": "24", "icon": "❓"},
    {"label": "Tópicos Ativos", "value": "8", "icon": "📚"},
    {"label": "Usuários Ativos", "value": "156", "icon": "👥"},
    {"label": "Taxa de Completude", "value": "78%", "icon": "✅"}
]

for i, stat in enumerate(content_stats):
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

