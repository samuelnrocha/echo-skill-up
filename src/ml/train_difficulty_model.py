import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression # Conceito do Cap11 [cite: 9394-9397]
from sklearn.metrics import mean_squared_error # Conceito do Cap11 [cite: 9311]
import joblib
import numpy as np

print("Iniciando treinamento do modelo mockado (Cap11)...")

# 1. Gerar dados FAKES (simulados)
# Vamos prever 'dificuldade_ideal' (0=fácil, 1=médio, 2=difícil)
# com base em 'avg_score' (score médio) e 'time_spent_min' (tempo gasto)
np.random.seed(42)
data_size = 100
X = pd.DataFrame({
    'avg_score': np.random.uniform(20, 100, data_size),
    'time_spent_min': np.random.uniform(5, 30, data_size)
})
# Lógica fake: score alto -> dificuldade ideal alta
y_target = (X['avg_score'] * 0.02) + np.random.normal(0, 0.5, data_size)
y_target = np.clip(y_target, 0, 2) # Nível 0=Fácil, 1=Média, 2=Difícil

print(f"Dados simulados gerados: {len(X)} amostras.")

# 2. Dividir dados (Conceito do Cap03-ML e Cap09-BigData) [cite: 583-589, 236]
X_train, X_test, y_train, y_test = train_test_split(X, y_target, test_size=0.2, random_state=42)

# 3. Treinar o modelo de Regressão
model = LinearRegression()
model.fit(X_train, y_train)
print("Modelo de Regressão Linear treinado.")

# 4. Avaliar (Métrica do Cap11)
preds = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, preds)) # RMSE é uma métrica válida [cite: 9323]
print(f"Avaliação (RMSE) do modelo: {rmse:.4f}")

# 5. Salvar o modelo treinado
joblib.dump(model, 'difficulty_model.joblib')
print("Modelo salvo em 'src/ml/difficulty_model.joblib'")