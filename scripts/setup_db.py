"""
Script para criar banco de dados e popular com dados iniciais
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database.models import create_db_and_tables
from src.backend.seed_data import seed_database

def setup_database():
    """Cria o banco de dados e popula com dados iniciais"""
    print("=" * 60)
    print("🌱 Setup do Banco de Dados - Eco-Skill Up")
    print("=" * 60)
    
    # Cria as tabelas
    print("\n📋 Criando tabelas do banco de dados...")
    create_db_and_tables()
    
    # Popula com dados iniciais
    print("\n🌱 Populando banco de dados com dados iniciais...")
    seed_database()
    
    print("\n" + "=" * 60)
    print("✅ Setup concluído com sucesso!")
    print("=" * 60)
    print("\n💡 Próximos passos:")
    print("   1. Inicie o servidor backend: python -m uvicorn src.backend.main:app --reload")
    print("   2. Inicie o frontend: streamlit run app.py")
    print("   3. Use as credenciais mostradas acima para fazer login")

if __name__ == "__main__":
    setup_database()

