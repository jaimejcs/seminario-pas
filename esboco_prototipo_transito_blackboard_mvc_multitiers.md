# Protótipo comparativo: Sistema Inteligente de Gerenciamento de Trânsito

## 1. Objetivo do protótipo

Criar três implementações demonstrativas do mesmo sistema de gerenciamento de trânsito inteligente, cada uma organizada segundo um estilo arquitetural diferente:

1. **Blackboard**
2. **MVC**
3. **Multitiers**

O objetivo não é desenvolver três sistemas completos de produção, mas criar protótipos funcionais e comparáveis que permitam demonstrar visualmente:

- como cada arquitetura organiza responsabilidades;
- como os componentes interagem;
- como uma mesma funcionalidade é implementada de formas diferentes;
- quais trade-offs surgem em:
  - manutenibilidade;
  - desempenho;
  - escalabilidade;
  - flexibilidade;
  - complexidade.

As três versões devem resolver o **mesmo problema**, usar o **mesmo conjunto de dados simulados** e apresentar resultados equivalentes.

---

# 2. Cenário comum

Uma cidade deseja monitorar o trânsito de uma região central em tempo quase real.

O sistema recebe informações simuladas de:

- sensores de velocidade média;
- volume de veículos;
- semáforos;
- câmeras;
- acidentes;
- condições climáticas.

A partir dessas informações, o sistema deve identificar situações de congestionamento e recomendar ações para melhorar o fluxo.

Exemplo:

```text
Avenida A
Velocidade média: 18 km/h
Fluxo: 92 veículos/min
Semáforo: ciclo de 60 s
Acidente: não
Chuva: forte

Resultado:
- Congestionamento alto
- Possível causa: alto fluxo + chuva
- Recomendação: aumentar em 15 s o tempo verde da Avenida A
```

O sistema é apenas uma **simulação acadêmica**.

Nenhum dispositivo físico, integração com câmeras reais, GPS ou infraestrutura urbana real é necessário.

---

# 3. Escopo funcional comum às três versões

Todas as arquiteturas devem implementar as mesmas funcionalidades.

## 3.1 Visualização das vias

Exibir pelo menos quatro vias monitoradas:

- Avenida A;
- Avenida B;
- Rua C;
- Rua D.

Cada via deve possuir:

- velocidade média;
- volume de veículos;
- estado do trânsito;
- estado do semáforo;
- ocorrência de acidente;
- condição climática;
- nível de congestionamento.

Estados possíveis:

```text
NORMAL
MODERADO
ALTO
CRÍTICO
```

---

## 3.2 Simulação de sensores

Os sensores devem ser simulados.

Exemplo de estrutura:

```json
{
  "road": "Avenida A",
  "average_speed": 18,
  "vehicles_per_minute": 92,
  "traffic_light_green_time": 30,
  "accident": false,
  "weather": "heavy_rain"
}
```

O sistema pode gerar novos valores automaticamente ou permitir um botão:

```text
[ Simular nova leitura ]
```

Não é necessário utilizar comunicação IoT real.

---

## 3.3 Detecção de congestionamento

Implementar uma regra simples e determinística.

Exemplo:

```text
SE velocidade < 20 km/h E fluxo > 80 veículos/min
    congestionamento = CRÍTICO

SENÃO SE velocidade < 30 km/h E fluxo > 60
    congestionamento = ALTO

SENÃO SE velocidade < 40 km/h
    congestionamento = MODERADO

SENÃO
    congestionamento = NORMAL
```

Acidentes e chuva podem aumentar o nível calculado.

Exemplo:

```text
Se acidente = true:
    elevar congestionamento em um nível

Se chuva = heavy_rain:
    elevar congestionamento em um nível
```

O comportamento deve ser igual nas três implementações.

---

## 3.4 Recomendação de ação

O sistema deve produzir uma recomendação simples.

Exemplos:

```text
NORMAL
Nenhuma intervenção necessária.

MODERADO
Monitorar via.

ALTO
Aumentar tempo verde do semáforo em 10 segundos.

CRÍTICO
Aumentar tempo verde em 15 segundos e emitir alerta ao operador.
```

Se houver acidente:

```text
Prioridade: atendimento do incidente.
Recomendar desvio de tráfego.
```

---

# 4. Interface comum

As três implementações devem possuir uma interface visual semelhante para evitar que a qualidade da interface influencie a comparação.

Sugestão:

```text
+------------------------------------------------------+
| SMART TRAFFIC CONTROL                               |
+------------------------------------------------------+

[ Simular nova leitura ]

Avenida A
---------------------------------
Velocidade: 18 km/h
Fluxo: 92 veículos/min
Clima: Chuva forte
Acidente: Não
Congestionamento: CRÍTICO

Recomendação:
Aumentar verde em 15 segundos.

---------------------------------

Avenida B
...
```

Opcionalmente, usar cards.

Não é necessário implementar mapa geográfico real.

---

# 5. Dataset inicial

Criar um arquivo compartilhado entre os projetos contendo dados iniciais.

Exemplo:

```json
[
  {
    "id": 1,
    "road": "Avenida A",
    "average_speed": 18,
    "vehicles_per_minute": 92,
    "traffic_light_green_time": 30,
    "accident": false,
    "weather": "heavy_rain"
  },
  {
    "id": 2,
    "road": "Avenida B",
    "average_speed": 42,
    "vehicles_per_minute": 45,
    "traffic_light_green_time": 40,
    "accident": false,
    "weather": "clear"
  },
  {
    "id": 3,
    "road": "Rua C",
    "average_speed": 25,
    "vehicles_per_minute": 70,
    "traffic_light_green_time": 25,
    "accident": true,
    "weather": "clear"
  },
  {
    "id": 4,
    "road": "Rua D",
    "average_speed": 50,
    "vehicles_per_minute": 35,
    "traffic_light_green_time": 35,
    "accident": false,
    "weather": "light_rain"
  }
]
```

---

# 6. Implementação 1 — Blackboard

## 6.1 Objetivo arquitetural

Demonstrar uma arquitetura na qual diferentes componentes especializados analisam informações independentes e colaboram por meio de uma estrutura compartilhada denominada **Blackboard**.

O foco desta versão é mostrar:

- colaboração entre especialistas;
- baixo acoplamento entre módulos de análise;
- facilidade para adicionar novos especialistas;
- complexidade de coordenação e rastreamento das decisões.

---

# 6.2 Estrutura conceitual

```text
             Sensor Simulator
                    |
                    v
          +-------------------+
          |    BLACKBOARD     |
          |-------------------|
          | sensor_data       |
          | observations      |
          | traffic_level     |
          | recommendations   |
          +-------------------+
            ^      ^       ^
            |      |       |
       +----+  +---+---+  +------+
       |       |       |         |
       v       v       v         v
   Speed    Volume   Accident  Weather
  Expert    Expert    Expert    Expert

                   |
                   v

          Recommendation Expert
```

---

# 6.3 Blackboard

Criar uma estrutura central contendo o estado atual.

Exemplo:

```python
blackboard = {
    "sensor_data": {},
    "observations": [],
    "traffic_level": None,
    "recommendations": []
}
```

O Blackboard deve registrar também **quem produziu cada conclusão**.

Exemplo:

```json
{
  "expert": "SpeedExpert",
  "message": "Low average speed detected",
  "severity": 2
}
```

Isso será importante para demonstrar a rastreabilidade das decisões.

---

# 6.4 Especialistas

Criar pelo menos os seguintes componentes.

## SpeedExpert

Analisa velocidade média.

Exemplo:

```text
< 20 km/h -> severidade 3
< 30 km/h -> severidade 2
< 40 km/h -> severidade 1
```

---

## VolumeExpert

Analisa veículos por minuto.

Exemplo:

```text
> 80 -> severidade 3
> 60 -> severidade 2
> 45 -> severidade 1
```

---

## AccidentExpert

```text
accident = true
    severidade adicional = 3
```

---

## WeatherExpert

```text
heavy_rain -> severidade +1
light_rain -> observação
clear -> nenhuma alteração
```

---

## TrafficDecisionExpert

Analisa as conclusões existentes no Blackboard e determina:

```text
NORMAL
MODERADO
ALTO
CRÍTICO
```

---

## RecommendationExpert

Com base no resultado final, adiciona uma recomendação ao Blackboard.

---

# 6.5 Controlador do Blackboard

Criar um componente simples responsável por executar os especialistas.

Exemplo:

```text
1. inserir dados dos sensores;
2. executar SpeedExpert;
3. executar VolumeExpert;
4. executar AccidentExpert;
5. executar WeatherExpert;
6. executar TrafficDecisionExpert;
7. executar RecommendationExpert;
8. devolver o estado final.
```

Embora exista uma ordem no protótipo, deixar claro no código que os especialistas conhecem apenas o Blackboard, e não uns aos outros.

---

# 6.6 Demonstração importante

A interface deve permitir visualizar algo semelhante a:

```text
BLACKBOARD - Avenida A

Sensor Data
-----------
Speed: 18 km/h
Traffic: 92 vehicles/min
Weather: Heavy Rain

Expert Contributions
--------------------

SpeedExpert
Low speed detected
Severity: 3

VolumeExpert
Very high vehicle volume
Severity: 3

WeatherExpert
Heavy rain detected
Severity modifier: +1

TrafficDecisionExpert
Traffic state: CRITICAL

RecommendationExpert
Increase green light by 15 seconds
```

Essa tela é importante para demonstrar como a solução foi construída coletivamente.

---

# 6.7 Extensão demonstrativa

Adicionar opcionalmente um novo especialista:

```text
EventExpert
```

Ele poderia detectar:

```text
football_match = true
```

e aumentar o risco de congestionamento.

O objetivo é mostrar que um novo especialista pode ser incluído sem alterar os especialistas existentes.

---

# 7. Implementação 2 — MVC

## 7.1 Objetivo arquitetural

Demonstrar separação entre:

```text
MODEL
VIEW
CONTROLLER
```

O foco deve ser:

- separação de responsabilidades;
- facilidade de manutenção;
- simplicidade de entendimento;
- forte adequação para aplicações interativas.

---

# 7.2 Estrutura conceitual

```text
                  USER
                   |
                   v
              +----------+
              |   VIEW   |
              +----------+
                   |
                   v
             +------------+
             | CONTROLLER |
             +------------+
                   |
                   v
              +---------+
              |  MODEL  |
              +---------+
```

---

# 7.3 Model

O Model deve representar:

```text
Road
TrafficData
TrafficLight
TrafficAnalysis
```

Exemplo:

```python
class Road:
    id
    name
    average_speed
    vehicles_per_minute
    traffic_light_green_time
    accident
    weather
```

O Model também pode conter a lógica:

```text
calculate_congestion()
generate_recommendation()
```

---

# 7.4 Controller

Responsável por receber eventos da interface.

Exemplos:

```text
GET /
GET /roads
POST /simulate
POST /roads/{id}/simulate
```

Fluxo:

```text
Usuário
   |
   v
Controller
   |
   v
Model
   |
   v
Controller
   |
   v
View
```

---

# 7.5 View

A View deve apresentar:

- vias;
- métricas;
- congestionamento;
- recomendação;
- botão de simulação.

Exemplo:

```text
Dashboard
    |
    +-- Road Card
    +-- Road Card
    +-- Road Card
    +-- Road Card
```

---

# 7.6 Organização sugerida

```text
mvc/
|
+-- controllers/
|   +-- traffic_controller.*
|
+-- models/
|   +-- road.*
|   +-- traffic_analysis.*
|
+-- views/
|   +-- dashboard.*
|   +-- road.*
|
+-- services/
|   +-- simulator.*
|
+-- data/
|   +-- roads.json
|
+-- app.*
```

---

# 7.7 Fluxo demonstrativo

Ao clicar em:

```text
Simular nova leitura
```

deve ocorrer:

```text
View

   |
   v

TrafficController.simulate()

   |
   v

TrafficSimulator

   |
   v

Road Model

   |
   v

TrafficAnalysis.calculate()

   |
   v

TrafficController

   |
   v

View atualizada
```

---

# 7.8 Demonstração importante

Durante a apresentação, mostrar rapidamente o código separado em:

```text
models/
views/
controllers/
```

e explicar que mudanças de interface não exigem modificar diretamente a regra de negócio.

Exemplo:

```text
Trocar cards por tabela:

View muda.
Model permanece igual.
Controller praticamente permanece igual.
```

---

# 8. Implementação 3 — Multitiers

## 8.1 Objetivo arquitetural

Demonstrar separação da aplicação em camadas que podem ser distribuídas e implantadas independentemente.

Sugestão de três tiers:

```text
Presentation Tier
Application / Business Tier
Data Tier
```

---

# 8.2 Estrutura conceitual

```text
+------------------------------+
|      PRESENTATION TIER       |
|                              |
| Dashboard Web                |
+--------------+---------------+
               |
               | HTTP/REST
               v
+------------------------------+
|       BUSINESS TIER          |
|                              |
| Traffic API                  |
| Traffic Analyzer             |
| Recommendation Service       |
| Sensor Simulator             |
+--------------+---------------+
               |
               |
               v
+------------------------------+
|          DATA TIER           |
|                              |
| Roads                        |
| Sensor Data                  |
| Traffic Events               |
+------------------------------+
```

---

# 8.3 Presentation Tier

Responsável apenas pela interface.

Pode ser uma aplicação web simples.

Ela deve consumir uma API.

Exemplos:

```text
GET /api/roads

POST /api/simulation

GET /api/roads/{id}
```

A Presentation Tier não deve calcular congestionamento.

---

# 8.4 Business Tier

Responsável pelas regras de negócio.

Componentes:

```text
TrafficService
TrafficAnalyzer
RecommendationService
SensorSimulator
```

Exemplo:

```text
TrafficAnalyzer
    |
    +-- calculateCongestion()
```

```text
RecommendationService
    |
    +-- generateRecommendation()
```

---

# 8.5 Data Tier

Pode usar:

```text
SQLite
```

ou até persistência JSON, caso o tempo seja limitado.

Entretanto, estruturalmente deve existir uma camada separada responsável por acesso aos dados.

Exemplo:

```text
RoadRepository
TrafficEventRepository
```

A Business Tier não deve acessar diretamente arquivos ou SQL espalhado pelo código.

---

# 8.6 Organização sugerida

```text
multitiers/
|
+-- frontend/
|   +-- ...
|
+-- backend/
|   |
|   +-- controllers/
|   +-- services/
|   +-- repositories/
|   +-- models/
|   |
|   +-- app.*
|
+-- database/
|   +-- traffic.db
|
+-- docker-compose.yml
```

---

# 8.7 Comunicação entre tiers

A comunicação entre frontend e backend deve ocorrer por HTTP.

Exemplo:

```http
GET /api/roads
```

Resposta:

```json
[
  {
    "road": "Avenida A",
    "average_speed": 18,
    "vehicles_per_minute": 92,
    "congestion": "CRITICAL",
    "recommendation": "Increase green time by 15 seconds"
  }
]
```

---

# 8.8 Demonstração importante

Mostrar que frontend e backend podem executar separadamente.

Exemplo:

```text
Terminal 1

frontend
localhost:3000
```

```text
Terminal 2

backend
localhost:8000
```

Explicar:

```text
Se o número de usuários aumentar,
o Business Tier poderia possuir múltiplas instâncias.

Se o volume de dados crescer,
a camada de dados pode ser escalada independentemente.
```

Não é necessário implementar cluster ou autoscaling.

O conceito deve apenas ficar evidente na arquitetura.

---

# 9. Tecnologias sugeridas

O agente pode escolher tecnologias equivalentes, mas uma opção simples é:

## Backend

```text
Python
FastAPI ou Flask
```

## Frontend

```text
HTML
CSS
JavaScript
```

ou:

```text
React
```

caso não aumente excessivamente a complexidade.

## Persistência

```text
JSON
```

ou:

```text
SQLite
```

## Execução

Preferencialmente:

```text
Docker / Docker Compose
```

mas isso é opcional.

O mais importante é a clareza arquitetural.

---

# 10. Organização geral do repositório

Sugestão:

```text
smart-traffic-architecture-demo/
|
+-- README.md
|
+-- shared/
|   +-- sample-data.json
|   +-- traffic-rules.md
|
+-- blackboard/
|   +-- ...
|
+-- mvc/
|   +-- ...
|
+-- multitiers/
|   +-- ...
|
+-- docs/
    +-- architecture-blackboard.md
    +-- architecture-mvc.md
    +-- architecture-multitiers.md
```

Cada projeto deve possuir seu próprio:

```text
README.md
```

com instruções de execução.

---

# 11. Garantia de comparabilidade

As três arquiteturas devem obrigatoriamente usar:

- os mesmos nomes de vias;
- os mesmos dados iniciais;
- as mesmas regras de congestionamento;
- as mesmas recomendações;
- funcionalidades equivalentes.

O que muda é **a organização arquitetural**, não o problema resolvido.

---

# 12. Cenário principal de demonstração

Criar um cenário controlado chamado:

```text
Rush Hour Scenario
```

Dados:

```text
Avenida A

Speed: 18 km/h
Vehicles/min: 92
Weather: Heavy Rain
Accident: false
```

Resultado esperado:

```text
Congestion: CRITICAL
```

Recomendação:

```text
Increase traffic light green time by 15 seconds.
```

Esse cenário deve produzir o mesmo resultado nas três arquiteturas.

---

# 13. Segundo cenário

```text
Rua C

Speed: 25 km/h
Vehicles/min: 70
Weather: Clear
Accident: true
```

Resultado esperado:

```text
Congestion: CRITICAL
```

Recomendação:

```text
Prioritize incident response and redirect traffic.
```

---

# 14. Elementos visuais úteis para o seminário

Cada versão deve exibir em alguma parte da interface:

```text
Architecture: BLACKBOARD
```

ou:

```text
Architecture: MVC
```

ou:

```text
Architecture: MULTITIERS
```

Também é desejável disponibilizar uma pequena visualização da arquitetura.

---

# 15. Comparação que o protótipo deve permitir

Após desenvolver as três versões, deve ser possível discutir:

| Critério | Blackboard | MVC | Multitiers |
|---|---|---|---|
| Manutenibilidade | Média | Alta | Alta, porém mais complexa |
| Flexibilidade | Muito alta | Média | Alta |
| Escalabilidade | Média | Limitada isoladamente | Alta |
| Complexidade | Alta | Baixa/Média | Alta |
| Desempenho | Depende da coordenação | Bom em aplicação simples | Overhead de comunicação |
| Extensibilidade | Muito alta para novos especialistas | Boa para mudanças estruturadas | Alta para novos serviços |
| Distribuição | Não é o foco | Não é o foco | Forte |
| Facilidade de depuração | Menor | Alta | Média |

Esses valores não devem ser tratados como regras absolutas.

O objetivo é utilizá-los como ponto inicial de discussão.

---

# 16. Mudança arquitetural para demonstrar trade-offs

Após implementar a versão mínima, realizar mentalmente ou demonstrar uma mudança de requisito.

Novo requisito:

```text
Adicionar análise de eventos esportivos que podem aumentar o fluxo de veículos.
```

## Blackboard

Adicionar:

```text
EventExpert
```

Impacto esperado:

```text
baixo
```

Os demais especialistas não precisam conhecer o novo componente.

---

## MVC

Adicionar informação ao Model:

```text
TrafficEvent
```

Alterar:

```text
TrafficAnalysis
Controller
View
```

Impacto esperado:

```text
moderado
```

---

## Multitiers

Pode exigir:

```text
novo endpoint
novo serviço
alteração de modelo
persistência
mudança no frontend
```

Impacto inicial:

```text
maior
```

Porém essa separação facilita evolução e escalabilidade futura.

---

# 17. Segundo trade-off demonstrável

Novo requisito:

```text
O sistema passará de 100 para 100.000 usuários simultâneos.
```

## Blackboard

O problema principal pode aparecer na coordenação e no Blackboard compartilhado.

## MVC

Uma aplicação MVC monolítica precisaria de estratégias adicionais de distribuição.

## Multitiers

A arquitetura permite escalar separadamente:

```text
frontend
backend
database
```

Mostrando por que a maior complexidade inicial pode ser justificada.

---

# 18. Logs e observabilidade

Para facilitar a apresentação, cada versão deve gerar logs indicando o fluxo interno.

## Blackboard

```text
[SpeedExpert] analyzing Avenida A
[VolumeExpert] analyzing Avenida A
[WeatherExpert] heavy rain detected
[TrafficDecisionExpert] result=CRITICAL
```

## MVC

```text
[Controller] simulate request
[Model] updating road data
[Model] congestion calculated
[View] dashboard rendered
```

## Multitiers

```text
[Frontend] GET /api/roads
[API] request received
[TrafficService] analyzing roads
[Repository] loading road data
```

Isso ajuda muito a demonstrar a diferença entre os estilos.

---

# 19. O que NÃO implementar

Para manter o protótipo viável, não implementar:

- machine learning real;
- reconhecimento de imagem;
- câmeras reais;
- mapas GIS;
- Google Maps;
- integração com semáforos reais;
- MQTT real;
- Kafka;
- Kubernetes;
- infraestrutura cloud;
- autenticação;
- controle de usuários;
- alta disponibilidade;
- banco distribuído;
- algoritmos avançados de otimização de tráfego.

Esses itens podem ser mencionados como evolução futura.

---

# 20. Critérios de conclusão

O protótipo estará completo quando:

### Blackboard

- sensores simulados alimentarem o Blackboard;
- pelo menos quatro especialistas analisarem os dados;
- for possível visualizar as contribuições dos especialistas;
- existir uma decisão final;
- existir uma recomendação.

### MVC

- Model, View e Controller estiverem claramente separados;
- o usuário puder executar nova simulação;
- o Controller coordenar a operação;
- o Model executar a regra de negócio;
- a View apresentar os resultados.

### Multitiers

- frontend e backend forem aplicações separadas;
- frontend consumir uma API;
- Business Tier possuir regras de negócio;
- Data Tier estiver isolado por repositórios;
- os três tiers forem identificáveis na estrutura do projeto.

---

# 21. Prioridade para o agente implementador

Priorizar nesta ordem:

1. clareza arquitetural;
2. funcionamento do fluxo principal;
3. equivalência funcional entre as três versões;
4. facilidade de demonstração;
5. interface visual limpa;
6. qualidade do código;
7. funcionalidades adicionais.

Não adicionar funcionalidades que dificultem compreender a arquitetura.

---

# 22. Resultado final esperado

Ao término deve ser possível executar três protótipos e demonstrar:

```text
MESMO PROBLEMA
      |
      +-------------------+
      |         |         |
      v         v         v
 Blackboard    MVC    Multitiers
      |         |         |
      v         v         v
 mesmo resultado funcional
```

Porém com estruturas internas distintas.

A pergunta central do seminário deve permanecer:

> Como a escolha de uma arquitetura altera a forma de organizar o sistema e quais atributos de qualidade são favorecidos ou prejudicados por essa decisão?

O protótipo não deve tentar provar que uma arquitetura é universalmente superior.

Ele deve tornar os **trade-offs visíveis**.
