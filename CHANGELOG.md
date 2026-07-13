
---

## [2026-07-07/10] — D2 Multi-tenant

### Implementado
- **Fase 0** — tabela `empresa` criada, Azevedo e Filhos registrada como empresa_id=1
- **Fase A** — coluna `empresa_id DEFAULT 1` adicionada em 45 tabelas de negocio
  - Indices criados: idx_emp_cliente, idx_emp_fornecedor, idx_emp_pedido,
    idx_emp_contato, idx_emp_produto, idx_emp_usuario
- **Fase B** — Row Level Security (RLS) ativo em 44 tabelas
  - Policy `empresa_isolation` filtra automaticamente por empresa_id
  - `database.py`: funcao `_set_empresa_id()` injeta empresa_id em toda conexao
  - `database.py`: funcao `get_empresa_id()` disponivel para uso nos modulos
  - `auth.py`: login carrega empresa_id do usuario e salva na sessao
- **Fase C** — script `d2_faseC_nova_empresa.py` pronto para cadastrar novo cliente

### Fase D (pendente — fazer apos alguns dias de uso estavel)
- Adicionar NOT NULL no empresa_id de todas as tabelas
- Garantir que nenhum registro entre sem empresa_id

### Regras criticas D2
- NUNCA rodar ALTER TABLE com o app ativo — usar matar_conexoes.py antes
- Para nova empresa: preencher e rodar d2_faseC_nova_empresa.py
- RLS e transparente ao codigo — nenhuma query precisa ser alterada
- database.py injeta empresa_id automaticamente em toda conexao PostgreSQL

### Outros itens desta sessao
- `despesas.py`: media do veiculo busca ultima entrada do banco automaticamente
- `visitas.py` + `crm_app.py`: modulo renomeado para "Promotores & Roteiros"
- `crm_app.py`: botao Catalogo removido do menu (aba PDF permanece em Produtos)
- `database.py`: auto-migracao _migrar_pedido_minimo desativada (causava deadlock)
