"""
Componente de Header reutilizável
"""

import streamlit as st

def render_header(title, subtitle=None, show_breadcrumb=False):
    """Renderiza o header da página"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title(title)
        if subtitle:
            st.caption(subtitle)
    
    with col3:
        # Notificações e ações rápidas podem ser adicionadas aqui
        pass
    
    if show_breadcrumb:
        st.markdown("---")

def render_metric_card(title, value, delta=None, delta_color="normal"):
    """Renderiza um card de métrica"""
    delta_html = ""
    if delta:
        color = "green" if delta_color == "normal" and delta > 0 else "red" if delta < 0 else "gray"
        delta_html = f'<span style="color: {color}; font-size: 0.9rem;">{delta:+.1f}%</span>'
    
    card_html = f"""
    <div class="metric-card">
        <h3 style="color: #6C757D; font-size: 0.9rem; margin: 0; font-weight: 500;">{title}</h3>
        <h1 style="color: #00D4AA; font-size: 2.5rem; margin: 0.5rem 0;">{value}</h1>
        {delta_html}
    </div>
    """
    return card_html

