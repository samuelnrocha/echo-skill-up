"""
Página de Estatísticas e Análises
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from src.frontend.components.theme import init_theme, apply_theme
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.header import render_header
from src.frontend.components.auth import check_authentication
from src.frontend.utils.api import api_request

# Configuração
st.set_page_config(
    page_title="Estatísticas - Eco-Skill Up",
    page_icon="📈",
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
render_header("📈 Estatísticas e Análises", "Visualize seu progresso e desempenho detalhado")

# ==================== FILTROS ====================
st.markdown("### 🔍 Filtros de Análise")
col1, col2, col3 = st.columns(3)

with col1:
    period = st.selectbox(
        "Período",
        ["Últimos 7 dias", "Últimos 30 dias", "Últimos 90 dias", "Todo o período"]
    )

with col2:
    metric_type = st.selectbox(
        "Tipo de Métrica",
        ["Pontuação", "Quizzes Completos", "Taxa de Acerto", "Tempo de Estudo"]
    )

with col3:
    topic_filter = st.selectbox(
        "Tópico",
        ["Todos"] + ["Prompt Engineering", "Python", "IA", "Machine Learning", 
                    "Banco de Dados", "R", "Sustentabilidade", "Economia Verde"]
    )

# ==================== GRÁFICO DE LINHA - EVOLUÇÃO ====================
st.markdown("### 📊 Evolução do Desempenho")

# Busca scores do usuário
scores_response = api_request("GET", "/users/me/scores")
if scores_response and scores_response.status_code == 200:
    scores = scores_response.json()
    
    if scores:
        df = pd.DataFrame(scores)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Agrupa por data
        df['date'] = df['timestamp'].dt.date
        daily = df.groupby('date').agg({
            'score': 'sum',
            'quiz_id': 'count'
        }).reset_index()
        daily.columns = ['Data', 'Pontuação', 'Quizzes']
        daily['Taxa de Acerto'] = 100  # Placeholder
        
        fig = px.line(
            daily, 
            x='Data', 
            y=metric_type if metric_type in daily.columns else 'Pontuação',
            color_discrete_sequence=['#00D4AA'],
            markers=True
        )
    else:
        fig = px.line(pd.DataFrame({'Data': [], 'Pontuação': []}), 
                      x='Data', y='Pontuação', color_discrete_sequence=['#00D4AA'])
else:
    fig = px.line(pd.DataFrame({'Data': [], 'Pontuação': []}), 
                  x='Data', y='Pontuação', color_discrete_sequence=['#00D4AA'])

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# ==================== GRÁFICOS COMPARATIVOS ====================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Desempenho por Tópico")
    
    topic_performance = pd.DataFrame({
        'Tópico': ['Python', 'IA', 'Sustentabilidade', 'ML', 'Banco de Dados', 'R'],
        'Pontuação Média': [8.5, 8.2, 9.0, 7.8, 8.7, 8.0],
        'Quizzes': [5, 4, 6, 3, 4, 3]
    })
    
    fig = px.bar(
        topic_performance,
        x='Tópico',
        y='Pontuação Média',
        color='Pontuação Média',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### ⏱️ Distribuição de Tempo")
    
    time_distribution = pd.DataFrame({
        'Atividade': ['Quizzes', 'Leitura', 'Prática', 'Revisão'],
        'Horas': [12, 8, 6, 4]
    })
    
    fig = px.pie(
        time_distribution,
        values='Horas',
        names='Atividade',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ==================== HEATMAP DE ATIVIDADE ====================
st.markdown("### 📅 Heatmap de Atividade")

# Gera dados para heatmap
import numpy as np
days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
weeks = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
activity_matrix = np.random.randint(0, 10, size=(len(weeks), len(days)))

fig = go.Figure(data=go.Heatmap(
    z=activity_matrix,
    x=days,
    y=weeks,
    colorscale='Viridis',
    text=activity_matrix,
    texttemplate='%{text}',
    textfont={"size": 10}
))
fig.update_layout(
    height=300,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# ==================== TABELA DETALHADA ====================
st.markdown("### 📋 Dados Detalhados")

detailed_data = pd.DataFrame({
    'Data': pd.date_range(start='2025-01-01', periods=10, freq='D'),
    'Quiz': [f"Quiz {i}" for i in range(1, 11)],
    'Tópico': ['Python', 'IA', 'Sustentabilidade', 'ML', 'Python', 'IA', 'Sustentabilidade', 'ML', 'Python', 'IA'],
    'Dificuldade': ['Fácil', 'Médio', 'Fácil', 'Difícil', 'Médio', 'Fácil', 'Médio', 'Difícil', 'Fácil', 'Médio'],
    'Pontuação': [10, 8, 10, 6, 9, 10, 8, 7, 10, 9],
    'Tempo (min)': [5, 8, 6, 12, 7, 5, 7, 15, 4, 6]
})

st.dataframe(
    detailed_data,
    use_container_width=True,
    hide_index=True
)

# ==================== INSIGHTS ====================
st.markdown("### 💡 Insights e Recomendações")

insights = [
    {
        "icon": "📈",
        "title": "Tendência Positiva",
        "description": "Sua pontuação média aumentou 15% nos últimos 30 dias. Continue assim!",
        "color": "#00D4AA"
    },
    {
        "icon": "🎯",
        "title": "Área de Melhoria",
        "description": "Machine Learning tem a menor pontuação média. Considere revisar esse tópico.",
        "color": "#FFB800"
    },
    {
        "icon": "⭐",
        "title": "Destaque",
        "description": "Você é excelente em Sustentabilidade! Continue explorando esse tema.",
        "color": "#00D4AA"
    }
]

for insight in insights:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                border-left: 4px solid {insight['color']}; 
                margin: 1rem 0; border: 1px solid #E0E0E0;'>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <span style='font-size: 2rem;'>{insight['icon']}</span>
            <div>
                <h4 style='color: #1E1E1E; margin: 0;'>{insight['title']}</h4>
                <p style='color: #6C757D; margin: 0.5rem 0 0 0;'>{insight['description']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

