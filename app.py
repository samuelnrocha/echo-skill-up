import streamlit as st

# Configura o título da página, ícone e layout
# Isso é um conceito do Cap04 (Streamlit) [cite: 1472-1473, 1539-1540]
st.set_page_config(
    page_title="AI-SkillUP",
    page_icon="🚀",
    layout="wide"
)

# Título principal da Landing Page
st.title("🚀 Bem-vindo ao AI-SkillUP!")

# Descrição do projeto (Markdown para formatar)
st.markdown(
    """
    Esta é a plataforma gamificada de aprendizado da sua Global Solution.
    
    O objetivo deste POC é demonstrar um sistema que utiliza Inteligência Artificial
    para personalizar a jornada de aprendizado, cumprindo os requisitos das
    disciplinas de ML, IA, Cloud, R, Python e Banco de Dados.
    
    **Utilize o menu ao lado para navegar:**
    * **Quiz Interativo:** Teste seus conhecimentos e receba feedback da IA.
    * **Placar:** Veja as pontuações (mockado).
    """
)

st.sidebar.success("Selecione uma tela acima.")