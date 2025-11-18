"""
Helper functions para fazer requisições à API
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger("eco_skillup_api")
logger.setLevel(logging.DEBUG)  # ou INFO em produção

if not logger.handlers:
    handler = logging.FileHandler("eco_skillup_frontend.log", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# URL base da API
API_URL = "http://127.0.0.1:8000/api/v1"

def get_auth_headers() -> Dict[str, str]:
    """Retorna headers com token de autenticação"""
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    require_auth: bool = True
) -> Optional[requests.Response]:
    """
    Wrapper para fazer requisições à API
    
    Args:
        method: Método HTTP (GET, POST, PUT, DELETE)
        endpoint: Endpoint da API (sem a URL base)
        data: Dados para enviar (form data)
        json: Dados JSON para enviar
        params: Parâmetros de query string
        require_auth: Se True, adiciona token de autenticação
    
    Returns:
        Response object ou None em caso de erro
    """
    url = f"{API_URL}{endpoint}"
    headers = get_auth_headers() if require_auth else {}
    logger.info(
        f"REQUEST → {method.upper()} {url}\n"
        f"Headers: {headers}\n"
        f"Params: {params}\n"
        f"Payload: {data}"
    )
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json, data=data, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=json, data=data, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            st.error(f"Método HTTP não suportado: {method}")
            return None
        
        # Se receber 401, limpa autenticação e redireciona para login
        if response.status_code == 401:
            st.session_state.is_authenticated = False
            st.session_state.access_token = None
            st.session_state.current_user = None
            st.error("Sessão expirada. Por favor, faça login novamente.")
            st.rerun()
        
        return response
        
    except requests.exceptions.ConnectionError:
        st.error("⚠️ **Erro de Conexão**\n\nA API backend não está rodando. Por favor, inicie o servidor backend.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ **Timeout**\n\nA requisição demorou muito para responder.")
        return None
    except Exception as e:
        st.error(f"❌ **Erro na requisição:** {str(e)}")
        return None

def login(username: str, password: str) -> bool:
    """
    Faz login na API e armazena token
    
    Returns:
        True se login foi bem-sucedido, False caso contrário
    """
    response = api_request("POST", "/login", json={"username": username, "password": password}, require_auth=False)
    
    if response and response.status_code == 200:
        data = response.json()
        st.session_state["is_authenticated"] = True
        st.session_state["access_token"] = data["access_token"]
        st.session_state["current_user"] = data["user"]
        return True
    elif response:
        error_data = response.json() if response.content else {}
        st.error(error_data.get("detail", "Erro ao fazer login. Verifique suas credenciais."))
    return False

def register(user_data: Dict[str, Any]) -> bool:
    """
    Registra novo usuário na API
    
    Returns:
        True se registro foi bem-sucedido, False caso contrário
    """
    response = api_request("POST", "/register", json=user_data, require_auth=False)
    
    if response and response.status_code == 200:
        data = response.json()
        st.session_state.is_authenticated = True
        st.session_state.access_token = data.get("access_token")
        st.session_state.current_user = data.get("user", {})
        return True
    elif response:
        error_data = response.json() if response.content else {}
        st.error(error_data.get("detail", "Erro ao registrar usuário."))
    return False

