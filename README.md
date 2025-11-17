# 🚀 AI-SkillUP: Plataforma Gamificada de Aprendizado

Projeto desenvolvido para a **Global Solution 2025 (1º Semestre)** da FIAP, como parte do curso de Análise e Desenvolvimento de Sistemas.

**Tema da Global Solution:** O Futuro do Trabalho.

[cite_start]Nossa solução, "AI-SkillUP", aborda o eixo **"Soluções gamificadas para engajamento e aprendizado corporativo"**[cite: 4466]. É uma Prova de Conceito (POC) de uma plataforma que utiliza Inteligência Artificial para personalizar a jornada de aprendizado, preparando profissionais para as novas demandas do mercado com foco em *upskilling* e *reskilling*.

## 👨‍💻 Equipe

* **Samuel Nicolas Oliveira Rocha** - RM568552

## 📽️ Vídeo da POC (7 Minutos)

[cite_start]`[INSERIR AQUI O LINK DO YOUTUBE "NÃO LISTADO" DA SUA APRESENTAÇÃO]` [cite: 4520]

---

## ✨ Funcionalidades Principais (MVP)

* **Frontend Interativo (Streamlit):** Uma interface web onde o usuário pode interagir com o quiz.
* **API Backend (FastAPI):** Um microsserviço que "simula" (mocka) a lógica de negócio, como buscar quizzes, salvar pontuações e retornar predições.
* **Predição de Dificuldade (Machine Learning):** Um endpoint de API (`/predict-difficulty`) que simula a chamada a um modelo de Regressão Linear, sugerindo o próximo nível de dificuldade para o usuário.
* **Análise de Dados (R & Python):** Scripts que demonstram a análise de dados (séries temporais de engajamento) e o treinamento do modelo de ML.
* **Banco de Dados (SQLite):** Um schema de banco de dados normalizado (baseado no Cap07 da FIAP) para armazenar usuários, quizzes, opções e pontuações.

## 🛠️ Tecnologias Utilizadas (Requisitos da GS)

[cite_start]Este projeto integra conhecimento de todas as disciplinas obrigatórias da Fase 4 [cite: 4474-4481, 4516]:

* **🐍 Python (Cap03 - A Magia da Matemática):**
    * Linguagem principal para o backend (FastAPI), frontend (Streamlit) e scripts de ML (Scikit-learn).
    * [cite_start]Uso de `Numpy` e `Pandas` para manipulação de dados no placar e no treinamento do modelo [cite: 13917-13921, 15998-16002].

* **🤖 Machine Learning & IA (Cap03 - Scikit-learn & Cap11 - Regressão):**
    * [cite_start]O script `src/ml/train_difficulty_model.py` simula o treinamento de um modelo de **Regressão Linear** [cite: 12224-12226, 12267-12270] para prever a dificuldade ideal do usuário.
    * O modelo é salvo em um arquivo `.joblib` para "produção".

* **📊 Linguagem R (Cap05 - Séries Temporais):**
    * [cite_start]O script `src/ml/analise_temporal_mock.R` demonstra a análise de uma série temporal mockada de engajamento de usuários, incluindo a **decomposição** da série [cite: 14008, 14022-14026].

* **🗃️ Banco de Dados (Cap06 - Relacionamentos & Cap07 - Do Conceitual ao Físico):**
    * [cite_start]O arquivo `src/database/models.py` define um **schema relacional normalizado** (3NF) [cite: 7414-7415] usando SQLAlchemy, com tabelas como `T_USER`, `T_QUIZ_ITEM`, `T_QUIZ_OPTION` e `T_USER_ANSWER`.
    * [cite_start]Isso evita redundâncias e segue as boas práticas de modelagem (atributos atômicos) [cite: 7414-7415].

* **🖥️ Frontend (Cap04 - Streamlit):**
    * [cite_start]O frontend completo é construído em Streamlit [cite: 14619-14620][cite_start], com uma arquitetura de múltiplas páginas (`app.py` + pasta `pages/`) [cite: 1470-1471].
    * [cite_start]Utiliza widgets interativos como `st.radio` e `st.button` [cite: 1419-1420] [cite_start]e `st.balloons` [cite: 1851-1852].

* **☁️ Computação em Nuvem:**
    * A arquitetura é desacoplada (frontend + backend).
    * O backend (`src/backend/main.py`) é uma **API RESTful** construída com **FastAPI**, pronta para deploy em qualquer plataforma de nuvem (como Azure App Service).

* **🔒 Cybersecurity (Cap08):**
    * A API é o ponto central de defesa. [cite_start]O projeto considera a mitigação de riscos como *Accounting Hijacking* (sequestro de conta) [cite: 5855-5856] ao modularizar a lógica e preparar a estrutura de banco de dados (`T_USER`) para autenticação futura.

* **🌱 Formação Social (Cap01, Cap03 - Fase 3):**
    * [cite_start]O projeto está alinhado aos **Objetivos de Desenvolvimento Sustentável (ODS)** da ONU, especificamente a **ODS 4 (Educação de Qualidade)** e **ODS 8 (Trabalho Decente)** [cite: 1515, 1530-1533].

---

## 🚦 Como Executar o Projeto (Localmente)

Para executar esta POC, você precisará de **dois terminais** rodando simultaneamente: um para o Backend (API) e um para o Frontend (Streamlit).

### 1. Pré-requisitos

* Python 3.9+
* R (Opcional, veja passo 4.3)
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