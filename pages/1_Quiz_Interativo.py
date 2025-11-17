import streamlit as st
import requests # Para comunicar com a API

# Configuração da página
st.set_page_config(page_title="Quiz Interativo", page_icon="❓")

st.title("❓ Quiz Interativo")

# URL da nossa API (rodando em http://127.0.0.1:8000)
API_URL = "http://127.0.0.1:8000"

# Carregar o quiz da API
# (Cap04 - Streamlit, Cap08 - NoSQL/JSON)
try:
    # Usamos "Prompt Engineering" como tópico mockado para a API
    response = requests.get(f"{API_URL}/quiz/Prompt Engineering")
    response.raise_for_status() # Lança um erro se a API falhar
    
    quiz_data = response.json().get("quiz")

    if quiz_data:
        st.subheader(f"Tópico: {quiz_data['topic']}")
        st.write(f"**Pergunta:** {quiz_data['question_text']}")
        
        # Cap04 - Usando widgets (st.radio) [cite: 1618]
        option_texts = [opt['text'] for opt in quiz_data['options']]
        selected_text = st.radio("Selecione sua resposta:", option_texts, key=f"quiz_{quiz_data['id_quiz']}")
        
        if st.button("Enviar Resposta"):
            # Encontra o ID da opção selecionada
            selected_option_id = next(opt['id'] for opt in quiz_data['options'] if opt['text'] == selected_text)
            
            # Verifica a resposta
            is_correct = (selected_option_id == quiz_data['correct_answer_id'])
            score = 10.0 if is_correct else 0.0
            
            # 1. Envia o score para a API (Cumpre "registrar pontuação")
            score_payload = {
                "user_id": 1, # ID de usuário mockado
                "quiz_id": quiz_data['id_quiz'],
                "score": score
            }
            requests.post(f"{API_URL}/submit-score", json=score_payload)
            
            if is_correct:
                st.success("Correto! Pontuação registrada.")
                st.balloons() # Conceito do Cap04 [cite: 1851-1852]
            else:
                st.error("Incorreto. Tente novamente!")
            
            # 2. Chama o modelo de ML (mockado) via API (Cumpre "ML/NN")
            ml_response = requests.get(f"{API_URL}/predict-difficulty/1") # ID de usuário mockado
            ml_data = ml_response.json()
            
            # Exibe o feedback da IA (Cap11)
            st.info(f"**Feedback da IA:** {ml_data['feedback_message']}")

    else:
        st.error("Não foi possível carregar o quiz. A API retornou um erro.")

except requests.exceptions.ConnectionError:
    st.error("Erro de Conexão: A API backend (FastAPI) não está rodando. Por favor, inicie o `src/backend/main.py`.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")