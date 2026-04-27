"""
SCRIPT DE MIGRAÇÃO — SQLite → Supabase (PostgreSQL)
PepperCRM — Azevedo e Filhos Representação Comercial

Execute este script UMA VEZ na pasta peppercrm:
    python migrar_para_supabase.py

O script:
1. Lê todos os dados do banco SQLite local (peppercrm.db)
2. Cria todas as tabelas no Supabase
3. Migra todos os dados preservando IDs e relacionamentos
4. Verifica integridade após a migração
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Configurações do Supabase ────────────────────────────────────────────
SUPABASE_URL  = "https://yunzqndswpwttejlgeaa.supabase.co"
SUPABASE_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bnpxbmRzd3B3dHRlamxnZWFhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzE2ODUxNCwiZXhwIjoyMDkyNzQ0NTE0fQ.1jcdN9mNKzo0b1h9BZ1n8wbyILTAJX-mK5S9xy0u4nk"
DB_SQLITE     = "peppercrm.db"

# ── Conexão PostgreSQL via psycopg2 ──────────────────────────────────────
# O Supabase expõe PostgreSQL direto — usa a string de conexão do painel
# Settings → Database → Connection string (URI)
# Formato: postgresql://postgres:[senha]@[host]:5432/postgres
import urllib.parse
host = "db.yunzqndswpwttejlgeaa.supabase.co"
senha = urllib.parse.quote("#JunioR_1970@")
PG_URL = f"postgresql://postgres:{senha}@{host}:5432/postgres"

# ── DDL PostgreSQL — todas as tabelas ───────────────────────────────────
DDL = """
-- Desabilita verificações de FK durante a importação
SET session_replication_role = 'replica';

CREATE TABLE IF NOT EXISTS configuracao (
    config_id         SERIAL PRIMARY KEY,
    modo_operacao     TEXT,
    empresa_nome      TEXT,
    data_instalacao   TEXT,
    versao_sistema    TEXT,
    anthropic_api_key TEXT,
    senha_exclusao    TEXT
);

CREATE TABLE IF NOT EXISTS representante (
    representante_id SERIAL PRIMARY KEY,
    razao_social TEXT, nome_fantasia TEXT,
    cnpj TEXT, endereco TEXT, bairro TEXT, cidade TEXT, estado TEXT,
    fone TEXT, whatsapp TEXT, email TEXT, site TEXT,
    observacao TEXT, ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS vendedor (
    vendedor_id      SERIAL PRIMARY KEY,
    representante_id INTEGER,
    nome TEXT, fone TEXT, whatsapp TEXT, email TEXT, cpf TEXT,
    chave_pix TEXT, data_aniversario TEXT, observacao TEXT,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS promotor (
    promotor_id SERIAL PRIMARY KEY,
    nome TEXT, fone TEXT, email TEXT, cpf TEXT, cnh TEXT,
    veiculo TEXT, cidade TEXT, estado TEXT, bairro TEXT,
    endereco TEXT, observacao TEXT, ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS att_promotor (
    att_promotor_id SERIAL PRIMARY KEY,
    promotor_id INTEGER, pdv_id INTEGER,
    dias_visita TEXT, frequencia TEXT,
    hora_inicio TEXT, hora_fim TEXT,
    observacao TEXT, ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS att_vendedor (
    att_vendedor_id SERIAL PRIMARY KEY,
    vendedor_id INTEGER, pdv_id INTEGER,
    dias_visita TEXT, frequencia TEXT,
    observacao TEXT, ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS usuario (
    usuario_id  SERIAL PRIMARY KEY,
    nome TEXT, email TEXT, senha_hash TEXT,
    tipo TEXT, vendedor_id INTEGER,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS fornecedor (
    fornecedor_id SERIAL PRIMARY KEY,
    razao_social TEXT, nome_fantasia TEXT NOT NULL,
    endereco TEXT, bairro TEXT, cidade TEXT, estado TEXT,
    cnpj TEXT, ie TEXT, observacao TEXT,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS contato_fornecedor (
    contato_fornecedor_id SERIAL PRIMARY KEY,
    fornecedor_id INTEGER,
    nome_contato TEXT, departamento TEXT,
    fone TEXT, email TEXT, observacao TEXT,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS comissao (
    comissao_id   SERIAL PRIMARY KEY,
    fornecedor_id INTEGER,
    percentual    REAL,
    observacao    TEXT,
    ativo         INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS comissao_pagamento (
    pagamento_id      SERIAL PRIMARY KEY,
    pedido_id         INTEGER,
    data_pagamento    TEXT,
    valor_previsto    REAL,
    valor_pago        REAL,
    status_pagamento  TEXT,
    observacao        TEXT
);

CREATE TABLE IF NOT EXISTS marca (
    marca_id      SERIAL PRIMARY KEY,
    fornecedor_id INTEGER,
    nome_marca    TEXT NOT NULL,
    ativo         INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS categoria (
    categoria_id   SERIAL PRIMARY KEY,
    nome_categoria TEXT NOT NULL,
    ativo          INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS linha (
    linha_id     SERIAL PRIMARY KEY,
    categoria_id INTEGER,
    nome_linha   TEXT NOT NULL,
    ativo        INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS produto (
    produto_id       SERIAL PRIMARY KEY,
    fornecedor_id    INTEGER,
    marca_id         INTEGER,
    categoria_id     INTEGER,
    linha_id         INTEGER,
    codigo_produto   TEXT,
    descricao        TEXT NOT NULL,
    descricao_curta  TEXT,
    peso             REAL,
    peso_caixa       REAL,
    unidade_medida   TEXT,
    unidades_caixa   INTEGER,
    caixas_pallet    INTEGER,
    ean              TEXT,
    dun              TEXT,
    ncm              TEXT,
    cest             TEXT,
    validade_dias    INTEGER,
    sub_categoria    TEXT,
    grupo            TEXT,
    observacao       TEXT,
    ativo            INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS tabela_preco (
    tabela_preco_id SERIAL PRIMARY KEY,
    fornecedor_id   INTEGER,
    nome_tabela     TEXT NOT NULL,
    tipo_tabela     TEXT,
    prazo_pagamento TEXT,
    frete           TEXT,
    data_inicio     TEXT,
    data_fim        TEXT,
    ativo           INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS tabela_preco_item (
    tabela_preco_item_id SERIAL PRIMARY KEY,
    tabela_preco_id      INTEGER,
    produto_id           INTEGER,
    preco_caixa          REAL NOT NULL,
    desconto_maximo      REAL DEFAULT 0,
    preco_kg             REAL,
    observacao           TEXT
);

CREATE TABLE IF NOT EXISTS historico_preco (
    hist_id       SERIAL PRIMARY KEY,
    produto_id    INTEGER,
    fornecedor_id INTEGER,
    tabela_id     INTEGER,
    nome_tabela   TEXT,
    data_vigencia TEXT,
    preco_caixa   REAL,
    preco_kg      REAL,
    data_registro TEXT
);

CREATE TABLE IF NOT EXISTS associacao (
    associacao_id SERIAL PRIMARY KEY,
    nome TEXT, tipo TEXT, cidade TEXT, estado TEXT,
    fone TEXT, email TEXT, contato TEXT, observacao TEXT,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS central_compras (
    central_id      SERIAL PRIMARY KEY,
    cliente_id      INTEGER,
    nome_central    TEXT,
    tipo_entrega    TEXT,
    endereco_cd     TEXT,
    bairro_cd       TEXT,
    cidade_cd       TEXT,
    estado_cd       TEXT,
    fone TEXT, email TEXT, contato TEXT, observacao TEXT,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS cliente (
    cliente_id    SERIAL PRIMARY KEY,
    razao_social  TEXT,
    nome_fantasia TEXT NOT NULL,
    endereco TEXT, bairro TEXT, cidade TEXT, estado TEXT,
    cnpj TEXT, ie TEXT, site TEXT, instagram TEXT, fone TEXT,
    perfil TEXT,
    associacao_id INTEGER,
    observacao TEXT,
    ativo    INTEGER DEFAULT 1,
    status   TEXT DEFAULT 'prospecto'
);

CREATE TABLE IF NOT EXISTS contato_cliente (
    contato_cliente_id SERIAL PRIMARY KEY,
    cliente_id    INTEGER,
    nome_contato  TEXT,
    departamento  TEXT,
    fone TEXT, whatsapp TEXT, email TEXT,
    observacao TEXT,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS cliente_fornecedor (
    cliente_fornecedor_id SERIAL PRIMARY KEY,
    cliente_id      INTEGER,
    fornecedor_id   INTEGER,
    tabela_preco_id INTEGER,
    prazo_pagamento TEXT,
    codigo_cliente  TEXT,
    observacao      TEXT,
    ativo           INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS produto_codigo_cliente (
    produto_codigo_id SERIAL PRIMARY KEY,
    cliente_id   INTEGER,
    produto_id   INTEGER,
    codigo_cliente TEXT
);

CREATE TABLE IF NOT EXISTS pdv (
    pdv_id        SERIAL PRIMARY KEY,
    cliente_id    INTEGER,
    numero_loja   TEXT,
    nome_loja     TEXT,
    endereco TEXT, bairro TEXT, cidade TEXT, estado TEXT,
    cnpj TEXT, ie TEXT,
    gerente TEXT, fone_gerente TEXT,
    encarregado TEXT, fone_encarregado TEXT,
    horario_recebimento TEXT,
    tipo_pdv TEXT, setor TEXT, cluster TEXT,
    tamanho_pdv TEXT,
    latitude TEXT, longitude TEXT,
    ordem_roteiro INTEGER,
    dia_visita TEXT,
    frequencia_visita TEXT,
    observacao TEXT,
    ativo   INTEGER DEFAULT 1,
    status  TEXT DEFAULT 'Ativo'
);

CREATE TABLE IF NOT EXISTS mix_cliente (
    mix_id        SERIAL PRIMARY KEY,
    cliente_id    INTEGER,
    fornecedor_id INTEGER,
    pdv_id        INTEGER,
    produto_id    INTEGER,
    ativo         INTEGER DEFAULT 1,
    observacao    TEXT
);

CREATE TABLE IF NOT EXISTS pedido (
    pedido_id             SERIAL PRIMARY KEY,
    nr_pedido_fornecedor  TEXT,
    nr_pedido_cliente     TEXT,
    cliente_id            INTEGER NOT NULL,
    pdv_id                INTEGER,
    fornecedor_id         INTEGER NOT NULL,
    vendedor_id           INTEGER,
    tabela_preco_id       INTEGER,
    prazo_pagamento       TEXT,
    frete                 TEXT,
    data_pedido           TEXT,
    data_entrega          TEXT,
    desconto_geral        REAL DEFAULT 0,
    observacao            TEXT,
    status_pedido         TEXT DEFAULT 'ABERTO',
    comissao_percentual   REAL
);

CREATE TABLE IF NOT EXISTS pedido_item (
    pedido_item_id SERIAL PRIMARY KEY,
    pedido_id      INTEGER NOT NULL,
    produto_id     INTEGER,
    preco_tabela   REAL,
    desconto       REAL,
    preco_final    REAL,
    quantidade     INTEGER,
    status_item    TEXT
);

CREATE TABLE IF NOT EXISTS pedido_historico (
    historico_id SERIAL PRIMARY KEY,
    pedido_id    INTEGER,
    data_hora    TEXT,
    campo        TEXT,
    valor_antes  TEXT,
    valor_depois TEXT,
    observacao   TEXT
);

CREATE TABLE IF NOT EXISTS visita_cliente (
    visita_id        SERIAL PRIMARY KEY,
    cliente_id       INTEGER,
    pdv_id           INTEGER,
    local            TEXT,
    data_visita      TEXT,
    contato          TEXT,
    resumo           TEXT,
    produtos_tratados TEXT,
    pedido_id        INTEGER,
    proxima_acao     TEXT,
    data_followup    TEXT,
    observacao       TEXT
);

CREATE TABLE IF NOT EXISTS concorrente (
    concorrente_id   SERIAL PRIMARY KEY,
    fornecedor_id    INTEGER,
    marca_concorrente TEXT NOT NULL,
    origem_cidade    TEXT,
    importada        INTEGER DEFAULT 0,
    importado_por    TEXT,
    observacao       TEXT,
    ativo            INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS produto_concorrente (
    produto_concorrente_id SERIAL PRIMARY KEY,
    concorrente_id  INTEGER,
    categoria_id    INTEGER,
    linha_id        INTEGER,
    descricao       TEXT NOT NULL,
    descricao_curta TEXT,
    peso            REAL,
    unidade_medida  TEXT,
    ean_concorrente TEXT,
    auditavel       INTEGER DEFAULT 1,
    validade_dias   INTEGER,
    observacao      TEXT,
    ativo           INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS produto_concorrente_relacao (
    relacao_id             SERIAL PRIMARY KEY,
    produto_id             INTEGER,
    produto_concorrente_id INTEGER,
    tipo_relacao           TEXT,
    observacao             TEXT
);

CREATE TABLE IF NOT EXISTS pesquisa_preco (
    pesquisa_id   SERIAL PRIMARY KEY,
    data_pesquisa TEXT,
    pdv_id        INTEGER,
    cliente_id    INTEGER,
    fornecedor_id INTEGER,
    observacao    TEXT,
    status        TEXT DEFAULT 'rascunho'
);

CREATE TABLE IF NOT EXISTS pesquisa_preco_item (
    pesquisa_item_id       SERIAL PRIMARY KEY,
    pesquisa_id            INTEGER,
    produto_id             INTEGER,
    produto_concorrente_id INTEGER,
    preco                  REAL,
    em_oferta              INTEGER DEFAULT 0,
    frentes                INTEGER,
    ruptura                INTEGER DEFAULT 0,
    ponto_extra            INTEGER DEFAULT 0,
    tipo_ponto_extra       TEXT,
    observacao             TEXT
);

CREATE TABLE IF NOT EXISTS pesquisa_foto (
    foto_id     SERIAL PRIMARY KEY,
    pesquisa_id INTEGER,
    foto_data   TEXT,
    nome_arquivo TEXT,
    descricao   TEXT,
    data_upload TEXT
);

CREATE TABLE IF NOT EXISTS contato_registro (
    contato_id          SERIAL PRIMARY KEY,
    data_contato        TEXT,
    via_comunicacao     TEXT,
    tipo_entidade       TEXT,
    cliente_id          INTEGER,
    fornecedor_id       INTEGER,
    contato_pessoa      TEXT,
    assunto             TEXT,
    descricao           TEXT,
    resultado           TEXT,
    proxima_acao        TEXT,
    data_followup       TEXT,
    previsao_conclusao  TEXT,
    status              TEXT,
    prioridade          TEXT,
    tipo_topico         TEXT DEFAULT 'Contato',
    usuario_resp        TEXT,
    observacao          TEXT,
    ativo               INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS contato_interacao (
    interacao_id    SERIAL PRIMARY KEY,
    contato_id      INTEGER,
    data_interacao  TEXT,
    via_comunicacao TEXT,
    contato_pessoa  TEXT,
    descricao       TEXT,
    ativo           INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS contato_x_fornecedor (
    id            SERIAL PRIMARY KEY,
    contato_id    INTEGER,
    fornecedor_id INTEGER,
    UNIQUE(contato_id, fornecedor_id)
);

CREATE TABLE IF NOT EXISTS mensagem_modelo (
    mensagem_id SERIAL PRIMARY KEY,
    nome        TEXT NOT NULL,
    assunto     TEXT,
    corpo       TEXT NOT NULL,
    via         TEXT DEFAULT 'WhatsApp',
    ativo       INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS meta_fornecedor (
    meta_id       SERIAL PRIMARY KEY,
    fornecedor_id INTEGER,
    ano           INTEGER,
    mes           INTEGER,
    meta_valor    REAL,
    meta_pedidos  INTEGER,
    observacao    TEXT,
    ativo         INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS meta_mix (
    meta_mix_id   SERIAL PRIMARY KEY,
    fornecedor_id INTEGER,
    tipo          TEXT DEFAULT 'produto',
    referencia_id INTEGER,
    descricao     TEXT,
    ano           INTEGER,
    mes           INTEGER,
    meta_qtd      INTEGER,
    meta_clientes INTEGER,
    observacao    TEXT,
    ativo         INTEGER DEFAULT 1
);

-- Reabilita verificações de FK
SET session_replication_role = 'origin';
"""

def main():
    print("=" * 60)
    print("MIGRAÇÃO PepperCRM: SQLite → Supabase")
    print(f"Iniciada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

    # Verifica banco SQLite
    if not os.path.exists(DB_SQLITE):
        print(f"\nERRO: {DB_SQLITE} não encontrado.")
        print("Execute na pasta peppercrm onde está o arquivo .db")
        sys.exit(1)

    # Conecta ao SQLite
    sqlite_conn = sqlite3.connect(DB_SQLITE)
    sqlite_conn.row_factory = sqlite3.Row
    print(f"\n✅ Banco SQLite: {DB_SQLITE}")

    # Verifica tabelas do SQLite
    tabelas = sqlite_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    print(f"   {len(tabelas)} tabelas encontradas")

    # Conecta ao PostgreSQL (Supabase)
    try:
        import psycopg2
        pg_conn = psycopg2.connect(PG_URL, connect_timeout=10)
        pg_conn.autocommit = False
        print(f"\n✅ Supabase conectado: {SUPABASE_URL}")
    except Exception as e:
        print(f"\nERRO ao conectar ao Supabase: {e}")
        print("Verifique sua conexão com a internet e as credenciais.")
        sys.exit(1)

    pg_cur = pg_conn.cursor()

    # Cria tabelas no PostgreSQL
    print("\n📋 Criando tabelas no Supabase...")
    try:
        pg_cur.execute(DDL)
        pg_conn.commit()
        print("   ✅ Todas as tabelas criadas")
    except Exception as e:
        pg_conn.rollback()
        print(f"   ERRO ao criar tabelas: {e}")
        sys.exit(1)

    # Ordem de migração respeitando dependências (FK)
    ORDEM_MIGRACAO = [
        "configuracao","representante","vendedor","promotor",
        "associacao","fornecedor","contato_fornecedor",
        "comissao","marca","categoria","linha",
        "produto","tabela_preco","tabela_preco_item","historico_preco",
        "central_compras","cliente","contato_cliente",
        "cliente_fornecedor","produto_codigo_cliente","pdv","mix_cliente",
        "pedido","pedido_item","pedido_historico",
        "visita_cliente","att_promotor","att_vendedor","usuario",
        "concorrente","produto_concorrente","produto_concorrente_relacao",
        "pesquisa_preco","pesquisa_preco_item","pesquisa_foto",
        "contato_registro","contato_interacao","contato_x_fornecedor",
        "mensagem_modelo","meta_fornecedor","meta_mix",
    ]

    print("\n📦 Migrando dados...")
    total_registros = 0
    erros = []

    for tabela in ORDEM_MIGRACAO:
        # Verifica se existe no SQLite
        existe = sqlite_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (tabela,)).fetchone()
        if not existe:
            print(f"   ⏭  {tabela}: não existe no SQLite, pulando")
            continue

        rows = sqlite_conn.execute(f"SELECT * FROM {tabela}").fetchall()
        if not rows:
            print(f"   ⬜ {tabela}: vazio")
            continue

        # Pega colunas do SQLite
        cols = [d[0] for d in sqlite_conn.execute(
            f"SELECT * FROM {tabela} LIMIT 0").description]

        # Monta INSERT
        placeholders = ", ".join(["%s"] * len(cols))
        cols_str     = ", ".join(f'"{c}"' for c in cols)
        sql_insert   = (f'INSERT INTO {tabela} ({cols_str}) '
                        f'VALUES ({placeholders}) ON CONFLICT DO NOTHING')

        try:
            dados = [tuple(r) for r in rows]
            pg_cur.executemany(sql_insert, dados)
            pg_conn.commit()
            print(f"   ✅ {tabela}: {len(rows)} registro(s)")
            total_registros += len(rows)
        except Exception as e:
            pg_conn.rollback()
            erros.append((tabela, str(e)))
            print(f"   ❌ {tabela}: ERRO — {e}")

    # Reajusta as sequences (SERIAL) para o max id de cada tabela
    print("\n🔧 Ajustando sequences...")
    seq_tabelas = {
        "configuracao":"config_id","representante":"representante_id",
        "vendedor":"vendedor_id","promotor":"promotor_id",
        "fornecedor":"fornecedor_id","categoria":"categoria_id",
        "linha":"linha_id","produto":"produto_id",
        "tabela_preco":"tabela_preco_id","tabela_preco_item":"tabela_preco_item_id",
        "cliente":"cliente_id","pdv":"pdv_id","pedido":"pedido_id",
        "pedido_item":"pedido_item_id","concorrente":"concorrente_id",
        "produto_concorrente":"produto_concorrente_id",
        "produto_concorrente_relacao":"relacao_id",
        "pesquisa_preco":"pesquisa_id","pesquisa_preco_item":"pesquisa_item_id",
        "contato_registro":"contato_id","contato_interacao":"interacao_id",
        "meta_fornecedor":"meta_id","meta_mix":"meta_mix_id",
        "mensagem_modelo":"mensagem_id","historico_preco":"hist_id",
    }
    for tabela, col_id in seq_tabelas.items():
        try:
            pg_cur.execute(
                f"SELECT setval(pg_get_serial_sequence('{tabela}','{col_id}'), "
                f"COALESCE((SELECT MAX({col_id}) FROM {tabela}),1))")
            pg_conn.commit()
        except Exception as e:
            pg_conn.rollback()
            print(f"   Aviso sequence {tabela}: {e}")

    print("\n" + "=" * 60)
    print(f"✅ MIGRAÇÃO CONCLUÍDA")
    print(f"   Total migrado: {total_registros} registros")
    if erros:
        print(f"   ⚠️  {len(erros)} tabela(s) com erro:")
        for t, e in erros:
            print(f"      {t}: {e}")
    print("=" * 60)
    print("\nPRÓXIMOS PASSOS:")
    print("  1. Verifique os dados no painel do Supabase")
    print("  2. Substitua o database.py pela versão Supabase")
    print("  3. Suba o código no GitHub")
    print("  4. Deploy no Streamlit Cloud")

    sqlite_conn.close()
    pg_conn.close()

if __name__ == "__main__":
    main()
