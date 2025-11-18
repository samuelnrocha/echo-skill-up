"""
Página de Quizzes Interativos
"""

import streamlit as st
import requests
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication

# Configuração
st.set_page_config(
    page_title="Quizzes - Eco-Skill Up",
    page_icon="❓",
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
render_header("❓ Quizzes Interativos", "Teste seus conhecimentos e ganhe pontos")

# URL da API
API_URL = "http://127.0.0.1:8000"

# ==================== SELEÇÃO DE TÓPICO ====================
st.markdown("### 📚 Selecione um Tópico")

topics = [
    "Prompt Engineering",
    "Python",
    "IA",
    "Machine Learning",
    "Banco de Dados",
    "R",
    "Sustentabilidade",
    "Economia Verde"
]

col1, col2, col3, col4 = st.columns(4)

selected_topic = None
for i, topic in enumerate(topics):
    with [col1, col2, col3, col4][i % 4]:
        if st.button(f"📖 {topic}", use_container_width=True, key=f"topic_{i}"):
            selected_topic = topic
            st.session_state.selected_topic = topic

# Usa tópico da sessão ou padrão
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = "Prompt Engineering"

current_topic = st.session_state.get('selected_topic', "Prompt Engineering")

st.markdown("---")

# ==================== QUIZ ====================
st.markdown(f"### 🎯 Quiz: {current_topic}")

try:
    # Carrega quiz da API
    response = requests.get(f"{API_URL}/quiz/{current_topic}")
    response.raise_for_status()
    
    quiz_data = response.json().get("quiz")
    
    if quiz_data:
        # Card do quiz
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 16px; 
                    border: 2px solid #E0E0E0; margin: 1rem 0;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                <span style='background: #00D4AA; color: white; padding: 0.5rem 1rem; 
                            border-radius: 8px; font-size: 0.9rem;'>
                    {quiz_data['difficulty']}
                </span>
                <span style='color: #6C757D; font-size: 0.9rem;'>
                    Tópico: {quiz_data['topic']}
                </span>
            </div>
            <h3 style='color: #1E1E1E; margin: 1rem 0; font-size: 1.3rem;'>
                {quiz_data['question_text']}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Opções de resposta
        option_texts = [opt['text'] for opt in quiz_data['options']]
        selected_text = st.radio(
            "Selecione sua resposta:",
            option_texts,
            key=f"quiz_{quiz_data['id_quiz']}",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✅ Enviar Resposta", type="primary", use_container_width=True):
                # Encontra o ID da opção selecionada
                selected_option_id = next(
                    opt['id'] for opt in quiz_data['options'] 
                    if opt['text'] == selected_text
                )
                
                # Verifica a resposta
                is_correct = (selected_option_id == quiz_data['correct_answer_id'])
                score = 10.0 if is_correct else 0.0
                
                # Envia o score para a API
                user_id = st.session_state.current_user.get('id', 1)
                score_payload = {
                    "user_id": user_id,
                    "quiz_id": quiz_data['id_quiz'],
                    "score": score
                }
                
                try:
                    requests.post(f"{API_URL}/submit-score", json=score_payload)
                except:
                    pass
                
                # Feedback visual
                if is_correct:
                    st.success("🎉 Correto! Pontuação registrada.")
                    st.balloons()
                else:
                    st.error("❌ Incorreta. Tente novamente!")
                
                # Feedback da IA
                try:
                    ml_response = requests.get(f"{API_URL}/predict-difficulty/{user_id}")
                    ml_data = ml_response.json()
                    st.info(f"🤖 **Feedback da IA:** {ml_data['feedback_message']}")
                except:
                    pass
                
                # Limpa a seleção para novo quiz
                if 'quiz_' + str(quiz_data['id_quiz']) in st.session_state:
                    del st.session_state['quiz_' + str(quiz_data['id_quiz'])]
                st.rerun()
        
        with col2:
            if st.button("🔄 Novo Quiz", use_container_width=True):
                if 'quiz_' + str(quiz_data['id_quiz']) in st.session_state:
                    del st.session_state['quiz_' + str(quiz_data['id_quiz'])]
                st.rerun()
    
    else:
        st.error("Não foi possível carregar o quiz. Tente novamente.")

except requests.exceptions.ConnectionError:
    st.error("""
    ⚠️ **Erro de Conexão**
    
    A API backend não está rodando. Por favor:
    1. Abra um terminal
    2. Navegue até `src/backend`
    3. Execute: `python main.py`
    """)
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

# ==================== ESTATÍSTICAS DO QUIZ ====================
st.markdown("---")
st.markdown("### 📊 Suas Estatísticas de Quiz")

col1, col2, col3 = st.columns(3)

stats = [
    {"label": "Taxa de Acerto", "value": "85%", "icon": "🎯"},
    {"label": "Quizzes Completos", "value": "24", "icon": "✅"},
    {"label": "Pontuação Média", "value": "8.5", "icon": "⭐"}
]

for i, stat in enumerate(stats):
    with [col1, col2, col3][i]:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                    padding: 1.5rem; border-radius: 12px; text-align: center; 
                    border: 1px solid #E0E0E0;'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{stat['icon']}</div>
            <h3 style='color: #00D4AA; font-size: 2rem; margin: 0.5rem 0;'>{stat['value']}</h3>
            <p style='color: #6C757D; margin: 0;'>{stat['label']}</p>
        </div>
        """, unsafe_allow_html=True)

