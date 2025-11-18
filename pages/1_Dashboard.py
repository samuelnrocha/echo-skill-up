"""
Dashboard Principal - Área Interna
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header, render_metric_card
from src.frontend.components.auth import check_authentication

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

# URL da API
API_URL = "http://127.0.0.1:8000"

# ==================== MÉTRICAS PRINCIPAIS ====================
st.markdown("### 📈 Métricas Principais")
col1, col2, col3, col4 = st.columns(4)

# Métricas (mockadas - em produção viriam da API)
metrics = [
    {"title": "Pontuação Total", "value": "1,250", "delta": 12.5},
    {"title": "Quizzes Completos", "value": "24", "delta": 3},
    {"title": "Nível Atual", "value": "Avançado", "delta": None},
    {"title": "Conquistas", "value": "8", "delta": 2}
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
    # Dados mockados
    progress_data = pd.DataFrame({
        'Dia': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        'Pontuação': [120, 150, 180, 200, 250, 300, 350]
    })
    fig = px.line(progress_data, x='Dia', y='Pontuação', 
                  color_discrete_sequence=['#00D4AA'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                     paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🎯 Distribuição por Tópico")
    topic_data = pd.DataFrame({
        'Tópico': ['Python', 'IA', 'Sustentabilidade', 'ML', 'Banco de Dados'],
        'Pontuação': [350, 280, 250, 200, 170]
    })
    fig = px.pie(topic_data, values='Pontuação', names='Tópico',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)

# ==================== ATIVIDADES RECENTES ====================
st.markdown("### 🕐 Atividades Recentes")

activities = [
    {"icon": "✅", "action": "Quiz completado", "topic": "Sustentabilidade", "score": "+10", "time": "2h atrás"},
    {"icon": "🏆", "action": "Conquista desbloqueada", "topic": "Python Master", "score": "", "time": "5h atrás"},
    {"icon": "📈", "action": "Nível aumentado", "topic": "Avançado", "score": "", "time": "1 dia atrás"},
    {"icon": "✅", "action": "Quiz completado", "topic": "Machine Learning", "score": "+8", "time": "2 dias atrás"},
]

for activity in activities:
    st.markdown(f"""
    <div style='background: white; padding: 1rem; border-radius: 12px; 
                border: 1px solid #E0E0E0; margin: 0.5rem 0; 
                display: flex; align-items: center; gap: 1rem;'>
        <span style='font-size: 2rem;'>{activity['icon']}</span>
        <div style='flex: 1;'>
            <strong>{activity['action']}</strong> - {activity['topic']}
            {f"<span style='color: #00D4AA; font-weight: bold;'>{activity['score']}</span>" if activity['score'] else ""}
        </div>
        <span style='color: #6C757D; font-size: 0.9rem;'>{activity['time']}</span>
    </div>
    """, unsafe_allow_html=True)

# ==================== PRÓXIMOS DESAFIOS ====================
st.markdown("### 🎯 Próximos Desafios")

col1, col2, col3 = st.columns(3)

challenges = [
    {"title": "Economia Circular", "difficulty": "Médio", "xp": 50},
    {"title": "Energias Renováveis", "difficulty": "Difícil", "xp": 75},
    {"title": "Python Avançado", "difficulty": "Avançado", "xp": 100}
]

for i, challenge in enumerate(challenges):
    with [col1, col2, col3][i]:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 2px solid #E0E0E0;'>
            <h4 style='color: #1E1E1E; margin: 0 0 0.5rem 0;'>{challenge['title']}</h4>
            <p style='color: #6C757D; margin: 0.5rem 0;'>
                Dificuldade: <strong>{challenge['difficulty']}</strong>
            </p>
            <p style='color: #00D4AA; font-weight: bold; margin: 0.5rem 0;'>
                🎁 {challenge['xp']} XP
            </p>
            <button style='background: #00D4AA; color: white; border: none; 
                          padding: 0.5rem 1rem; border-radius: 8px; 
                          cursor: pointer; width: 100%; margin-top: 1rem;'>
                Iniciar Desafio
            </button>
        </div>
        """, unsafe_allow_html=True)

