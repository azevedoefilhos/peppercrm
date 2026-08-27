from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import _pg_connect, execute_write

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== Etapa 1: Banco de dados para Roteiros ===\n")

    # ─── 1. Tabela setor ───────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS setor (
            setor_id    SERIAL PRIMARY KEY,
            codigo      TEXT NOT NULL,
            nome        TEXT NOT NULL,
            cidade      TEXT,
            empresa_id  INTEGER NOT NULL DEFAULT 1,
            ativo       BOOLEAN NOT NULL DEFAULT TRUE,
            criado_em   TIMESTAMP DEFAULT NOW()
        )
    """)
    print("OK: tabela setor criada")

    # Pré-popula setores da Baixada Santista (empresa_id=1)
    setores = [
        ('S1',  'Setor 1 - Santos Centro / Porto',          'Santos'),
        ('S2',  'Setor 2 - Santos Intermediário',           'Santos'),
        ('S3A', 'Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)', 'Santos'),
        ('S3B', 'Setor 3B - Santos Orla Sul (Gonzaga / José Menino)',   'Santos'),
        ('S4',  'Setor 4 - Ponta da Praia',                 'Santos'),
        ('S5',  'Setor 5 - São Vicente',                    'São Vicente'),
        ('S6',  'Setor 6 - Guarujá',                        'Guarujá'),
        ('S7A', 'Setor 7A - Praia Grande Orla / Norte',     'Praia Grande'),
        ('S7B', 'Setor 7B - Praia Grande Interior / Sul',   'Praia Grande'),
        ('S8',  'Setor 8 - Litoral Sul',                    'Itanhaém'),
    ]
    for cod, nome, cidade in setores:
        cur.execute("""
            INSERT INTO setor (codigo, nome, cidade, empresa_id)
            SELECT %s, %s, %s, 1
            WHERE NOT EXISTS (
                SELECT 1 FROM setor WHERE codigo=%s AND empresa_id=1
            )
        """, (cod, nome, cidade, cod))
    print(f"OK: {len(setores)} setores pré-populados")

    # ─── 2. Colunas em pdv ─────────────────────────────────────────────
    colunas_pdv = [
        ("setor_id",        "INTEGER REFERENCES setor(setor_id)"),
        ("turno_visita",    "TEXT CHECK(turno_visita IN ('Manhã','Tarde','Ambos'))"),
        ("aceita_promotor", "BOOLEAN DEFAULT TRUE"),
    ]
    for col, tipo in colunas_pdv:
        cur.execute(f"""
            SELECT COUNT(*) FROM information_schema.columns
            WHERE table_name='pdv' AND column_name='{col}'
        """)
        if cur.fetchone()[0] == 0:
            cur.execute(f"ALTER TABLE pdv ADD COLUMN {col} {tipo}")
            print(f"OK: pdv.{col} adicionado")
        else:
            print(f"-- pdv.{col} ja existe")

    # ─── 3. Migra setor texto → setor_id ──────────────────────────────
    cur.execute("""
        UPDATE pdv p SET setor_id = s.setor_id
        FROM setor s
        WHERE p.setor = s.nome
          AND p.setor_id IS NULL
          AND p.setor IS NOT NULL
    """)
    print(f"OK: {cur.rowcount} PDVs migrados para setor_id")

    # ─── 4. aceita_promotor = FALSE para tipos sem promotor ───────────
    tipos_sem_promotor = (
        'Hamburgueria','Bar / Boteco','Restaurante','Lanchonete',
        'Clube / Associacao','Acougue','Casa de Carnes','Peixaria'
    )
    ph = ','.join(['%s']*len(tipos_sem_promotor))
    cur.execute(f"""
        UPDATE pdv SET aceita_promotor = FALSE
        WHERE tipo_pdv IN ({ph})
          AND aceita_promotor IS TRUE
    """, tipos_sem_promotor)
    print(f"OK: {cur.rowcount} PDVs marcados aceita_promotor=FALSE")

    # ─── 5. Tabela roteiro_item ────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roteiro_item (
            roteiro_item_id SERIAL PRIMARY KEY,
            tipo_roteiro    TEXT NOT NULL CHECK(tipo_roteiro IN ('vendedor','promotor')),
            usuario_id      INTEGER NOT NULL REFERENCES usuario(usuario_id),
            pdv_id          INTEGER NOT NULL REFERENCES pdv(pdv_id),
            dia_semana      INTEGER NOT NULL CHECK(dia_semana BETWEEN 1 AND 5),
            turno           TEXT NOT NULL DEFAULT 'Manhã'
                            CHECK(turno IN ('Manhã','Tarde')),
            ordem_rota      INTEGER NOT NULL DEFAULT 1,
            frequencia      TEXT NOT NULL DEFAULT 'semanal'
                            CHECK(frequencia IN (
                                'semanal','quinzenal_1_3','quinzenal_2_4','mensal'
                            )),
            ativo           BOOLEAN NOT NULL DEFAULT TRUE,
            empresa_id      INTEGER NOT NULL DEFAULT 1,
            criado_por      INTEGER REFERENCES usuario(usuario_id),
            criado_em       TIMESTAMP DEFAULT NOW(),
            UNIQUE(tipo_roteiro, usuario_id, pdv_id, dia_semana, turno)
        )
    """)
    print("OK: tabela roteiro_item criada")

    # ─── 6. Tabela roteiro_substituicao (trocas pontuais) ─────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roteiro_substituicao (
            sub_id              SERIAL PRIMARY KEY,
            roteiro_item_id     INTEGER REFERENCES roteiro_item(roteiro_item_id),
            data_substituicao   DATE NOT NULL,
            pdv_substituto_id   INTEGER REFERENCES pdv(pdv_id),
            motivo              TEXT,
            criado_por          INTEGER REFERENCES usuario(usuario_id),
            criado_em           TIMESTAMP DEFAULT NOW()
        )
    """)
    print("OK: tabela roteiro_substituicao criada")

    # ─── 7. Flag pode_editar_roteiro_promotor em vendedor ─────────────
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='vendedor' AND column_name='pode_editar_roteiro_promotor'
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("""
            ALTER TABLE vendedor
            ADD COLUMN pode_editar_roteiro_promotor BOOLEAN DEFAULT FALSE
        """)
        print("OK: vendedor.pode_editar_roteiro_promotor adicionado")
    else:
        print("-- vendedor.pode_editar_roteiro_promotor ja existe")

    # ─── 8. Ponto de partida do usuario (para otimizacao de rota) ─────
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='usuario'
        AND column_name='lat_base'
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("""
            ALTER TABLE usuario
            ADD COLUMN lat_base  NUMERIC(10,6),
            ADD COLUMN lng_base  NUMERIC(10,6),
            ADD COLUMN end_base  TEXT
        """)
        print("OK: usuario lat_base/lng_base/end_base adicionados")
    else:
        print("-- usuario lat_base ja existe")

    conn.commit()
    print("\n✅ Etapa 1 concluída com sucesso!")

    # Resumo
    cur.execute("SELECT COUNT(*) FROM setor WHERE empresa_id=1")
    print(f"\nSetores cadastrados: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM pdv WHERE setor_id IS NOT NULL")
    print(f"PDVs com setor vinculado: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM pdv WHERE aceita_promotor=FALSE")
    print(f"PDVs sem promotor: {cur.fetchone()[0]}")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    import traceback; traceback.print_exc()
finally:
    cur.close()
    conn.close()
