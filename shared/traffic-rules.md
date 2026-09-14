# Contrato de regras

1. Velocidade < 20 km/h e fluxo > 80 veículos/min → CRÍTICO (3).
2. Caso contrário, velocidade < 30 e fluxo > 60 → ALTO (2).
3. Caso contrário, velocidade < 40 → MODERADO (1).
4. Caso contrário → NORMAL (0).

Acidente, chuva forte e evento esportivo acrescentam um nível cada, com teto 3. Chuva leve não agrava. Adotamos a regra comum de acidente +1 da seção 3 do esboço, garantindo equivalência entre implementações.

Normal: nenhuma intervenção. Moderado: monitorar. Alto: recomendar +10 segundos de verde. Crítico: recomendar +15 segundos e alerta. Acidente tem prioridade: atendimento e desvio, sem recomendação de aumento do verde. O tempo sugerido não é aplicado automaticamente.
