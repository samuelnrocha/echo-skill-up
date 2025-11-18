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

with col3:
    period_filter = st.selectbox(
        "Período",
        ["Todo o período", "Últimos 7 dias", "Últimos 30 dias"]
    )

# ==================== TOP 3 PODIUM ====================
st.markdown("### 🥇 Top 3")

# Dados mockados
top3_data = [
    {"name": "Ana Silva", "score": 2450, "badges": 12, "position": 1},
    {"name": "Carlos Santos", "score": 2380, "badges": 11, "position": 2},
    {"name": "Maria Oliveira", "score": 2320, "badges": 10, "position": 3}
]

col1, col2, col3 = st.columns([1, 1.2, 1])

medals = ["🥇", "🥈", "🥉"]
for i, user in enumerate(top3_data):
    with [col1, col2, col3][i]:
        height = "250px" if i == 1 else "200px"
        medal = medals[i]
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                    padding: 2rem; border-radius: 16px; text-align: center; 
                    border: 2px solid #E0E0E0; height: {height}; 
                    display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>{medal}</div>
            <h3 style='color: #1E1E1E; margin: 0.5rem 0;'>{user['name']}</h3>
            <h2 style='color: #00D4AA; font-size: 2.5rem; margin: 0.5rem 0;'>{user['score']}</h2>
            <p style='color: #6C757D; margin: 0.5rem 0;'>
                🏅 {user['badges']} Conquistas
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==================== RANKING COMPLETO ====================
st.markdown("### 📊 Ranking Completo")

# Dados mockados para o ranking
leaderboard_data = {
    'Posição': list(range(1, 21)),
    'Usuário': [f"User_{i}" for i in range(1, 21)],
    'Pontuação': [2450 - i*50 + (i%3)*10 for i in range(20)],
    'Quizzes': [25 - i for i in range(20)],
    'Taxa de Acerto': [95 - i*2 for i in range(20)],
    'Tópico Favorito': ['Python', 'IA', 'Sustentabilidade', 'ML', 'Python'] * 4
}

df_leaderboard = pd.DataFrame(leaderboard_data)

# Destaca o usuário atual
current_user = st.session_state.current_user.get('username', 'demo_user')
if current_user in df_leaderboard['Usuário'].values:
    st.info(f"👤 Você está na posição {df_leaderboard[df_leaderboard['Usuário'] == current_user]['Posição'].values[0]} do ranking!")

# Tabela do ranking
st.dataframe(
    df_leaderboard,
    use_container_width=True,
    hide_index=True
)

# ==================== GRÁFICOS ====================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Distribuição de Pontuações")
    
    fig = px.histogram(
        df_leaderboard,
        x='Pontuação',
        nbins=20,
        color_discrete_sequence=['#00D4AA']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🎯 Pontuação por Tópico")
    
    topic_scores = df_leaderboard.groupby('Tópico Favorito')['Pontuação'].mean().reset_index()
    
    fig = px.bar(
        topic_scores,
        x='Tópico Favorito',
        y='Pontuação',
        color='Pontuação',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== ESTATÍSTICAS DO RANKING ====================
st.markdown("### 📊 Estatísticas do Ranking")

col1, col2, col3, col4 = st.columns(4)

ranking_stats = [
    {"label": "Total de Participantes", "value": "156", "icon": "👥"},
    {"label": "Pontuação Média", "value": "1,850", "icon": "📊"},
    {"label": "Maior Pontuação", "value": "2,450", "icon": "⭐"},
    {"label": "Sua Posição", "value": "12", "icon": "🎯"}
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

