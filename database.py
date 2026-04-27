# database.py — PepperCRM v2

import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "peppercrm.db")

TIPOS_PONTO_EXTRA = ["Ponta de gôndola","Ilha","Check-stand","Clip strip","Display"]


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def query(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [tuple(r) for r in rows]


def criar_tabelas():
    conn = conectar(); c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS configuracao (
        config_id INTEGER PRIMARY KEY AUTOINCREMENT,
        modo_operacao TEXT, empresa_nome TEXT,
        data_instalacao TEXT, versao_sistema TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS representante (
        representante_id INTEGER PRIMARY KEY AUTOINCREMENT,
        razao_social TEXT, nome_fantasia TEXT, cnpj TEXT,
        endereco TEXT, bairro TEXT, cidade TEXT, estado TEXT,
        fone TEXT, email TEXT, site TEXT, observacao TEXT, ativo INTEGER DEFAULT 1)""")

    c.execute("""CREATE TABLE IF NOT EXISTS vendedor (
        vendedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        representante_id INTEGER, nome TEXT NOT NULL,
        fone TEXT, email TEXT, cpf TEXT, chave_pix TEXT,
        data_aniversario TEXT, observacao TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (representante_id) REFERENCES representante(representante_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS promotor (
        promotor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, fone TEXT, email TEXT,
        cpf TEXT, cnh TEXT, veiculo TEXT,
        cidade TEXT, estado TEXT, bairro TEXT,
        endereco TEXT, observacao TEXT, ativo INTEGER DEFAULT 1)""")

    c.execute("""CREATE TABLE IF NOT EXISTS att_promotor (
        att_promotor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        promotor_id INTEGER NOT NULL,
        pdv_id      INTEGER NOT NULL,
        dias_visita TEXT,
        frequencia  TEXT DEFAULT 'Semanal',
        hora_inicio TEXT,
        hora_fim    TEXT,
        observacao  TEXT,
        ativo       INTEGER DEFAULT 1,
        FOREIGN KEY (promotor_id) REFERENCES promotor(promotor_id),
        FOREIGN KEY (pdv_id)      REFERENCES pdv(pdv_id),
        UNIQUE (promotor_id, pdv_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS att_vendedor (
        att_vendedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendedor_id INTEGER NOT NULL,
        pdv_id      INTEGER NOT NULL,
        dias_visita TEXT,
        frequencia  TEXT DEFAULT 'Mensal',
        observacao  TEXT,
        ativo       INTEGER DEFAULT 1,
        FOREIGN KEY (vendedor_id) REFERENCES vendedor(vendedor_id),
        FOREIGN KEY (pdv_id)      REFERENCES pdv(pdv_id),
        UNIQUE (vendedor_id, pdv_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS usuario (
        usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, email TEXT UNIQUE, senha_hash TEXT,
        tipo TEXT DEFAULT 'usuario', vendedor_id INTEGER, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (vendedor_id) REFERENCES vendedor(vendedor_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS fornecedor (
        fornecedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        razao_social TEXT, nome_fantasia TEXT NOT NULL,
        endereco TEXT, bairro TEXT, cidade TEXT, estado TEXT,
        cnpj TEXT, ie TEXT, observacao TEXT, ativo INTEGER DEFAULT 1)""")

    c.execute("""CREATE TABLE IF NOT EXISTS contato_fornecedor (
        contato_fornecedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor_id INTEGER NOT NULL, nome_contato TEXT,
        departamento TEXT, fone TEXT, email TEXT, observacao TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS comissao (
        comissao_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor_id INTEGER NOT NULL, percentual REAL NOT NULL DEFAULT 0,
        observacao TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id),
        UNIQUE (fornecedor_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS comissao_pagamento (
        pagamento_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL, data_pagamento TEXT,
        valor_previsto REAL, valor_pago REAL,
        status_pagamento TEXT DEFAULT 'PENDENTE', observacao TEXT,
        FOREIGN KEY (pedido_id) REFERENCES pedido(pedido_id), UNIQUE (pedido_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS marca (
        marca_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor_id INTEGER NOT NULL, nome_marca TEXT NOT NULL, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS categoria (
        categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_categoria TEXT NOT NULL, ativo INTEGER DEFAULT 1)""")

    c.execute("""CREATE TABLE IF NOT EXISTS linha (
        linha_id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria_id INTEGER, nome_linha TEXT NOT NULL, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (categoria_id) REFERENCES categoria(categoria_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS produto (
        produto_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor_id INTEGER, marca_id INTEGER, categoria_id INTEGER, linha_id INTEGER,
        codigo_produto TEXT, descricao TEXT NOT NULL, descricao_curta TEXT,
        peso REAL, unidade_medida TEXT, unidades_caixa INTEGER, caixas_pallet INTEGER,
        ean TEXT, dun TEXT, validade_dias INTEGER, observacao TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id),
        FOREIGN KEY (marca_id)      REFERENCES marca(marca_id),
        FOREIGN KEY (categoria_id)  REFERENCES categoria(categoria_id),
        FOREIGN KEY (linha_id)      REFERENCES linha(linha_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS tabela_preco (
        tabela_preco_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor_id INTEGER NOT NULL, nome_tabela TEXT NOT NULL,
        tipo_tabela TEXT, prazo_pagamento TEXT, frete TEXT,
        data_inicio TEXT, data_fim TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS tabela_preco_item (
        tabela_preco_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tabela_preco_id INTEGER NOT NULL, produto_id INTEGER NOT NULL,
        preco_caixa REAL NOT NULL, desconto_maximo REAL DEFAULT 0,
        FOREIGN KEY (tabela_preco_id) REFERENCES tabela_preco(tabela_preco_id),
        FOREIGN KEY (produto_id)      REFERENCES produto(produto_id),
        UNIQUE (tabela_preco_id, produto_id))""")

    # cliente.status: ativo | inativo | prospecto | visitado
    c.execute("""CREATE TABLE IF NOT EXISTS contato_registro (
        contato_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        data_contato      TEXT NOT NULL,
        via_comunicacao   TEXT NOT NULL,
        tipo_entidade     TEXT NOT NULL DEFAULT 'cliente',
        cliente_id        INTEGER REFERENCES cliente(cliente_id),
        fornecedor_id     INTEGER REFERENCES fornecedor(fornecedor_id),
        contato_pessoa    TEXT,
        assunto           TEXT NOT NULL,
        descricao         TEXT,
        resultado         TEXT,
        proxima_acao      TEXT,
        data_followup     TEXT,
        previsao_conclusao TEXT,
        status            TEXT NOT NULL DEFAULT 'Pendente',
        prioridade        TEXT NOT NULL DEFAULT 'Media',
        usuario_resp      TEXT,
        observacao        TEXT,
        ativo             INTEGER DEFAULT 1)""")

    c.execute("""CREATE TABLE IF NOT EXISTS central_compras (
        central_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        nome_central TEXT NOT NULL,
        tipo_entrega TEXT DEFAULT 'Loja a loja',
        endereco_cd TEXT, bairro_cd TEXT, cidade_cd TEXT, estado_cd TEXT,
        fone TEXT, email TEXT, contato TEXT, observacao TEXT,
        ativo INTEGER DEFAULT 1,
        FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS associacao (
        associacao_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, tipo TEXT, cidade TEXT, estado TEXT,
        fone TEXT, email TEXT, contato TEXT, observacao TEXT,
        ativo INTEGER DEFAULT 1)""")

    c.execute("""CREATE TABLE IF NOT EXISTS cliente (
        cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
        razao_social TEXT, nome_fantasia TEXT NOT NULL,
        endereco TEXT, bairro TEXT, cidade TEXT, estado TEXT,
        cnpj TEXT, ie TEXT, site TEXT, instagram TEXT, fone TEXT,
        perfil TEXT,
        associacao_id INTEGER REFERENCES associacao(associacao_id),
        observacao TEXT, ativo INTEGER DEFAULT 1, status TEXT DEFAULT 'ativo')""")

    c.execute("""CREATE TABLE IF NOT EXISTS contato_cliente (
        contato_cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL, nome_contato TEXT,
        departamento TEXT, fone TEXT, email TEXT, observacao TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS cliente_fornecedor (
        cliente_fornecedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL, fornecedor_id INTEGER NOT NULL,
        tabela_preco_id INTEGER, prazo_pagamento TEXT, codigo_cliente TEXT,
        observacao TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (cliente_id)      REFERENCES cliente(cliente_id),
        FOREIGN KEY (fornecedor_id)   REFERENCES fornecedor(fornecedor_id),
        FOREIGN KEY (tabela_preco_id) REFERENCES tabela_preco(tabela_preco_id),
        UNIQUE (cliente_id, fornecedor_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS produto_codigo_cliente (
        produto_codigo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL, produto_id INTEGER NOT NULL,
        codigo_cliente TEXT,
        FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id),
        FOREIGN KEY (produto_id) REFERENCES produto(produto_id),
        UNIQUE (cliente_id, produto_id))""")

    # pdv.status: ativo | inativo | prospecto | visitado  —  estado default SP
    c.execute("""CREATE TABLE IF NOT EXISTS pdv (
        pdv_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL, numero_loja TEXT, nome_loja TEXT NOT NULL,
        endereco TEXT, bairro TEXT, cidade TEXT, estado TEXT DEFAULT 'SP',
        cnpj TEXT, ie TEXT, gerente TEXT, fone_gerente TEXT,
        encarregado TEXT, fone_encarregado TEXT, horario_recebimento TEXT,
        observacao TEXT, ativo INTEGER DEFAULT 1, status TEXT DEFAULT 'ativo',
        FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS mix_cliente (
        mix_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL, fornecedor_id INTEGER NOT NULL,
        pdv_id INTEGER, produto_id INTEGER NOT NULL,
        ativo INTEGER DEFAULT 1, observacao TEXT,
        FOREIGN KEY (cliente_id)    REFERENCES cliente(cliente_id),
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id),
        FOREIGN KEY (pdv_id)        REFERENCES pdv(pdv_id),
        FOREIGN KEY (produto_id)    REFERENCES produto(produto_id),
        UNIQUE (cliente_id, fornecedor_id, pdv_id, produto_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS pedido (
        pedido_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nr_pedido_fornecedor TEXT, nr_pedido_cliente TEXT,
        cliente_id INTEGER NOT NULL, pdv_id INTEGER,
        fornecedor_id INTEGER NOT NULL, vendedor_id INTEGER,
        tabela_preco_id INTEGER, prazo_pagamento TEXT, frete TEXT,
        data_pedido TEXT, data_entrega TEXT,
        desconto_geral REAL DEFAULT 0, observacao TEXT,
        status_pedido TEXT DEFAULT 'ABERTO', comissao_percentual REAL,
        FOREIGN KEY (cliente_id)      REFERENCES cliente(cliente_id),
        FOREIGN KEY (pdv_id)          REFERENCES pdv(pdv_id),
        FOREIGN KEY (fornecedor_id)   REFERENCES fornecedor(fornecedor_id),
        FOREIGN KEY (vendedor_id)     REFERENCES vendedor(vendedor_id),
        FOREIGN KEY (tabela_preco_id) REFERENCES tabela_preco(tabela_preco_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS pedido_item (
        pedido_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL, produto_id INTEGER NOT NULL,
        preco_tabela REAL, desconto REAL DEFAULT 0, preco_final REAL,
        quantidade INTEGER NOT NULL, status_item TEXT DEFAULT 'NORMAL',
        FOREIGN KEY (pedido_id)  REFERENCES pedido(pedido_id),
        FOREIGN KEY (produto_id) REFERENCES produto(produto_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS pedido_historico (
        historico_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL, data_hora TEXT NOT NULL,
        campo TEXT NOT NULL, valor_antes TEXT, valor_depois TEXT, observacao TEXT,
        FOREIGN KEY (pedido_id) REFERENCES pedido(pedido_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS visita_cliente (
        visita_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL, pdv_id INTEGER, local TEXT,
        data_visita TEXT NOT NULL, contato TEXT, resumo TEXT,
        produtos_tratados TEXT, pedido_id INTEGER,
        proxima_acao TEXT, data_followup TEXT, observacao TEXT,
        FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id),
        FOREIGN KEY (pdv_id)     REFERENCES pdv(pdv_id),
        FOREIGN KEY (pedido_id)  REFERENCES pedido(pedido_id))""")

    # concorrente — fornecedor_id OBRIGATÓRIO (NOT NULL)
    c.execute("""CREATE TABLE IF NOT EXISTS concorrente (
        concorrente_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor_id     INTEGER NOT NULL,
        marca_concorrente TEXT NOT NULL,
        origem_cidade     TEXT, observacao TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS produto_concorrente (
        produto_concorrente_id INTEGER PRIMARY KEY AUTOINCREMENT,
        concorrente_id  INTEGER NOT NULL,
        categoria_id    INTEGER, linha_id INTEGER,
        descricao       TEXT NOT NULL, descricao_curta TEXT,
        peso REAL, unidade_medida TEXT, ean TEXT, validade_dias INTEGER,
        observacao TEXT, ativo INTEGER DEFAULT 1,
        FOREIGN KEY (concorrente_id) REFERENCES concorrente(concorrente_id),
        FOREIGN KEY (categoria_id)   REFERENCES categoria(categoria_id),
        FOREIGN KEY (linha_id)       REFERENCES linha(linha_id))""")

    # Relação produto meu <-> produto concorrente
    c.execute("""CREATE TABLE IF NOT EXISTS produto_concorrente_relacao (
        relacao_id             INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id             INTEGER NOT NULL,
        produto_concorrente_id INTEGER NOT NULL,
        tipo_relacao           TEXT DEFAULT 'direto',
        observacao             TEXT,
        FOREIGN KEY (produto_id)             REFERENCES produto(produto_id),
        FOREIGN KEY (produto_concorrente_id) REFERENCES produto_concorrente(produto_concorrente_id),
        UNIQUE (produto_id, produto_concorrente_id))""")

    # pesquisa_preco — status: rascunho | finalizado
    c.execute("""CREATE TABLE IF NOT EXISTS pesquisa_preco (
        pesquisa_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        data_pesquisa  TEXT NOT NULL,
        pdv_id         INTEGER,
        cliente_id     INTEGER,
        fornecedor_id  INTEGER NOT NULL,
        observacao     TEXT,
        status         TEXT DEFAULT 'rascunho',
        FOREIGN KEY (pdv_id)        REFERENCES pdv(pdv_id),
        FOREIGN KEY (cliente_id)    REFERENCES cliente(cliente_id),
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id))""")

    # pesquisa_preco_item — um registro por produto/concorrente pesquisado
    c.execute("""CREATE TABLE IF NOT EXISTS pesquisa_preco_item (
        pesquisa_item_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        pesquisa_id            INTEGER NOT NULL,
        produto_id             INTEGER,
        produto_concorrente_id INTEGER,
        preco                  REAL,
        em_oferta              INTEGER DEFAULT 0,
        frentes                INTEGER,
        ruptura                INTEGER DEFAULT 0,
        ponto_extra            INTEGER DEFAULT 0,
        tipo_ponto_extra       TEXT,
        observacao             TEXT,
        FOREIGN KEY (pesquisa_id)            REFERENCES pesquisa_preco(pesquisa_id),
        FOREIGN KEY (produto_id)             REFERENCES produto(produto_id),
        FOREIGN KEY (produto_concorrente_id) REFERENCES produto_concorrente(produto_concorrente_id))""")

    conn.commit(); conn.close()
    _migrar_todos()
    print("✅ Tabelas OK.")


def _migrar_todos():
    conn = sqlite3.connect(DB_PATH)

    def cols(t):
        try: return [r[1] for r in conn.execute(f"PRAGMA table_info({t})").fetchall()]
        except: return []

    def tabs():
        return [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

    T = tabs()

    def add_col(table, col, tipo):
        if table in T and col not in cols(table):
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {tipo}")
            conn.commit()

    # Migrações acumuladas
    add_col("mix_cliente",      "pdv_id",              "INTEGER REFERENCES pdv(pdv_id)")
    add_col("pedido",           "comissao_percentual",  "REAL")
    add_col("cliente",          "status",               "TEXT DEFAULT 'ativo'")
    add_col("pdv",              "status",               "TEXT DEFAULT 'ativo'")
    add_col("pdv",              "estado",               "TEXT DEFAULT 'SP'")
    add_col("visita_cliente",   "produtos_tratados",    "TEXT")
    add_col("visita_cliente",   "pedido_id",            "INTEGER REFERENCES pedido(pedido_id)")
    add_col("visita_cliente",   "proxima_acao",         "TEXT")
    add_col("visita_cliente",   "data_followup",        "TEXT")
    add_col("visita_cliente",   "pesquisa_preco_id",    "INTEGER REFERENCES pesquisa_preco(pesquisa_id)")
    add_col("visita_cliente",   "latitude",             "REAL")
    add_col("visita_cliente",   "longitude",            "REAL")
    add_col("visita_cliente",   "endereco_gps",         "TEXT")
    add_col("visita_cliente",   "duracao_minutos",      "INTEGER")
    add_col("pdv",              "tipo_pdv",             "TEXT")
    add_col("pedido",           "data_entrega_realizada","TEXT")
    add_col("pdv",              "dia_visita",            "TEXT")
    add_col("pdv",              "frequencia_visita",     "TEXT")
    add_col("pdv",              "ordem_roteiro",         "INTEGER")
    add_col("pdv",              "setor",                 "TEXT")
    add_col("pdv",              "cluster",               "TEXT")
    add_col("produto",          "sub_categoria",         "TEXT")
    add_col("produto",          "grupo",                 "TEXT")
    add_col("produto",          "peso_caixa",            "REAL")
    add_col("produto",          "shelf_life_resfriado",  "INTEGER")
    add_col("produto",          "shelf_life_congelado",  "INTEGER")
    add_col("produto",          "ncm",                   "TEXT")
    add_col("produto",          "cest",                  "TEXT")
    add_col("contato_cliente",  "whatsapp",              "TEXT")
    add_col("tabela_preco_item", "preco_kg",              "REAL")
    if "contato_x_fornecedor" not in T:
        conn.execute("""CREATE TABLE contato_x_fornecedor (
            cxf_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            contato_id    INTEGER NOT NULL REFERENCES contato_registro(contato_id),
            fornecedor_id INTEGER NOT NULL REFERENCES fornecedor(fornecedor_id),
            UNIQUE(contato_id, fornecedor_id))""")
        conn.commit()
    if "contato_registro" not in T:
        conn.execute("""CREATE TABLE contato_registro (
            contato_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            data_contato      TEXT NOT NULL,
            via_comunicacao   TEXT NOT NULL,
            tipo_entidade     TEXT NOT NULL DEFAULT 'cliente',
            cliente_id        INTEGER REFERENCES cliente(cliente_id),
            fornecedor_id     INTEGER REFERENCES fornecedor(fornecedor_id),
            contato_pessoa    TEXT,
            assunto           TEXT NOT NULL,
            descricao         TEXT,
            resultado         TEXT,
            proxima_acao      TEXT,
            data_followup     TEXT,
            previsao_conclusao TEXT,
            status            TEXT NOT NULL DEFAULT 'Pendente',
            prioridade        TEXT NOT NULL DEFAULT 'Media',
            usuario_resp      TEXT,
            observacao        TEXT,
            ativo             INTEGER DEFAULT 1)""")
        conn.commit()
    add_col("tabela_preco_item", "observacao",            "TEXT")
    add_col("pdv",              "tamanho_pdv",           "TEXT")
    # Novas tabelas de atendimento
    for _tbl, _sql in [
        ("promotor", """CREATE TABLE promotor (
            promotor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, fone TEXT, email TEXT,
            cpf TEXT, cnh TEXT, veiculo TEXT,
            cidade TEXT, estado TEXT, bairro TEXT,
            endereco TEXT, observacao TEXT, ativo INTEGER DEFAULT 1)"""),
        ("att_promotor", """CREATE TABLE att_promotor (
            att_promotor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            promotor_id INTEGER NOT NULL, pdv_id INTEGER NOT NULL,
            dias_visita TEXT, frequencia TEXT DEFAULT 'Semanal',
            hora_inicio TEXT, hora_fim TEXT, observacao TEXT, ativo INTEGER DEFAULT 1,
            FOREIGN KEY (promotor_id) REFERENCES promotor(promotor_id),
            FOREIGN KEY (pdv_id)      REFERENCES pdv(pdv_id),
            UNIQUE (promotor_id, pdv_id))"""),
        ("att_vendedor", """CREATE TABLE att_vendedor (
            att_vendedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendedor_id INTEGER NOT NULL, pdv_id INTEGER NOT NULL,
            dias_visita TEXT, frequencia TEXT DEFAULT 'Mensal',
            observacao TEXT, ativo INTEGER DEFAULT 1,
            FOREIGN KEY (vendedor_id) REFERENCES vendedor(vendedor_id),
            FOREIGN KEY (pdv_id)      REFERENCES pdv(pdv_id),
            UNIQUE (vendedor_id, pdv_id))"""),
    ]:
        if _tbl not in T:
            conn.execute(_sql)
    add_col("pdv",              "latitude",              "REAL")
    add_col("pdv",              "longitude",             "REAL")
    add_col("cliente",          "fone",                  "TEXT")
    if "central_compras" not in T:
        conn.execute("""CREATE TABLE central_compras (
            central_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            nome_central TEXT NOT NULL,
            tipo_entrega TEXT DEFAULT 'Loja a loja',
            endereco_cd TEXT, bairro_cd TEXT, cidade_cd TEXT, estado_cd TEXT,
            fone TEXT, email TEXT, contato TEXT, observacao TEXT,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id))""")
        conn.commit()
    add_col("cliente",          "perfil",                "TEXT")
    add_col("cliente",          "associacao_id",         "INTEGER REFERENCES associacao(associacao_id)")
    add_col("configuracao",     "anthropic_api_key",     "TEXT")
    add_col("representante",    "whatsapp",              "TEXT")
    add_col("produto_concorrente", "auditavel",          "INTEGER DEFAULT 1")
    add_col("concorrente",         "importada",          "INTEGER DEFAULT 0")
    add_col("concorrente",         "importado_por",      "TEXT")
    add_col("produto_concorrente", "ean_concorrente",    "TEXT")
    add_col("tabela_preco_item","preco_kg",              "REAL")
    add_col("tabela_preco_item","observacao",            "TEXT")
    if "historico_preco" not in T:
        conn.execute("""CREATE TABLE historico_preco (
            hist_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id     INTEGER NOT NULL REFERENCES produto(produto_id),
            fornecedor_id  INTEGER NOT NULL REFERENCES fornecedor(fornecedor_id),
            tabela_id      INTEGER REFERENCES tabela_preco(tabela_preco_id),
            nome_tabela    TEXT,
            data_vigencia  TEXT NOT NULL,
            preco_caixa    REAL NOT NULL,
            preco_kg       REAL,
            data_registro  TEXT NOT NULL)""")
        conn.commit()
        # Migra preços já existentes para o histórico
        conn.execute("""INSERT INTO historico_preco
            (produto_id, fornecedor_id, tabela_id, nome_tabela,
             data_vigencia, preco_caixa, preco_kg, data_registro)
            SELECT tpi.produto_id, tp.fornecedor_id, tp.tabela_preco_id,
                   tp.nome_tabela,
                   COALESCE(tp.data_inicio, date('now')),
                   tpi.preco_caixa,
                   tpi.preco_kg,
                   COALESCE(tp.data_inicio, date('now'))
            FROM tabela_preco_item tpi
            JOIN tabela_preco tp ON tpi.tabela_preco_id = tp.tabela_preco_id""")
        conn.commit()
    add_col("vendedor",         "whatsapp",              "TEXT")
    add_col("configuracao",     "senha_exclusao",        "TEXT")
    add_col("pesquisa_preco",   "foto_path",             "TEXT")
    add_col("pesquisa_preco_item", "foto_path",          "TEXT")
    add_col("contato_registro", "tipo_topico", "TEXT")
    if "contato_interacao" not in T:
        conn.execute("""CREATE TABLE contato_interacao (
            interacao_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            contato_id         INTEGER NOT NULL REFERENCES contato_registro(contato_id),
            data_interacao     TEXT NOT NULL,
            via_comunicacao    TEXT NOT NULL,
            contato_pessoa     TEXT,
            contato_cliente_id INTEGER REFERENCES contato_cliente(contato_cliente_id),
            descricao          TEXT,
            resultado          TEXT,
            data_followup      TEXT,
            ativo              INTEGER DEFAULT 1)""")
        conn.commit()
        # Migra interações existentes dos campos de contato_registro
        conn.execute("""INSERT INTO contato_interacao
            (contato_id, data_interacao, via_comunicacao,
             contato_pessoa, descricao, resultado, data_followup, ativo)
            SELECT contato_id, data_contato, via_comunicacao,
                   contato_pessoa, descricao, resultado, data_followup, ativo
            FROM contato_registro WHERE ativo=1""")
        conn.commit()
    if "negociacao" not in T:
        conn.execute("""CREATE TABLE negociacao (
            negociacao_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id         INTEGER REFERENCES cliente(cliente_id),
            fornecedor_id      INTEGER REFERENCES fornecedor(fornecedor_id),
            titulo             TEXT NOT NULL,
            data_abertura      TEXT NOT NULL,
            status             TEXT NOT NULL DEFAULT 'Aberta',
            prioridade         TEXT NOT NULL DEFAULT 'Media',
            previsao_conclusao TEXT,
            observacao         TEXT,
            ativo              INTEGER DEFAULT 1)""")
        conn.commit()
    if "interacao" not in T:
        conn.execute("""CREATE TABLE interacao (
            interacao_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            negociacao_id      INTEGER NOT NULL REFERENCES negociacao(negociacao_id),
            data_interacao     TEXT NOT NULL,
            via_comunicacao    TEXT NOT NULL,
            contato_pessoa     TEXT,
            contato_cliente_id INTEGER REFERENCES contato_cliente(contato_cliente_id),
            descricao          TEXT,
            resultado          TEXT,
            data_followup      TEXT,
            status_interacao   TEXT NOT NULL DEFAULT 'Realizado',
            ativo              INTEGER DEFAULT 1)""")
        conn.commit()
    if "pesquisa_foto" not in T:
        conn.execute("""CREATE TABLE pesquisa_foto (
            foto_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            pesquisa_id   INTEGER NOT NULL REFERENCES pesquisa_preco(pesquisa_id),
            foto_path     TEXT NOT NULL,
            legenda       TEXT,
            data_upload   TEXT,
            ativo         INTEGER DEFAULT 1)""")
        conn.commit()
    # Cria tabela associacao se nao existir (para bancos antigos)
    if "associacao" not in T:
        conn.execute("""CREATE TABLE associacao (
            associacao_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, tipo TEXT, cidade TEXT, estado TEXT,
            fone TEXT, email TEXT, contato TEXT, observacao TEXT,
            ativo INTEGER DEFAULT 1)""")
    add_col("pesquisa_preco",   "cliente_id",           "INTEGER REFERENCES cliente(cliente_id)")
    add_col("pesquisa_preco",   "status",               "TEXT DEFAULT 'rascunho'")
    add_col("pesquisa_preco_item", "preco",             "REAL")

    # Migra dados gravados com colunas antigas (preco_proprio / preco_concorrente) -> preco
    conn2 = sqlite3.connect(DB_PATH)
    cols_pi = [r[1] for r in conn2.execute("PRAGMA table_info(pesquisa_preco_item)").fetchall()]
    if "preco_proprio" in cols_pi:
        # Copia preco_proprio -> preco onde preco ainda é NULL e produto_concorrente_id é NULL
        conn2.execute("""
            UPDATE pesquisa_preco_item SET preco = preco_proprio
            WHERE preco IS NULL AND produto_concorrente_id IS NULL
              AND preco_proprio IS NOT NULL
        """)
        conn2.commit()
    if "preco_concorrente" in cols_pi:
        # Copia preco_concorrente -> preco onde preco ainda é NULL e produto_concorrente_id não é NULL
        conn2.execute("""
            UPDATE pesquisa_preco_item SET preco = preco_concorrente
            WHERE preco IS NULL AND produto_concorrente_id IS NOT NULL
              AND preco_concorrente IS NOT NULL
        """)
        conn2.commit()
    conn2.close()
    add_col("pesquisa_preco_item", "frentes",           "INTEGER")
    add_col("pesquisa_preco_item", "ruptura",           "INTEGER DEFAULT 0")
    add_col("pesquisa_preco_item", "ponto_extra",       "INTEGER DEFAULT 0")
    add_col("pesquisa_preco_item", "tipo_ponto_extra",  "TEXT")

    # pedido_historico
    if "pedido_historico" not in T:
        conn.execute("""CREATE TABLE pedido_historico (
            historico_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL, data_hora TEXT NOT NULL,
            campo TEXT NOT NULL, valor_antes TEXT, valor_depois TEXT, observacao TEXT,
            FOREIGN KEY (pedido_id) REFERENCES pedido(pedido_id))""")
        conn.commit()

    # comissao
    if "comissao" not in T:
        conn.execute("""CREATE TABLE comissao (
            comissao_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fornecedor_id INTEGER NOT NULL, percentual REAL NOT NULL DEFAULT 0,
            observacao TEXT, ativo INTEGER DEFAULT 1,
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(fornecedor_id),
            UNIQUE (fornecedor_id))""")
        conn.commit()

    # comissao_pagamento
    if "comissao_pagamento" not in T:
        conn.execute("""CREATE TABLE comissao_pagamento (
            pagamento_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL, data_pagamento TEXT,
            valor_previsto REAL, valor_pago REAL,
            status_pagamento TEXT DEFAULT 'PENDENTE', observacao TEXT,
            FOREIGN KEY (pedido_id) REFERENCES pedido(pedido_id), UNIQUE (pedido_id))""")
        conn.commit()

    # produto_concorrente_relacao
    if "produto_concorrente_relacao" not in T:
        conn.execute("""CREATE TABLE produto_concorrente_relacao (
            relacao_id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL, produto_concorrente_id INTEGER NOT NULL,
            tipo_relacao TEXT DEFAULT 'direto', observacao TEXT,
            FOREIGN KEY (produto_id)             REFERENCES produto(produto_id),
            FOREIGN KEY (produto_concorrente_id) REFERENCES produto_concorrente(produto_concorrente_id),
            UNIQUE (produto_id, produto_concorrente_id))""")
        conn.commit()

    # Corrige concorrente sem fornecedor_id (bancos antigos com coluna nullable)
    # Apenas garante que novos registros tenham fornecedor
    conn.close()


# ── Helpers públicos ──────────────────────────────────

def registrar_historico(conn, pedido_id, campo, valor_antes, valor_depois, obs=None):
    from datetime import datetime
    conn.execute("""INSERT INTO pedido_historico
        (pedido_id,data_hora,campo,valor_antes,valor_depois,observacao)
        VALUES(?,?,?,?,?,?)""",
        (pedido_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), campo,
         str(valor_antes) if valor_antes is not None else None,
         str(valor_depois) if valor_depois is not None else None, obs))


def get_percentual_comissao(fornecedor_id: int) -> float:
    r = query("SELECT percentual FROM comissao WHERE fornecedor_id=? AND ativo=1", (fornecedor_id,))
    return float(r[0][0]) if r else 0.0


def get_fornecedores_do_cliente(cliente_id: int):
    return query("""
        SELECT cf.cliente_fornecedor_id, f.fornecedor_id, f.nome_fantasia,
               tp.tabela_preco_id, tp.nome_tabela, tp.tipo_tabela,
               COALESCE(cf.prazo_pagamento, tp.prazo_pagamento), tp.frete, cf.codigo_cliente
        FROM cliente_fornecedor cf
        JOIN fornecedor f ON cf.fornecedor_id=f.fornecedor_id
        LEFT JOIN tabela_preco tp ON cf.tabela_preco_id=tp.tabela_preco_id
        WHERE cf.cliente_id=? AND cf.ativo=1 AND f.ativo=1""", (cliente_id,))


def get_mix_com_preco(cliente_id: int, fornecedor_id: int, pdv_id=None):
    if pdv_id:
        where = "mc.cliente_id=? AND mc.fornecedor_id=? AND mc.pdv_id=? AND mc.ativo=1"
        p = (cliente_id, fornecedor_id, pdv_id)
    else:
        where = "mc.cliente_id=? AND mc.fornecedor_id=? AND mc.pdv_id IS NULL AND mc.ativo=1"
        p = (cliente_id, fornecedor_id)
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(f"""
        SELECT p.produto_id, p.codigo_produto, p.descricao, p.descricao_curta,
               p.unidades_caixa, p.unidade_medida, tpi.preco_caixa, tpi.desconto_maximo,
               pcc.codigo_cliente,
               (SELECT pi2.quantidade FROM pedido_item pi2
                JOIN pedido ped2 ON pi2.pedido_id=ped2.pedido_id
                WHERE pi2.produto_id=p.produto_id
                  AND ped2.cliente_id={cliente_id} AND ped2.fornecedor_id={fornecedor_id}
                ORDER BY ped2.data_pedido DESC LIMIT 1),
               (SELECT ped2.data_pedido FROM pedido_item pi2
                JOIN pedido ped2 ON pi2.pedido_id=ped2.pedido_id
                WHERE pi2.produto_id=p.produto_id
                  AND ped2.cliente_id={cliente_id} AND ped2.fornecedor_id={fornecedor_id}
                ORDER BY ped2.data_pedido DESC LIMIT 1)
        FROM mix_cliente mc
        JOIN produto p ON mc.produto_id=p.produto_id
        LEFT JOIN cliente_fornecedor cf ON cf.cliente_id=mc.cliente_id AND cf.fornecedor_id=mc.fornecedor_id
        LEFT JOIN tabela_preco_item tpi ON tpi.tabela_preco_id=cf.tabela_preco_id AND tpi.produto_id=p.produto_id
        LEFT JOIN produto_codigo_cliente pcc ON pcc.cliente_id=mc.cliente_id AND pcc.produto_id=p.produto_id
        WHERE {where} AND p.ativo=1 ORDER BY p.descricao_curta""", p).fetchall()
    conn.close()
    return [tuple(r) for r in rows]


def get_clientes_ativos():
    return query("SELECT cliente_id, nome_fantasia, cidade, estado FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")


def get_produtos_por_fornecedor(fornecedor_id: int):
    return query("""SELECT produto_id, codigo_produto, descricao, descricao_curta,
        unidades_caixa, unidade_medida FROM produto WHERE fornecedor_id=? AND ativo=1 ORDER BY descricao""",
        (fornecedor_id,))


if __name__ == "__main__":
    criar_tabelas()