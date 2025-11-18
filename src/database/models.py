import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# --- Tabelas de Dimensão (Prática de 3NF - Cap07) ---

class Company(Base):
    """ T_COMPANY: Armazena as empresas cadastradas. """
    __tablename__ = 'T_COMPANY'
    id_company = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(200), nullable=False, unique=True)
    cnpj = Column(String(18), unique=True, nullable=True)
    email = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    users = relationship("User", back_populates="company")

class User(Base):
    """ T_USER: Armazena os usuários da plataforma. """
    __tablename__ = 'T_USER'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    full_name = Column(String(200), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user', nullable=False)  # 'admin' ou 'user'
    phone = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relacionamento com empresa
    id_company = Column(Integer, ForeignKey('T_COMPANY.id_company'), nullable=True)
    company = relationship("Company", back_populates="users")
    
    scores = relationship("UserScore", back_populates="user")
    answers = relationship("UserAnswer", back_populates="user")
    created_quizzes = relationship("QuizItem", back_populates="creator")

class QuizItem(Base):
    """ T_QUIZ_ITEM: Armazena a pergunta central do quiz. """
    __tablename__ = 'T_QUIZ_ITEM'
    id_quiz = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relação com as tabelas de dimensão (Melhor prática de Cap07)
    id_topic = Column(Integer, ForeignKey('T_TOPIC.id_topic'))
    id_difficulty = Column(Integer, ForeignKey('T_DIFFICULTY.id_difficulty'))
    id_creator = Column(Integer, ForeignKey('T_USER.id_user'), nullable=True)
    
    topic = relationship("Topic")
    difficulty = relationship("Difficulty")
    creator = relationship("User", back_populates="created_quizzes")
    options = relationship("QuizOption", back_populates="quiz_item", cascade="all, delete-orphan")
    scores = relationship("UserScore", back_populates="quiz")

class QuizOption(Base):
    """ T_QUIZ_OPTION: Armazena as opções de um quiz. (Resolve o 1NF) """
    __tablename__ = 'T_QUIZ_OPTION'
    id_option = Column(Integer, primary_key=True, autoincrement=True)
    option_text = Column(String(500), nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    
    id_quiz = Column(Integer, ForeignKey('T_QUIZ_ITEM.id_quiz'))
    quiz_item = relationship("QuizItem", back_populates="options")

class UserScore(Base):
    """ T_USER_SCORE: Armazena a pontuação final de um usuário em um quiz. """
    __tablename__ = 'T_USER_SCORE'
    id_score = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    id_user = Column(Integer, ForeignKey('T_USER.id_user'))
    id_quiz = Column(Integer, ForeignKey('T_QUIZ_ITEM.id_quiz'))
    
    user = relationship("User", back_populates="scores")
    quiz = relationship("QuizItem", back_populates="scores")

class UserAnswer(Base):
    """ T_USER_ANSWER: Loga CADA resposta. Essencial para o ML/R. """
    __tablename__ = 'T_USER_ANSWER'
    id_answer = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    id_user = Column(Integer, ForeignKey('T_USER.id_user'))
    id_option = Column(Integer, ForeignKey('T_QUIZ_OPTION.id_option'))
    
    user = relationship("User", back_populates="answers")
    option = relationship("QuizOption")


# --- Tabelas de Dimensão (Prática de 3NF - Cap07) ---

class Topic(Base):
    """ T_TOPIC: Armazena os tópicos (Python, R, IA, etc.) """
    __tablename__ = 'T_TOPIC'
    id_topic = Column(Integer, primary_key=True, autoincrement=True)
    topic_name = Column(String(100), nullable=False, unique=True)

class Difficulty(Base):
    """ T_DIFFICULTY: Armazena os níveis (Fácil, Médio, Difícil) """
    __tablename__ = 'T_DIFFICULTY'
    id_difficulty = Column(Integer, primary_key=True, autoincrement=True)
    difficulty_name = Column(String(50), nullable=False, unique=True)


# --- Criação do Banco ---
DATABASE_URL = "sqlite:///./poc_database.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    print("Criando tabelas (schema de produção)...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    create_db_and_tables()