# 🚀 AI-SkillUP: Plataforma Gamificada de Aprendizado

Projeto desenvolvido para a **Global Solution 2025 (1º Semestre)** da FIAP, como parte do curso de Análise e Desenvolvimento de Sistemas.

**Tema da Global Solution:** O Futuro do Trabalho.

Nossa solução, "AI-SkillUP", aborda o eixo **"Soluções gamificadas para engajamento e aprendizado corporativo"**. É uma Prova de Conceito (POC) de uma plataforma que utiliza Inteligência Artificial para personalizar a jornada de aprendizado, preparando profissionais para as novas demandas do mercado com foco em *upskilling* e *reskilling*.

## 👨‍💻 Equipe

* **Samuel Nicolas Oliveira Rocha** - RM568552

* **Gabriel Oliveira dos Santos** RM567166

* **Roberson Pedrosa de Oliveira Junior** RM567216

* **Arthur Brutttel Nascimento** RM568484

* **Jonatan Viotti Rodrigues da Silva** RM566787

## 📽️ Vídeo da POC (7 Minutos)

`[INSERIR AQUI O LINK DO YOUTUBE "NÃO LISTADO" DA SUA APRESENTAÇÃO]`

---

## ✨ Funcionalidades Principais (MVP)

* **Frontend Interativo (Streamlit):** Uma interface web onde o usuário pode interagir com o quiz.
* **API Backend (FastAPI):** Um microsserviço que "simula" (mocka) a lógica de negócio, como buscar quizzes, salvar pontuações e retornar predições.
* **Predição de Dificuldade (Machine Learning):** Um endpoint de API (`/predict-difficulty`) que simula a chamada a um modelo de Regressão Linear, sugerindo o próximo nível de dificuldade para o usuário.
* **Análise de Dados (R & Python):** Scripts que demonstram a análise de dados (séries temporais de engajamento) e o treinamento do modelo de ML.
* **Banco de Dados (SQLite):** Um schema de banco de dados normalizado (baseado no Cap07 da FIAP) para armazenar usuários, quizzes, opções e pontuações.

## 🛠️ Tecnologias Utilizadas (Requisitos da GS)

Este projeto integra conhecimento de todas as disciplinas obrigatórias da Fase 4:

* **🐍 Python (Cap03 - A Magia da Matemática):**
    * Linguagem principal para o backend (FastAPI), frontend (Streamlit) e scripts de ML (Scikit-learn).
    * Uso de `Numpy` e `Pandas` para manipulação de dados no placar e no treinamento do modelo.

* **🤖 Machine Learning & IA (Cap03 - Scikit-learn & Cap11 - Regressão):**
    * O script `src/ml/train_difficulty_model.py` simula o treinamento de um modelo de **Regressão Linear** para prever a dificuldade ideal do usuário.
    * O modelo é salvo em um arquivo `.joblib` para "produção".

* **📊 Linguagem R (Cap05 - Séries Temporais):**
    * O script `src/ml/analise_temporal_mock.R` demonstra a análise de uma série temporal mockada de engajamento de usuários, incluindo a **decomposição** da série.

* **🗃️ Banco de Dados (Cap06 - Relacionamentos & Cap07 - Do Conceitual ao Físico):**
    * O arquivo `src/database/models.py` define um **schema relacional normalizado** (3NF) usando SQLAlchemy, com tabelas como `T_USER`, `T_QUIZ_ITEM`, `T_QUIZ_OPTION` e `T_USER_ANSWER`.
    * Isso evita redundâncias e segue as boas práticas de modelagem (atributos atômicos) .

* **🖥️ Frontend (Cap04 - Streamlit):**
    * O frontend completo é construído em Streamlit , com uma arquitetura de múltiplas páginas (`app.py` + pasta `pages/`).
    * Utiliza widgets interativos como `st.radio` e `st.button` e `st.balloons` .

* **☁️ Computação em Nuvem:**
    * A arquitetura é desacoplada (frontend + backend).
    * O backend (`src/backend/main.py`) é uma **API RESTful** construída com **FastAPI**, pronta para deploy em qualquer plataforma de nuvem (como Azure App Service).

* **🔒 Cybersecurity (Cap08):**
    * A API é o ponto central de defesa. O projeto considera a mitigação de riscos como *Accounting Hijacking* (sequestro de conta) ao modularizar a lógica e preparar a estrutura de banco de dados (`T_USER`) para autenticação futura.

* **🌱 Formação Social (Cap01, Cap03 - Fase 3):**
    * O projeto está alinhado aos **Objetivos de Desenvolvimento Sustentável (ODS)** da ONU, especificamente a **ODS 4 (Educação de Qualidade)** e **ODS 8 (Trabalho Decente)**.

---

## 🚦 Como Executar o Projeto (Localmente)

Para executar esta POC, você precisará de **dois terminais** rodando simultaneamente: um para o Backend (API) e um para o Frontend (Streamlit).

### 1. Pré-requisitos

* Python 3.9+
* R (Opcional, veja passo 3.3)
* Git

### 2. Clone e Prepare o Ambiente

```bash
# 1. Clone o repositório
git clone [https://github.com/samuelnrocha/echo-skill-up.git](https://github.com/samuelnrocha/echo-skill-up.git)
cd echo-skill-up

# 2. Crie e ative o ambiente virtual (PowerShell)
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate

# 3. Instale as dependências Python
pip install -r requirements.txt

```

### 3. Gere os Artefatos (Executar 1 vez)
Você precisa executar esses scripts uma única vez para gerar os arquivos necessários para o projeto.

```bash

# 3.1. Criar o banco de dados (SQLite)
# (Isso cria o arquivo 'poc_database.db' na raiz)
python src/database/models.py

# 3.2. Treinar o modelo (ML)
# (Isso cria o arquivo 'difficulty_model.joblib' em 'src/ml/')
python src/ml/train_difficulty_model.py

# 3.3. Popular o banco com dados iniciais (Seed)
# (Isso adiciona quizzes, tópicos, dificuldades e usuário demo)
python src/backend/seed_data.py

# 3.4. Gerar o gráfico (R)
# (Isso cria o 'engagement_timeseries.png' em 'src/ml/')
#
# NOTA: Se você não tiver o R instalado, pule este passo e rode o script Python alternativo:
python src/ml/gerar_grafico_R_mock.py
# (O script analise_temporal_mock.R está no repositório para entrega,
# mas o script Python gera o mesmo gráfico .png para conveniência)
```

### 4. Execute a Aplicação
**Abra dois terminais separados (ambos com o venv ativo):**

**➡️ Terminal 1: Backend (API)**

```bash

# Navegue até a pasta do backend
cd src\backend

# Inicie o servidor da API
python main.py
(Deixe este terminal rodando. Você verá o Uvicorn rodando em http://127.0.0.1:8000)

```

**➡️ Terminal 2: Frontend (Streamlit)**

```bash

# Navegue até a pasta raiz do projeto (importante!)
# Se você está em 'src\backend', volte duas pastas:
cd ..\.. 

# Inicie o aplicativo Streamlit
streamlit run app.py

```

### 5. Acesse a Aplicação

**Seu navegador abrirá automaticamente no endereço http://localhost:8501.**

```bash

📂 Estrutura do Projeto
echo-skill-up/
│
├── app.py                      # Landing Page principal do Streamlit (Cap04)
├── poc_database.db             # Banco de dados SQLite (criado no passo 3.1)
├── requirements.txt            # Dependências do Python
├── README.md                   # Este arquivo
│
├── pages/                      # Pasta de páginas do Streamlit (Cap04)
│   ├── 1_Quiz_Interativo.py    # Tela do Quiz (Frontend)
│   └── 2_Placar.py             # Tela do Placar (Frontend)
│
└── src/
    │
    ├── backend/
    │   ├── main.py             # API Backend (FastAPI) (Python, Cloud)
    │   └── seed_data.py        # Script para popular banco com dados iniciais
    │
    ├── database/
    │   └── models.py           # Definição das tabelas (SQLAlchemy) (Banco de Dados)
    │
    └── ml/
        ├── train_difficulty_model.py # Script de treino do modelo (ML, Cap11)
        ├── difficulty_model.joblib   # Modelo treinado (criado no passo 3.2)
        │
        ├── analise_temporal_mock.R   # Script de análise (Linguagem R, Cap05)
        ├── gerar_grafico_R_mock.py   # Script Python para simular a saída do R
        └── engagement_timeseries.png # Gráfico da Série Temporal (criado no passo 3.4)
```