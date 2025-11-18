"""
Página de Gerenciamento de Conteúdo
"""

import streamlit as st
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication
from src.frontend.utils.api import api_request
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

# Verifica se é admin
is_admin = st.session_state.current_user.get('role') == 'admin'

if not is_admin:
    st.warning("⚠️ Apenas administradores podem gerenciar conteúdo.")
    st.stop()

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
            if question and option1 and option2:
                # Busca IDs de tópico e dificuldade
                topics_response = api_request("GET", "/quizzes", params={"limit": 1})
                if topics_response and topics_response.status_code == 200:
                    # Cria opções
                    options_list = [
                        {"text": option1, "is_correct": correct_answer == "Opção 1"},
                        {"text": option2, "is_correct": correct_answer == "Opção 2"}
                    ]
                    if option3:
                        options_list.append({"text": option3, "is_correct": correct_answer == "Opção 3"})
                    if option4:
                        options_list.append({"text": option4, "is_correct": correct_answer == "Opção 4"})
                    
                    # Mapeia tópico e dificuldade (simplificado - em produção buscar da API)
                    topic_map = {
                        "Prompt Engineering": 1, "Python": 2, "IA": 3, "Machine Learning": 4,
                        "Banco de Dados": 5, "R": 6, "Sustentabilidade": 7, "Economia Verde": 8
                    }
                    difficulty_map = {"Fácil": 1, "Médio": 2, "Difícil": 3}
                    
                    quiz_data = {
                        "question_text": question,
                        "id_topic": topic_map.get(topic, 1),
                        "id_difficulty": difficulty_map.get(difficulty, 1),
                        "options": options_list
                    }
                    
                    create_response = api_request("POST", "/quizzes", json=quiz_data)
                    if create_response and create_response.status_code == 200:
                        st.success("✅ Quiz criado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao criar quiz. Verifique os dados.")
                else:
                    st.error("❌ Erro ao buscar informações necessárias.")
            else:
                st.error("⚠️ Por favor, preencha pelo menos a pergunta e 2 opções.")

# ==================== TAB 2: LISTAR CONTEÚDO ====================
with tab2:
    st.markdown("### 📋 Conteúdo Disponível")
    
    # Filtros
    col1, col2 = st.columns(2)
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
    
    # Busca quizzes da API
    quiz_params = {}
    if filter_topic != "Todos":
        quiz_params["topic"] = filter_topic
    if filter_difficulty != "Todas":
        quiz_params["difficulty"] = filter_difficulty
    
    quizzes_response = api_request("GET", "/quizzes", params=quiz_params)
    quizzes = quizzes_response.json() if quizzes_response and quizzes_response.status_code == 200 else []
    
    # Exibe quizzes
    if quizzes:
        for quiz in quizzes:
            with st.expander(f"📝 {quiz.get('question_text', '')[:60]}..."):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**Pergunta completa:** {quiz.get('question_text', '')}")
                with col2:
                    st.write(f"**Tópico:** {quiz.get('topic', 'N/A')}")
                    st.write(f"**Dificuldade:** {quiz.get('difficulty', 'N/A')}")
                with col3:
                    st.write(f"**ID:** {quiz.get('id_quiz', 'N/A')}")
                    quiz_id = quiz.get('id_quiz')
                    if st.button("🗑️ Deletar", key=f"delete_{quiz_id}"):
                        delete_response = api_request("DELETE", f"/quizzes/{quiz_id}")
                        if delete_response and delete_response.status_code == 200:
                            st.success("✅ Quiz deletado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao deletar quiz.")
    else:
        st.info("Nenhum quiz encontrado com os filtros selecionados.")

# ==================== TAB 3: EDITAR CONTEÚDO ====================
with tab3:
    st.markdown("### ✏️ Editar Conteúdo Existente")
    
    # Busca todos os quizzes
    all_quizzes_response = api_request("GET", "/quizzes")
    all_quizzes = all_quizzes_response.json() if all_quizzes_response and all_quizzes_response.status_code == 200 else []
    
    if all_quizzes:
        quiz_options = {f"ID {q.get('id_quiz')}: {q.get('question_text', '')[:50]}...": q.get('id_quiz') 
                       for q in all_quizzes}
        selected_quiz_name = st.selectbox(
            "Selecione o quiz para editar",
            options=["Selecione um quiz..."] + list(quiz_options.keys())
        )
        
        if selected_quiz_name != "Selecione um quiz...":
            quiz_id = quiz_options[selected_quiz_name]
            quiz_response = api_request("GET", f"/quizzes/{quiz_id}")
            
            if quiz_response and quiz_response.status_code == 200:
                quiz_data = quiz_response.json()
                st.info("📝 Funcionalidade de edição completa será implementada em breve. Use a API diretamente para editar quizzes.")
                st.json(quiz_data)
            else:
                st.error("Não foi possível carregar os dados do quiz.")
    else:
        st.info("Nenhum quiz disponível para editar.")

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

