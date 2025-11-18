"""
Dashboard Principal - Área Interna
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header, render_metric_card
from src.frontend.components.auth import check_authentication
from src.frontend.utils.api import api_request

# Configuração
st.set_page_config(
    page_title="Dashboard - Eco-Skill Up",
    page_icon="📊",
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
render_header("📊 Dashboard", "Visão geral do seu desempenho e progresso")

# ==================== MÉTRICAS PRINCIPAIS ====================
st.markdown("### 📈 Métricas Principais")
col1, col2, col3, col4 = st.columns(4)

# Busca estatísticas do usuário
stats_response = api_request("GET", "/users/me/stats")
if stats_response and stats_response.status_code == 200:
    stats = stats_response.json()
    
    # Calcula nível baseado na pontuação
    total_score = stats.get("total_score", 0)
    if total_score < 50:
        level = "Iniciante"
    elif total_score < 150:
        level = "Intermediário"
    elif total_score < 300:
        level = "Avançado"
    else:
        level = "Expert"
    
    metrics = [
        {"title": "Pontuação Total", "value": f"{int(total_score):,}", "delta": None},
        {"title": "Quizzes Completos", "value": str(stats.get("quizzes_completed", 0)), "delta": None},
        {"title": "Nível Atual", "value": level, "delta": None},
        {"title": "Taxa de Acerto", "value": f"{stats.get('accuracy', 0):.1f}%", "delta": None}
    ]
else:
    # Fallback para dados mockados
    metrics = [
        {"title": "Pontuação Total", "value": "0", "delta": None},
        {"title": "Quizzes Completos", "value": "0", "delta": None},
        {"title": "Nível Atual", "value": "Iniciante", "delta": None},
        {"title": "Taxa de Acerto", "value": "0%", "delta": None}
    ]

for i, metric in enumerate(metrics):
    with [col1, col2, col3, col4][i]:
        st.markdown(render_metric_card(
            metric["title"],
            metric["value"],
            metric.get("delta"),
            "normal"
        ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== GRÁFICOS ====================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Progresso Semanal")
    # Busca scores do usuário
    scores_response = api_request("GET", "/users/me/scores")
    if scores_response and scores_response.status_code == 200:
        scores = scores_response.json()
        
        # Agrupa por semana
        if scores:
            df = pd.DataFrame(scores)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['week'] = df['timestamp'].dt.to_period('W')
            weekly = df.groupby('week')['score'].sum().reset_index()
            weekly['week_str'] = weekly['week'].astype(str)
            
            fig = px.line(weekly, x='week_str', y='score', 
                          color_discrete_sequence=['#00D4AA'],
                          labels={'week_str': 'Semana', 'score': 'Pontuação'})
        else:
            # Dados vazios
            fig = px.line(pd.DataFrame({'Dia': [], 'Pontuação': []}), 
                          x='Dia', y='Pontuação', color_discrete_sequence=['#00D4AA'])
    else:
        # Fallback
        progress_data = pd.DataFrame({
            'Dia': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
            'Pontuação': [0, 0, 0, 0, 0, 0, 0]
        })
        fig = px.line(progress_data, x='Dia', y='Pontuação', 
                      color_discrete_sequence=['#00D4AA'])
    
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                     paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🎯 Distribuição por Tópico")
    # Busca scores e agrupa por tópico
    scores_response = api_request("GET", "/users/me/scores")
    if scores_response and scores_response.status_code == 200:
        scores = scores_response.json()
        
        if scores:
            df = pd.DataFrame(scores)
            topic_scores = df.groupby('topic')['score'].sum().reset_index()
            topic_scores.columns = ['Tópico', 'Pontuação']
            
            fig = px.pie(topic_scores, values='Pontuação', names='Tópico',
                         color_discrete_sequence=px.colors.qualitative.Set3)
        else:
            fig = px.pie(pd.DataFrame({'Tópico': [], 'Pontuação': []}), 
                         values='Pontuação', names='Tópico',
                         color_discrete_sequence=px.colors.qualitative.Set3)
    else:
        topic_data = pd.DataFrame({
            'Tópico': [],
            'Pontuação': []
        })
        fig = px.pie(topic_data, values='Pontuação', names='Tópico',
                     color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)

# ==================== ATIVIDADES RECENTES ====================
st.markdown("### 🕐 Atividades Recentes")

activities_response = api_request("GET", "/users/me/activities", params={"limit": 10})
if activities_response and activities_response.status_code == 200:
    activities = activities_response.json()
    
    if activities:
        for activity in activities:
            # Formata timestamp
            timestamp = activity.get('timestamp')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.utcnow()
                    diff = now - dt.replace(tzinfo=None) if dt.tzinfo else now - dt
                    
                    if diff.days > 0:
                        time_str = f"{diff.days} dia(s) atrás"
                    elif diff.seconds > 3600:
                        time_str = f"{diff.seconds // 3600}h atrás"
                    else:
                        time_str = f"{diff.seconds // 60}min atrás"
                except:
                    time_str = timestamp
            else:
                time_str = "Recentemente"
            
            score = activity.get('score', 0)
            score_str = f"+{int(score)}" if score > 0 else ""
            
            st.markdown(f"""
            <div style='background: white; padding: 1rem; border-radius: 12px; 
                        border: 1px solid #E0E0E0; margin: 0.5rem 0; 
                        display: flex; align-items: center; gap: 1rem;'>
                <span style='font-size: 2rem;'>✅</span>
                <div style='flex: 1;'>
                    <strong>{activity.get('action', 'Quiz completado')}</strong> - {activity.get('topic', 'N/A')} ({activity.get('difficulty', 'N/A')})
                    {f"<span style='color: #00D4AA; font-weight: bold;'>{score_str}</span>" if score_str else ""}
                </div>
                <span style='color: #6C757D; font-size: 0.9rem;'>{time_str}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma atividade recente. Complete alguns quizzes para ver seu progresso aqui!")
else:
    st.info("Não foi possível carregar atividades recentes.")

# ==================== PRÓXIMOS DESAFIOS ====================
st.markdown("### 🎯 Próximos Desafios")

# Busca quizzes disponíveis
available_response = api_request("GET", "/quizzes/available", params={"limit": 3})
if available_response and available_response.status_code == 200:
    available_quizzes = available_response.json()
    
    if available_quizzes:
        cols = st.columns(min(3, len(available_quizzes)))
        for i, quiz in enumerate(available_quizzes[:3]):
            with cols[i]:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                            padding: 1.5rem; border-radius: 12px; border: 2px solid #E0E0E0;'>
                    <h4 style='color: #1E1E1E; margin: 0 0 0.5rem 0;'>{quiz.get('topic', 'Quiz')}</h4>
                    <p style='color: #6C757D; margin: 0.5rem 0; font-size: 0.9rem;'>
                        {quiz.get('question_text', '')[:60]}...
                    </p>
                    <p style='color: #6C757D; margin: 0.5rem 0;'>
                        Dificuldade: <strong>{quiz.get('difficulty', 'N/A')}</strong>
                    </p>
                    <p style='color: #00D4AA; font-weight: bold; margin: 0.5rem 0;'>
                        🎁 10 XP
                    </p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Iniciar Quiz", key=f"quiz_{quiz.get('id_quiz')}", use_container_width=True):
                    st.session_state.selected_quiz_id = quiz.get('id_quiz')
                    st.switch_page("pages/2_Quizzes.py")
    else:
        st.info("🎉 Parabéns! Você completou todos os quizzes disponíveis!")
else:
    st.info("Não foi possível carregar próximos desafios.")

