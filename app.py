"""
Eco-Skill Up - Landing Page
Sistema Gamificado para Transição de Carreira Sustentável
"""

import streamlit as st
from src.frontend.components.theme import init_theme, apply_theme

# Configuração da página
st.set_page_config(
    page_title="Eco-Skill Up - Plataforma de Aprendizado Sustentável",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializa tema
init_theme()
apply_theme(st.session_state.get('theme', 'light'))

# ==================== CSS Customizado ====================
st.markdown("""
<style>
    /* Esconde o menu padrão do Streamlit na landing page */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilos gerais */
    .hero-section {
        background: linear-gradient(135deg, #00D4AA 0%, #006B5A 100%);
        color: white;
        padding: 5rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
    }
    
    .feature-card {
        background: white;
        border: 1px solid #E0E0E0;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    .benefit-item {
        padding: 1rem;
        margin: 0.5rem 0;
        background: #F8F9FA;
        border-left: 4px solid #00D4AA;
        border-radius: 8px;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #00D4AA 0%, #006B5A 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        border: none;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 212, 170, 0.3);
    }
    
    .step-card {
        background: white;
        border: 2px solid #E0E0E0;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        height: 100%;
    }
    
    .step-number {
        background: linear-gradient(135deg, #00D4AA 0%, #006B5A 100%);
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0 auto 1rem;
    }
    
    .footer {
        background: #1E1E1E;
        color: white;
        padding: 3rem 2rem;
        margin-top: 4rem;
        border-radius: 20px 20px 0 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("""
    <div style='padding: 1rem 0;'>
        <h1 style='color: #00D4AA; margin: 0; font-size: 2.5rem;'>🌱 Eco-Skill Up</h1>
        <p style='color: #6C757D; margin: 0; font-size: 1.1rem;'>Sistema Gamificado para Transição de Carreira Sustentável</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    theme_icon = "🌙" if st.session_state.get('theme', 'light') == 'light' else "☀️"
    if st.button(theme_icon, key="theme_toggle_landing"):
        st.session_state.theme = 'dark' if st.session_state.get('theme', 'light') == 'light' else 'light'
        st.rerun()
    
    if st.button("🚀 Entrar na Plataforma", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Dashboard.py")

st.markdown("---")

# ==================== HERO SECTION ====================
st.markdown("""
<div class="hero-section">
    <h1 style='font-size: 3rem; margin-bottom: 1rem;'>Prepare-se para a Economia Verde</h1>
    <p style='font-size: 1.3rem; margin-bottom: 2rem; opacity: 0.95;'>
        Transforme sua carreira com habilidades sustentáveis através de aprendizado gamificado e inteligência artificial
    </p>
    <div style='margin-top: 2rem;'>
        <a href='#demo' style='background: white; color: #006B5A; padding: 1rem 2rem; border-radius: 12px; text-decoration: none; font-weight: 600; display: inline-block; margin: 0 1rem;'>
            🎯 Começar Agora
        </a>
        <a href='#como-funciona' style='background: transparent; color: white; padding: 1rem 2rem; border: 2px solid white; border-radius: 12px; text-decoration: none; font-weight: 600; display: inline-block; margin: 0 1rem;'>
            📖 Saiba Mais
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== PROPOSTA DE VALOR ====================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 💡 Nossa Proposta de Valor")
st.markdown("""
<div style='background: #F8F9FA; padding: 2rem; border-radius: 16px; margin: 2rem 0;'>
    <p style='font-size: 1.2rem; line-height: 1.8; color: #1E1E1E;'>
        O <strong>Eco-Skill Up</strong> é uma plataforma inovadora que utiliza <strong>gamificação</strong> e 
        <strong>inteligência artificial</strong> para treinar e requalificar profissionais em habilidades essenciais 
        para a <strong>Economia Verde</strong>. Nossa solução mapeia gaps de competências e sugere trilhas de 
        aprendizado personalizadas, apresentadas em formato de missões e desafios, promovendo engajamento e 
        inovação sustentável.
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== BENEFÍCIOS ====================
st.markdown("## ✨ Benefícios da Plataforma")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2 style='color: #00D4AA; font-size: 3rem; margin: 0;'>🎯</h2>
        <h3 style='color: #1E1E1E; margin: 1rem 0;'>Aprendizado Personalizado</h3>
        <p style='color: #6C757D; line-height: 1.6;'>
            IA adapta o conteúdo ao seu nível e ritmo de aprendizado, garantindo máxima eficiência.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h2 style='color: #00D4AA; font-size: 3rem; margin: 0;'>🏆</h2>
        <h3 style='color: #1E1E1E; margin: 1rem 0;'>Gamificação Engajante</h3>
        <p style='color: #6C757D; line-height: 1.6;'>
            Sistema de pontos, badges e rankings que transformam aprendizado em uma experiência divertida.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h2 style='color: #00D4AA; font-size: 3rem; margin: 0;'>🌱</h2>
        <h3 style='color: #1E1E1E; margin: 1rem 0;'>Foco em Sustentabilidade</h3>
        <p style='color: #6C757D; line-height: 1.6;'>
            Conteúdo especializado em habilidades verdes e práticas sustentáveis para o futuro do trabalho.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== COMO FUNCIONA ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<a name="como-funciona"></a>', unsafe_allow_html=True)
st.markdown("## 🔄 Como Funciona")

col1, col2, col3, col4 = st.columns(4)

steps = [
    {"icon": "👤", "title": "Cadastro", "desc": "Crie sua conta e defina seus objetivos de carreira"},
    {"icon": "📊", "title": "Análise", "desc": "IA mapeia suas competências e identifica gaps"},
    {"icon": "🎯", "title": "Trilha Personalizada", "desc": "Receba missões e desafios adaptados ao seu perfil"},
    {"icon": "🚀", "title": "Evolução", "desc": "Acompanhe seu progresso e conquiste novas habilidades"}
]

for i, step in enumerate(steps, 1):
    with [col1, col2, col3, col4][i-1]:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{i}</div>
            <h2 style='font-size: 2.5rem; margin: 0;'>{step['icon']}</h2>
            <h3 style='color: #1E1E1E; margin: 1rem 0;'>{step['title']}</h3>
            <p style='color: #6C757D; line-height: 1.6;'>{step['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== RECURSOS ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## 🛠️ Recursos da Plataforma")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 16px; border: 1px solid #E0E0E0;'>
        <h3 style='color: #1E1E1E; margin-bottom: 1rem;'>📚 Conteúdo Diversificado</h3>
        <ul style='color: #6C757D; line-height: 2;'>
            <li>Quizzes interativos sobre sustentabilidade</li>
            <li>Módulos de aprendizado em economia verde</li>
            <li>Casos práticos e estudos de caso</li>
            <li>Recursos multimídia e vídeos educativos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 16px; border: 1px solid #E0E0E0;'>
        <h3 style='color: #1E1E1E; margin-bottom: 1rem;'>📈 Analytics Avançado</h3>
        <ul style='color: #6C757D; line-height: 2;'>
            <li>Dashboard com métricas de desempenho</li>
            <li>Análise de progresso e evolução</li>
            <li>Relatórios personalizados</li>
            <li>Insights baseados em IA</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== DEMONSTRAÇÃO ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<a name="demo"></a>', unsafe_allow_html=True)
st.markdown("## 🎬 Demonstração da Plataforma")

st.markdown("""
<div style='background: #F8F9FA; padding: 2rem; border-radius: 16px; text-align: center; margin: 2rem 0;'>
    <h3 style='color: #1E1E1E; margin-bottom: 1rem;'>Experimente Agora!</h3>
    <p style='color: #6C757D; margin-bottom: 2rem;'>
        Acesse nossa plataforma e descubra como podemos transformar sua jornada de aprendizado.
        Faça login para começar a explorar quizzes, acompanhar seu progresso e muito mais.
    </p>
    <div style='display: flex; gap: 1rem; justify-content: center;'>
        <button onclick="window.location.href='pages/1_Dashboard.py'" 
                style='background: linear-gradient(135deg, #00D4AA 0%, #006B5A 100%); 
                       color: white; padding: 1rem 2rem; border-radius: 12px; 
                       border: none; font-size: 1.1rem; font-weight: 600; cursor: pointer;'>
            🚀 Acessar Plataforma
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# Mockup/Ilustração (usando emojis e cards como placeholder)
st.markdown("### 📱 Interface da Plataforma")
col1, col2, col3 = st.columns(3)

mockups = [
    {"title": "Dashboard", "icon": "📊", "desc": "Visualize suas métricas e progresso"},
    {"title": "Quizzes", "icon": "❓", "desc": "Teste seus conhecimentos de forma interativa"},
    {"title": "Estatísticas", "icon": "📈", "desc": "Acompanhe sua evolução detalhada"}
]

for mockup in mockups:
    with [col1, col2, col3][mockups.index(mockup)]:
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 16px; 
                    border: 2px solid #E0E0E0; text-align: center; height: 200px; 
                    display: flex; flex-direction: column; justify-content: center;'>
            <h1 style='font-size: 4rem; margin: 0;'>{mockup['icon']}</h1>
            <h3 style='color: #1E1E1E; margin: 1rem 0;'>{mockup['title']}</h3>
            <p style='color: #6C757D; font-size: 0.9rem;'>{mockup['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== RODAPÉ ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; margin-bottom: 2rem;'>
        <div>
            <h3 style='color: #00D4AA; margin-bottom: 1rem;'>🌱 Eco-Skill Up</h3>
            <p style='color: #B0B0B0; line-height: 1.8;'>
                Transformando carreiras através de aprendizado sustentável e gamificado.
            </p>
        </div>
        <div>
            <h4 style='color: white; margin-bottom: 1rem;'>Produto</h4>
            <ul style='list-style: none; padding: 0; color: #B0B0B0; line-height: 2;'>
                <li>Funcionalidades</li>
                <li>Preços</li>
                <li>Recursos</li>
            </ul>
        </div>
        <div>
            <h4 style='color: white; margin-bottom: 1rem;'>Empresa</h4>
            <ul style='list-style: none; padding: 0; color: #B0B0B0; line-height: 2;'>
                <li>Sobre Nós</li>
                <li>Contato</li>
                <li>Carreiras</li>
            </ul>
        </div>
        <div>
            <h4 style='color: white; margin-bottom: 1rem;'>Legal</h4>
            <ul style='list-style: none; padding: 0; color: #B0B0B0; line-height: 2;'>
                <li>Privacidade</li>
                <li>Termos de Uso</li>
                <li>Cookies</li>
            </ul>
        </div>
    </div>
    <div style='border-top: 1px solid #3A3A3A; padding-top: 2rem; text-align: center; color: #B0B0B0;'>
        <p>© 2025 Eco-Skill Up. Todos os direitos reservados. | Global Solution FIAP</p>
        <p style='margin-top: 0.5rem; font-size: 0.9rem;'>
            Desenvolvido com ❤️ para o futuro do trabalho sustentável
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
