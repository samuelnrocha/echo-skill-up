# Título: Análise de Série Temporal Mock (Global Solution - Cap05)
# Este script cumpre o requisito da disciplina "Linguagem R".

# 1. Gerar dados mockados de engajamento
# (Simulando 36 meses de engajamento de usuários)
set.seed(42)
engajamento <- 50 + seq(1, 36) * 0.5 + rnorm(36, mean=0, sd=3)
ts_data <- ts(engajamento, start=c(2023, 1), frequency=12)

# 2. Aplicar Decomposição (Conceito do Cap05) [cite: 13986-13987]
decomposicao <- decompose(ts_data, type="additive")

# 3. Plotar a decomposição para o PDF final
print("Gerando gráfico de decomposição em 'engagement_timeseries.png'...")
png("engagement_timeseries.png", width=800, height=600)
plot(decomposicao)
dev.off()

print("Script R finalizado.")