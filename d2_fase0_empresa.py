# d2_fase0_empresa.py
# Fase 0 do D2 Multi-tenant: criar tabela empresa
# Execucao: unica vez, local e Railway
# Risco: ZERO — nao altera nenhuma tabela existente

from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== FASE 0 - Criar tabela empresa ===\n")

    print("1. Criando tabela empresa...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS empresa (
            empresa_id       SERIAL PRIMARY KEY,
            nome             TEXT NOT NULL,
            cnpj             TEXT,
            email_admin      TEXT NOT NULL,
            plano            TEXT DEFAULT 'solo',
            status           TEXT DEFAULT 'ativo',
            data_criacao     DATE DEFAULT CURRENT_DATE,
            data_vencimento  DATE,
            max_usuarios     INTEGER DEFAULT 3,
            max_clientes     INTEGER DEFAULT 500,
            ativo            INTEGER DEFAULT 1
        )
    """)
    print("   OK - Tabela empresa criada (ou ja existia)")

    cur.execute("SELECT COUNT(*) FROM empresa")
    total = cur.fetchone()[0]

    if total == 0:
        print("\n2. Inserindo empresa atual (Azevedo e Filhos)...")
        cur.execute("""
            INSERT INTO empresa
                (empresa_id, nome, cnpj, email_admin, plano, status,
                 max_usuarios, max_clientes, ativo)
            VALUES
                (1, 'Azevedo e Filhos Representacao Comercial',
                 NULL, 'fernandojr@azevedoefilhos.com.br',
                 'escritorio', 'ativo', 15, 9999, 1)
        """)
        print("   OK - Empresa registrada com empresa_id=1")
    else:
        print(f"\n2. Empresa ja cadastrada ({total} registro(s)) - pulando insercao")

    cur.execute("SELECT setval('empresa_empresa_id_seq', GREATEST(1, (SELECT MAX(empresa_id) FROM empresa)))")
    print("   OK - Sequence ajustada")

    conn.commit()

    print("\n=== Resultado ===")
    cur.execute("SELECT empresa_id, nome, plano, status, max_usuarios, max_clientes FROM empresa")
    for r in cur.fetchall():
        print(f"  empresa_id : {r[0]}")
        print(f"  nome       : {r[1]}")
        print(f"  plano      : {r[2]}")
        print(f"  status     : {r[3]}")
        print(f"  max_usuarios: {r[4]}")
        print(f"  max_clientes: {r[5]}")

    print("\nFASE 0 concluida com sucesso!")
    print("Proximo passo: d2_faseA.py")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    raise
finally:
    cur.close()
    conn.close()
