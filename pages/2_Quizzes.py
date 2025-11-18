"""
Página de Quizzes Interativos
"""

import streamlit as st
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication
from src.frontend.utils.api import api_request

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

# ==================== SELEÇÃO DE QUIZ ====================
st.markdown("### 📚 Selecione um Quiz")

# Busca quizzes disponíveis
available_response = api_request("GET", "/quizzes/available")
if available_response and available_response.status_code == 200:
    available_quizzes = available_response.json()
    
    if available_quizzes:
        # Se há um quiz selecionado na sessão, usa ele
        selected_quiz_id = st.session_state.get('selected_quiz_id')
        
        if not selected_quiz_id and available_quizzes:
            selected_quiz_id = available_quizzes[0].get('id_quiz')
        
        # Lista de quizzes para seleção
        quiz_options = {f"{q.get('topic', 'Quiz')} - {q.get('question_text', '')[:50]}...": q.get('id_quiz') 
                       for q in available_quizzes}
        
        selected_quiz_name = st.selectbox(
            "Escolha um quiz para responder:",
            options=list(quiz_options.keys()),
            index=0 if not selected_quiz_id else next((i for i, qid in enumerate(quiz_options.values()) if qid == selected_quiz_id), 0)
        )
        
        selected_quiz_id = quiz_options[selected_quiz_name]
        st.session_state.selected_quiz_id = selected_quiz_id
        
        st.markdown("---")
        
        # ==================== EXIBIR QUIZ ====================
        # Busca detalhes do quiz selecionado
        quiz_response = api_request("GET", f"/quizzes/{selected_quiz_id}")
        
        if quiz_response and quiz_response.status_code == 200:
            quiz_data = quiz_response.json()
            
            # Card do quiz
            st.markdown(f"""
            <div style='background: white; padding: 2rem; border-radius: 16px; 
                        border: 2px solid #E0E0E0; margin: 1rem 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                    <span style='background: #00D4AA; color: white; padding: 0.5rem 1rem; 
                                border-radius: 8px; font-size: 0.9rem;'>
                        {quiz_data.get('difficulty', 'N/A')}
                    </span>
                    <span style='color: #6C757D; font-size: 0.9rem;'>
                        Tópico: {quiz_data.get('topic', 'N/A')}
                    </span>
                </div>
                <h3 style='color: #1E1E1E; margin: 1rem 0; font-size: 1.3rem;'>
                    {quiz_data.get('question_text', '')}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Opções de resposta
            options = quiz_data.get('options', [])
            if options:
                option_texts = [opt['text'] for opt in options]
                selected_text = st.radio(
                    "Selecione sua resposta:",
                    option_texts,
                    key=f"quiz_option_{selected_quiz_id}",
                    label_visibility="visible"
                )
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("✅ Enviar Resposta", type="primary", use_container_width=True):
                        # Encontra o ID da opção selecionada
                        selected_option = next(
                            opt for opt in options 
                            if opt['text'] == selected_text
                        )
                        
                        # Envia resposta
                        answer_response = api_request(
                            "POST",
                            f"/quizzes/{selected_quiz_id}/answer",
                            json={
                                "quiz_id": selected_quiz_id,
                                "option_id": selected_option['id']
                            }
                        )
                        
                        if answer_response and answer_response.status_code == 200:
                            result = answer_response.json()
                            
                            # Feedback visual
                            if result.get('correct', False):
                                st.success(f"🎉 {result.get('message', 'Correto!')} Pontuação: {result.get('score', 0)}")
                                st.balloons()
                            else:
                                st.error(f"❌ {result.get('message', 'Incorreto.')}")
                            
                            # Limpa seleção e recarrega
                            if f"quiz_option_{selected_quiz_id}" in st.session_state:
                                del st.session_state[f"quiz_option_{selected_quiz_id}"]
                            
                            # Remove quiz da lista de disponíveis
                            if 'selected_quiz_id' in st.session_state:
                                del st.session_state['selected_quiz_id']
                            
                            st.rerun()
                
                with col2:
                    if st.button("🔄 Novo Quiz", use_container_width=True):
                        if 'selected_quiz_id' in st.session_state:
                            del st.session_state['selected_quiz_id']
                        if f"quiz_option_{selected_quiz_id}" in st.session_state:
                            del st.session_state[f"quiz_option_{selected_quiz_id}"]
                        st.rerun()
        else:
            st.error("Não foi possível carregar o quiz selecionado.")
    else:
        st.info("🎉 Parabéns! Você completou todos os quizzes disponíveis!")
        st.markdown("Volte mais tarde para novos desafios ou crie novos quizzes na página de Gerenciar Conteúdo.")
else:
    st.error("Não foi possível carregar os quizzes disponíveis.")

# ==================== ESTATÍSTICAS DO QUIZ ====================
st.markdown("---")
st.markdown("### 📊 Suas Estatísticas de Quiz")

# Busca estatísticas do usuário
stats_response = api_request("GET", "/users/me/stats")
if stats_response and stats_response.status_code == 200:
    stats = stats_response.json()
    
    col1, col2, col3 = st.columns(3)
    
    stats_display = [
        {"label": "Taxa de Acerto", "value": f"{stats.get('accuracy', 0):.1f}%", "icon": "🎯"},
        {"label": "Quizzes Completos", "value": str(stats.get('quizzes_completed', 0)), "icon": "✅"},
        {"label": "Pontuação Média", "value": f"{stats.get('average_score', 0):.1f}", "icon": "⭐"}
    ]
    
    for i, stat in enumerate(stats_display):
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
else:
    st.info("Não foi possível carregar suas estatísticas.")
