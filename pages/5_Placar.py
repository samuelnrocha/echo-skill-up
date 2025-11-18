"""
Página de Placar de Líderes
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication
from src.frontend.utils.api import api_request

# Configuração
st.set_page_config(
    page_title="Placar de Líderes - Eco-Skill Up",
    page_icon="🏆",
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
render_header("🏆 Placar de Líderes", "Veja o ranking dos melhores desempenhos")

# ==================== FILTROS ====================
st.markdown("### 🔍 Filtros")
col1, col2, col3 = st.columns(3)

with col1:
    ranking_type = st.selectbox(
        "Tipo de Ranking",
        ["Geral", "Por Tópico", "Semanal", "Mensal"]
    )

with col2:
    topic_filter = st.selectbox(
        "Tópico",
        ["Todos"] + ["Prompt Engineering", "Python", "IA", "Machine Learning", 
                    "Banco de Dados", "R", "Sustentabilidade", "Economia Verde"]
    )

# Busca leaderboard
leaderboard_params = {"limit": 20}
if topic_filter != "Todos":
    leaderboard_params["topic"] = topic_filter

leaderboard_response = api_request("GET", "/leaderboard", params=leaderboard_params)
leaderboard_data = leaderboard_response.json() if leaderboard_response and leaderboard_response.status_code == 200 else []

# ==================== TOP 3 PODIUM ====================
st.markdown("### 🥇 Top 3")

top3_data = leaderboard_data[:3] if len(leaderboard_data) >= 3 else leaderboard_data

col1, col2, col3 = st.columns([1, 1.2, 1])

medals = ["🥇", "🥈", "🥉"]
if top3_data:
    for i, user in enumerate(top3_data):
        with [col1, col2, col3][i]:
            height = "250px" if i == 1 else "200px"
            medal = medals[i] if i < len(medals) else "🏅"
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                        padding: 2rem; border-radius: 16px; text-align: center; 
                        border: 2px solid #E0E0E0; height: {height}; 
                        display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 4rem; margin-bottom: 1rem;'>{medal}</div>
                <h3 style='color: #1E1E1E; margin: 0.5rem 0;'>{user.get('full_name', user.get('username', 'Usuário'))}</h3>
                <h2 style='color: #00D4AA; font-size: 2.5rem; margin: 0.5rem 0;'>{int(user.get('total_score', 0)):,}</h2>
                <p style='color: #6C757D; margin: 0.5rem 0;'>
                    ✅ {user.get('quizzes_completed', 0)} Quizzes
                </p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Ainda não há dados suficientes para exibir o ranking.")

# ==================== RANKING COMPLETO ====================
st.markdown("### 📊 Ranking Completo")

if leaderboard_data:
    # Prepara dados para DataFrame
    df_data = {
        'Posição': [u.get('rank', i+1) for i, u in enumerate(leaderboard_data)],
        'Usuário': [u.get('full_name', u.get('username', 'Usuário')) for u in leaderboard_data],
        'Pontuação': [int(u.get('total_score', 0)) for u in leaderboard_data],
        'Quizzes Completos': [u.get('quizzes_completed', 0) for u in leaderboard_data]
    }
    
    df_leaderboard = pd.DataFrame(df_data)
    
    # Destaca o usuário atual
    current_user_id = st.session_state.current_user.get('id_user')
    user_rank = next((u.get('rank') for u in leaderboard_data if u.get('user_id') == current_user_id), None)
    if user_rank:
        st.info(f"👤 Você está na posição {user_rank} do ranking!")
    
    # Tabela do ranking
    st.dataframe(
        df_leaderboard,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Ainda não há dados suficientes para exibir o ranking completo.")

# ==================== GRÁFICOS ====================
if leaderboard_data and len(leaderboard_data) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Distribuição de Pontuações")
        
        scores = [u.get('total_score', 0) for u in leaderboard_data]
        fig = px.histogram(
            x=scores,
            nbins=min(20, len(scores)),
            color_discrete_sequence=['#00D4AA'],
            labels={'x': 'Pontuação', 'y': 'Frequência'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Top 10 Pontuações")
        
        top10 = leaderboard_data[:10]
        fig = px.bar(
            x=[u.get('full_name', u.get('username', 'Usuário')) for u in top10],
            y=[u.get('total_score', 0) for u in top10],
            color=[u.get('total_score', 0) for u in top10],
            color_continuous_scale='Viridis',
            labels={'x': 'Usuário', 'y': 'Pontuação'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================== ESTATÍSTICAS DO RANKING ====================
st.markdown("### 📊 Estatísticas do Ranking")

if leaderboard_data:
    total_participants = len(leaderboard_data)
    avg_score = sum(u.get('total_score', 0) for u in leaderboard_data) / total_participants if total_participants > 0 else 0
    max_score = max((u.get('total_score', 0) for u in leaderboard_data), default=0)
    current_user_id = st.session_state.current_user.get('id_user')
    user_rank = next((u.get('rank') for u in leaderboard_data if u.get('user_id') == current_user_id), None)
    
    col1, col2, col3, col4 = st.columns(4)
    
    ranking_stats = [
        {"label": "Total de Participantes", "value": str(total_participants), "icon": "👥"},
        {"label": "Pontuação Média", "value": f"{int(avg_score):,}", "icon": "📊"},
        {"label": "Maior Pontuação", "value": f"{int(max_score):,}", "icon": "⭐"},
        {"label": "Sua Posição", "value": str(user_rank) if user_rank else "N/A", "icon": "🎯"}
    ]
    
    for i, stat in enumerate(ranking_stats):
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
else:
    st.info("Ainda não há dados suficientes para exibir estatísticas.")

