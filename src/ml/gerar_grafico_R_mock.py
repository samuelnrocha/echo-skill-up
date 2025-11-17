import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("Gerando gráfico mockado (Python) para a entrega de R...")

# 1. Gerar os mesmos dados mockados
np.random.seed(42)
tempo = np.arange(1, 37)
engajamento = 50 + tempo * 0.5 + np.random.normal(0, 3, 36) + np.sin(tempo * 0.5) * 5
indice_temporal = pd.date_range(start='2023-01-01', periods=36, freq='MS')

df = pd.DataFrame(data={'data': indice_temporal, 'engajamento': engajamento})
df = df.set_index('data')

# 2. Simular a "Decomposição" (conceito do Cap05)
# Em um projeto real, usaríamos statsmodels.tsa.seasonal_decompose
# Para o mock, vamos apenas criar os 4 gráficos
df['tendencia'] = df['engajamento'].rolling(window=6, center=True).mean().fillna(method='bfill').fillna(method='ffill')
df['sazonal'] = (df['engajamento'] - df['tendencia']).rolling(window=3, center=True).mean().fillna(method='bfill').fillna(method='ffill')
df['residuo'] = df['engajamento'] - df['tendencia'] - df['sazonal']

# 3. Plotar os 4 gráficos (idêntico ao 'plot(decomposicao)' do R)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
fig.suptitle('Decomposição Aditiva da Série Temporal (Mock)', fontsize=16)

ax1.plot(df.index, df['engajamento'], label='Observado')
ax1.set_ylabel('Observado')
ax1.legend()

ax2.plot(df.index, df['tendencia'], label='Tendência')
ax2.set_ylabel('Tendência')
ax2.legend()

ax3.plot(df.index, df['sazonal'], label='Sazonalidade')
ax3.set_ylabel('Sazonalidade')
ax3.legend()

ax4.plot(df.index, df['residuo'], 'o', markersize=4, label='Resíduo')
ax4.set_ylabel('Resíduo')
ax4.legend()

plt.xlabel('Data')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 4. Salvar o arquivo
output_file = 'engagement_timeseries.png'
plt.savefig(output_file)

print(f"Gráfico '{output_file}' gerado com sucesso usando Python.")