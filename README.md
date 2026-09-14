# Fluxo · Laboratório de arquiteturas

Protótipo funcional do esboço de gerenciamento de trânsito. Um dashboard em português permite experimentar **Blackboard, MVC e Multitiers** usando os mesmos sensores e regras determinísticas.

## Executar

Requer **Python 3.10+**. Não precisa instalar pacotes, Node, banco externo ou fontes da internet.

```bash
python3 run.py
```

Abra **http://localhost:3000**. Encerre com Ctrl+C.

Para demonstrar a separação dos tiers, execute em dois terminais, na raiz:

```bash
python3 server.py
```

```bash
python3 -m http.server 3000 --bind 127.0.0.1 --directory multitiers/frontend
```

O frontend também aceita `http://localhost:3000/?api=http://localhost:8001` quando a API inicia com `python3 server.py --port 8001`.

## Experimentar

1. Observe Avenida A e Rua C críticas no dataset inicial.
2. Selecione uma via no mapa, no card ou no seletor de sensores.
3. Ajuste velocidade, fluxo, clima, acidente, tempo verde e evento esportivo. Clique em **Aplicar sensores e analisar**.
4. Alterne a arquitetura: a entrada é preservada; o rastro e o estado JSON revelam a organização interna.
5. Experimente cenários prontos, leituras aleatórias e cards/tabela.
6. Abra **Comparar arquiteturas** e execute a comparação. Ela verifica todos os campos dos resultados sobre uma cópia dos mesmos dados.
7. Use o guia integrado para conduzir o seminário.

## Estrutura

- `shared/`: dataset e contrato comum de regras.
- `blackboard/`: quadro, especialistas independentes e controlador de execução.
- `mvc/models/`: Model responsável pela análise.
- `mvc/controllers/`: Controller que coordena Model e View.
- `mvc/views/`: serialização para a View web compartilhada.
- `multitiers/frontend/`: apresentação HTML/CSS/JavaScript, sem cálculo de congestionamento.
- `multitiers/backend/services/`: análise e recomendações do Business Tier.
- `multitiers/backend/repositories/`: acesso transacional ao SQLite.
- `multitiers/database/traffic.db`: criado automaticamente pela API.
- `server.py`: adaptador HTTP compartilhado e validação de entrada.

As três implementações executam de verdade no backend. O seletor escolhe a implementação que processa a requisição; não troca apenas a descrição. O frontend é reutilizado para uma comparação visual justa. MVC usa uma View JSON e a apresentação web comum. Os tiers de apresentação e negócio são processos distintos; SQLite é embarcado, isolado por repositório, sem servidor de banco separado.

## API

- `GET /api/roads`: dataset inicial compartilhado.
- `POST /api/analyze`: `{ "architecture": "blackboard|mvc|multitiers", "roads": [...] }` → vias analisadas, rastro por via e duração de processamento. Blackboard inclui também o quadro.

A leitura ativa fica no navegador. Multitiers persiste a última análise em SQLite; restaurar e recarregar usam o dataset inicial. Simulação e presets produzem entradas no frontend, enquanto toda decisão de trânsito é calculada no backend.

## Verificar

```bash
python3 -m unittest discover -s tests -v
node --check multitiers/frontend/app.js
```

Testes cobrem cenários esperados, limites das regras, equivalência em 288 combinações de sensores, extensão EventExpert, persistência e validação. Node é opcional, utilizado apenas para checagem de sintaxe JavaScript.

## Limites da demonstração

Mapa esquemático e sensores simulados. Recomendações não alteram automaticamente o tempo verde. O evento esportivo acrescenta um nível nas três versões; em Blackboard, isso ativa um especialista adicional. Tempos mostrados são medições reais do processamento local, incluem persistência em Multitiers e não são um benchmark de superioridade arquitetural. Não há cluster, implantação distribuída do banco nem controle de dispositivos reais.

## Portas ocupadas

O inicializador verifica as portas antes de criar os processos e só anuncia os links depois que os dois servidores respondem. Se outra execução já estiver aberta, use-a ou encerre com Ctrl+C no terminal correspondente. Para usar portas diferentes:

```bash
python3 run.py --frontend-port 3001 --api-port 8001
```

Abra o link completo impresso, que inclui a configuração da API. O inicializador não encerra processos de outras execuções.

## Foco didático

Cada arquitetura tem um painel com características, situações de aplicação, benefícios, limitações, trade-off principal e evidência observável. Na comparação, selecione uma mudança de requisito: evento esportivo, nova apresentação ou 100.000 usuários. O painel apresenta o impacto e uma pergunta para discussão, distinguindo experimentos implementados de possibilidades conceituais.

MVC, Blackboard e Multitiers tratam dimensões diferentes e podem coexistir em um sistema. A demonstração não pretende determinar uma alternativa universalmente superior.
