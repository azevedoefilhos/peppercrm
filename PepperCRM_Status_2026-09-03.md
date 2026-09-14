# PepperCRM — Status do Projeto (atualizado em 03/09/2026)

> Este arquivo substitui o .md de julho. Foi reconstruído a partir da conversa
> "Desenvolvimento do PepperCRM" que atingiu o limite de compactação em 02-03/09/2026.
> Cole este conteúdo como primeira mensagem em um novo chat para retomar com contexto completo.

## Sobre o projeto
PepperCRM é um CRM em Streamlit para representantes comerciais e agências de
merchandising no Brasil, desenvolvido por Fernando Azevedo Jr. (dono/MASTER).
Deploy: Railway (PostgreSQL) + GitHub (deploy automático). Desenvolvimento local
via PyCharm no Windows.

## O que está funcionando bem
- Autenticação e perfis de acesso por colaborador
- Módulos: Clientes, Pedidos, Ver Pedidos, Contatos, Pesquisa PDV, Despesas,
  Relatórios, Visitas, Metas, Comissões, Resultado Operacional, Fornecedores,
  Produtos, Tabelas de Preço
- Filtros por carteira (`get_where_cliente()` / `get_lista_clientes()` em
  `permissoes.py`) implementados na quase totalidade dos módulos
- Módulo Roteiros com estrutura sólida recém-implementada
- Banco PostgreSQL no Railway estável; deploy automático via GitHub

## Em andamento / pendente
- **Filtros de perfil em Despesas**: linhas 572 e 635 de `despesas.py` ainda
  estavam sem filtro (linhas 296-301 já corretas, filtram por `usuario_id`)
- **Módulo Roteiros**: funcional mas incompleto — faltam testes por perfil
  (Execução do Dia, Cobertura e Alertas, Roteiro Supervisor com Gabriel,
  migração automática quando promotor recebe login)
- Alertas do dashboard por perfil — não implementados
- Módulo Configuração, aba Sistema — pendente

## Bugs recentes reportados (última sessão, 02/09)
- **Equipe**: Enrico Guastaferro (Promotor Vendedor) aparecia incorretamente
  também na lista de Promotores, além de aparecer corretamente na lista de
  Promotor Vendedor — regressão, não acontecia antes
- **Erro de conexão Railway**: `psycopg2.OperationalError: connection to
  server at "kodama.proxy.rlwy.net" (66.33.22.228), port 49266 failed:
  server closed the connection unexpectedly` — ocorreu ao transitar entre
  abas Promotor/Vendedor no módulo Equipe
- Login com preenchimento automático do Firefox — bug conhecido, não corrigido

## Decisões arquiteturais recentes (ainda não implementadas)
- **ADM vs Representante ADM**: criar a condição de ADM (não só a nomenclatura)
  para clientes que são indústria/fornecedor, e não escritório de representante.
  Um colaborador de indústria não deve se enquadrar como "representante adm",
  apenas "adm". Todas as atribuições de representante adm se aplicam ao adm.
- Aba "Sistema" em Configuração: decidir futuramente se deve ser exclusiva ao
  ADM (para evitar que um usuário comum altere o Modo de operação inadvertidamente)
  — e trocar nomenclatura "Fornecedor" para "Indústria/Fornecedor" quando chegar a hora
- Marcelo (perfil Vendedor) não deveria ver a aba Usuários em Configuração
  (mensagem "Esta função é restrita ao administrador" a torna desnecessária);
  aba "Minha Empresa" pode ser visível mas não editável para usuário comum
- **Histórico vinculado ao cliente, não ao vendedor**: ao migrar carteira de um
  cliente entre vendedores, o novo responsável deve ver todo o histórico de
  pedidos e conversas anteriores, mantendo o vendedor original como autor
  desses registros antigos
- Ainda pendente: atribuir/migrar toda a carteira de clientes e PDVs de
  Fernando (MASTER) para os demais vendedores, para permitir testes de
  transferência de carteira

## Prioridades combinadas (ordem definida na última sessão)
**Prioridade 1 — Estabilizar o que existe (1-2 sessões)**
1. Testes completos por perfil: Marcelo (Vendedor), Sandra (Representante),
   Gabriel (Supervisor), Enrico (Promotor Vendedor), Francisco (Promotor)
2. Corrigir bugs encontrados nos testes (incluindo os do Equipe listados acima)
3. Alertas do dashboard por perfil

**Prioridade 2 — Completar Roteiros (2-3 sessões, sessão exclusiva)**
1. Aba Execução do Dia — testar e corrigir
2. Aba Cobertura e Alertas — testar
3. Roteiro Supervisor — testar com Gabriel
4. Migração automática quando promotor recebe login
5. Roteiro do vendedor por PDV / Roteiro do promotor com Google Maps /
   "Meu Roteiro" (visão pessoal por perfil)

**Prioridade 3 — Configuração e Sistema (1 sessão)**
1. Aba Sistema — modo de operação (Representante vs Indústria/Fornecedor)
2. Fix login Firefox
3. Nomenclatura ADM vs Representante ADM

**Prioridade 4 — Evolução do produto (sessões futuras)**
1. Google Maps Routes API quando tiver usuários pagantes
2. Notificações de PDV não visitado
3. Aba de pedidos cancelados/suspensos
4. Ranking PDV — definir status incluídos
5. Carteira de clientes visível no módulo Clientes

## Padrões técnicos importantes (não esquecer)
- SQL: sempre usar `OR` em vez de `IN` — bug de tradução em `_traduzir_sql_pg`
  no `database.py` (correção geral ainda pendente — identificar todos os
  lugares afetados e aplicar patch)
- Nunca usar `LEFT JOIN` com tabelas protegidas por RLS
- Usar scripts de restauração atômica em base64 (`fix_X_atomico.py`) para
  qualquer alteração de arquivo, rodados via CMD/PowerShell com PyCharm fechado
- Fernando prefere receber apenas arquivos modificados (não ZIPs completos) e
  quer scripts PowerShell incluídos junto com as atualizações
- Seis níveis de acesso: MASTER, ADM, REPRESENTANTE_ADM, VENDEDOR,
  PROMOTOR_VENDEDOR, PROMOTOR
- Tabela `promotor` usa campo `subtipo`: PROMOTOR, PROMOTOR_VENDEDOR, SEM_PROMOTOR

## Última troca do chat anterior (não respondida — retomar exatamente daqui)
A última resposta que o Claude enviou foi a avaliação técnica/estratégica
completa (resumida abaixo). Em seguida, Fernando enviou esta pergunta, que
ficou sem resposta porque a conversa não pôde mais ser compactada:

> "Boa tarde. Irei iniciar os testes acessando com perfis diferentes de
> usuários para primeiramente verificar se os módulos e abas habilitadas
> estão corretos para cada nível de acesso, lembrando que já validamos isso
> para a função de vendedor: Marcelo. Para depois testar o funcionamento das
> ferramentas para cada um destes usuários. E finalmente poderemos buscar a
> validação dos alertas do dashboard. Ok?"

Ou seja: o plano de testes por perfil (Prioridade 1) já estava em execução —
Marcelo (Vendedor) já foi validado quanto a módulos/abas visíveis. Faltam:
Sandra (Representante), Gabriel (Supervisor), Enrico (Promotor Vendedor),
Francisco (Promotor). A ordem combinada é: 1) módulos/abas corretos por
perfil → 2) funcionamento das ferramentas por perfil → 3) alertas do dashboard.

## Avaliação estratégica (registrada na última sessão)
O app foi avaliado como genuinamente bom — uma ferramenta especializada para
representação comercial e merchandising, nicho que CRMs genéricos (Salesforce,
HubSpot, Pipedrive) não atendem bem por serem caros, complexos e não
adaptados à realidade do representante brasileiro.
