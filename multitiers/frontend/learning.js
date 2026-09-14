export const learning = {
 blackboard: {
  characteristic:'Conhecimento compartilhado e especialistas independentes, coordenados por um mecanismo de controle.',
  application:'Problemas que combinam fontes de conhecimento distintas: diagnóstico, interpretação de sinais e planejamento com hipóteses parciais.',
  benefit:'Novos especialistas podem contribuir sem conhecer a implementação dos demais.',
  limitation:'O quadro vira ponto de coordenação. Conflitos, ordem de execução e critérios de parada exigem controle explícito.',
  tradeoff:'Maior extensibilidade dos especialistas em troca de maior esforço para coordenar e explicar a decisão global.',
  evidence:'Ative evento esportivo em uma via normal: EventExpert aparece no rastro e publica seu fato. Neste lab a agenda é fixa; resolução dinâmica de conflitos não foi implementada.'
 },
 mvc: {
  characteristic:'Separação de responsabilidades entre estado e regras (Model), apresentação (View) e tratamento das interações (Controller).',
  application:'Aplicações interativas e sistemas administrativos com telas que evoluem sobre regras de domínio relativamente estáveis.',
  benefit:'Facilita testar regras e modificar a apresentação de forma independente.',
  limitation:'Controllers podem acumular responsabilidades. MVC, por si só, não define distribuição, persistência ou escala.',
  tradeoff:'Clareza e facilidade de manutenção da interação em troca da disciplina para preservar as fronteiras e evitar Controllers excessivos.',
  evidence:'Troque cards por tabela e acompanhe o rastro View → Controller → Model. A análise permanece a mesma; essa troca é reutilizada nas três versões da interface.'
 },
 multitiers: {
  characteristic:'Separação entre apresentação, negócio e dados, com fronteiras que permitem implantação e evolução independentes.',
  application:'Sistemas com múltiplos clientes, negócio centralizado e necessidades distintas de capacidade, segurança ou implantação entre partes.',
  benefit:'Permite centralizar regras e planejar a expansão de capacidade por tier.',
  limitation:'Chamadas entre processos, contratos, falhas parciais e operação acrescentam complexidade. Escalar requer infraestrutura e desenho de estado.',
  tradeoff:'Independência de implantação e capacidade em troca de comunicação adicional e maior custo operacional.',
  evidence:'Observe HTTP → serviço → repositório no rastro. Frontend e API são processos distintos; SQLite é embarcado. Escala independente do banco e múltiplas instâncias são possibilidades, não recursos implementados.'
 }
};
export const challenges = {
 event: {title:'Adicionar análise de eventos esportivos', context:'O domínio precisa incorporar uma nova fonte de informação.', rows:[
 ['Blackboard','Registrar EventExpert e publicar um fato no quadro.','Preserva os outros especialistas, mas o contrato dos fatos e a decisão precisam aceitar a contribuição.'],
 ['MVC','Adicionar o atributo de evento ao Model e expor o controle na View.','A separação ajuda a localizar mudanças; a regra e os dados ainda precisam evoluir.'],
 ['Multitiers','Evoluir entrada da API, serviço e persistência do evento.','Mais fronteiras para manter compatíveis; clientes distintos reutilizam a regra central.']], question:'A frequência de novos especialistas justifica o custo de coordenação do Blackboard?', experiment:'Experimento disponível: use Fluxo livre, ative evento esportivo, aplique e compare as arquiteturas.'},
 interface: {title:'Trocar o dashboard por outra apresentação',context:'O domínio permanece igual, mas o usuário precisa consumir os dados de outra forma.',rows:[
 ['Blackboard','Construir outra visualização do quadro.','O quadro pode servir várias apresentações; é preciso controlar o acoplamento ao formato interno.'],
 ['MVC','Modificar a View mantendo o Model.','Benefício direto da separação; mudanças na interação podem também exigir Controller.'],
 ['Multitiers','Adicionar outro frontend consumidor da API.','Reutiliza o negócio, mas exige um contrato de API estável.']],question:'A mudança é apenas visual ou exige novos casos de uso e contratos?',experiment:'Experimento disponível: alterne entre cards e tabela. As regras de congestionamento não mudam.'},
 scale: {title:'Passar de 100 para 100.000 usuários',context:'Discussão arquitetural: o laboratório não executa um teste de carga dessa magnitude.',rows:[
 ['Blackboard','Investigar contenção, particionamento e coordenação do quadro.','Distribuir especialistas não elimina disputas por estado compartilhado.'],
 ['MVC','Planejar réplicas, cache e gerenciamento de estado da aplicação.','MVC organiza responsabilidades; não impede distribuição, mas não a resolve sozinho.'],
 ['Multitiers','Medir gargalos e planejar capacidade por tier.','A separação favorece escalabilidade independente, com custos de rede, observabilidade e operação.']],question:'Qual tier é o gargalo e que evidência justificaria distribuí-lo?',experiment:'Discussão conceitual: os tempos locais exibidos não permitem extrapolar capacidade para 100.000 usuários.'}
};
