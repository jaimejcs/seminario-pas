# Multitiers

Na raiz, inicie `python3 server.py` e, em outro terminal, `python3 -m http.server 3000 --bind 127.0.0.1 --directory multitiers/frontend`. Abra http://localhost:3000 e selecione Multitiers.

Presentation Tier: `frontend/`, consumindo HTTP/JSON. Business Tier: `backend/services/`. Data Tier: `backend/repositories/`, responsável pelo SQLite em `database/traffic.db`. O banco é embarcado; não há processo de banco distribuído. Cada requisição salva e consulta seu conjunto de sensores em uma transação, mantendo consistência entre requisições concorrentes.
