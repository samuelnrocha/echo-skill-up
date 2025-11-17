import streamlit as st
import pandas as pd
import numpy as np # Cap03 - A Magia da Matemática [cite: 1086-1087]

st.set_page_config(page_title="Placar de Líderes", page_icon="🏆")
st.title("🏆 Placar de Líderes")
st.write("Esta tela demonstra a leitura de dados (mockados) e conceitos de Análise de Dados.")

# Gerar dados FAKES para o placar, já que não temos um T_USER real
# (Cap03 - NumPy)
@st.cache_data
def get_mock_leaderboard():
    data = {
        'Usuário (Mock)': ['User_1', 'User_5', 'User_3', 'User_4', 'User_2'],
        'Pontuação (Cap03)': np.random.randint(50, 100, 5),
        'Tópico (Cap07)': ['Python', 'IA', 'Python', 'R', 'Banco de Dados']
    }
    df = pd.DataFrame(data)
    return df.sort_values(by='Pontuação (Cap03)', ascending=False)

try:
    df_leaderboard = get_mock_leaderboard()
    
    st.subheader("Ranking Geral")
    # Cap04 - Exibindo um DataFrame [cite: 1724]
    st.dataframe(df_leaderboard, use_container_width=True)
    
    # Gráfico (Cap05 - Os gráficos também falam) [cite: 4593-4597]
    st.subheader("Pontuação por Tópico")
    st.bar_chart(df_leaderboard.groupby('Tópico (Cap07)')['Pontuação (Cap03)'].mean())
    
except Exception as e:
    st.error(f"Ocorreu um erro ao gerar o placar: {e}")