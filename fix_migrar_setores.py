from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import _pg_connect, query

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    # Ver mapeamento atual setor texto -> setor_id
    cur.execute("""SELECT DISTINCT p.setor, p.setor_id, s.nome, COUNT(p.pdv_id)
        FROM pdv p LEFT JOIN setor s ON s.setor_id=p.setor_id
        WHERE p.setor IS NOT NULL
        GROUP BY p.setor, p.setor_id, s.nome
        ORDER BY p.setor""")
    print("=== Mapeamento atual ===")
    for r in cur.fetchall():
        print(f"  setor='{r[0]}' -> setor_id={r[1]} ({r[2]}) — {r[3]} PDVs")

    # Mapeamento correto setor texto -> codigo do setor
    mapa = {
        'Setor 1 - Santos Centro / Porto':           'S1',
        'Setor 2 - Santos Intermediário':            'S2',
        'Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)': 'S3A',
        'Setor 3B - Santos Orla Sul (Gonzaga / José Menino)':   'S3B',
        'Setor 3 - Santos Orla':                     'S3B',  # legado -> S3B
        'Setor 4 - Ponta da Praia':                  'S4',
        'Setor 5 - São Vicente':                     'S5',
        'Setor 6 - Guarujá':                         'S6',
        'Setor 7A - Praia Grande Orla / Norte':      'S7A',
        'Setor 7B - Praia Grande Interior / Sul':    'S7B',
        'Setor 7 - Praia Grande':                    'S7A',  # legado -> S7A
        'Setor 8 - Litoral Sul':                     'S8',
    }

    # Busca IDs dos setores
    cur.execute("SELECT codigo, setor_id FROM setor WHERE empresa_id=1")
    codigo_to_id = {r[0]: r[1] for r in cur.fetchall()}
    print(f"\nCodigos disponiveis: {codigo_to_id}")

    # Corrige setor_id para cada PDV
    print("\n=== Corrigindo setor_id ===")
    total = 0
    for texto_setor, codigo in mapa.items():
        sid = codigo_to_id.get(codigo)
        if not sid:
            print(f"  AVISO: codigo {codigo} nao encontrado")
            continue
        cur.execute("""UPDATE pdv SET setor_id=%s
            WHERE setor=%s AND (setor_id IS NULL OR setor_id!=%s)""",
            (sid, texto_setor, sid))
        n = cur.rowcount
        if n > 0:
            print(f"  '{texto_setor}' -> {codigo} (id={sid}): {n} PDVs")
            total += n

    print(f"\nTotal corrigido: {total} PDVs")
    conn.commit()

    # Verifica resultado
    print("\n=== Resultado final ===")
    cur.execute("""SELECT s.nome, COUNT(p.pdv_id)
        FROM setor s
        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0
        WHERE s.empresa_id=1
        GROUP BY s.setor_id, s.nome, s.codigo
        ORDER BY s.codigo""")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]} PDVs")

except Exception as e:
    conn.rollback()
    print(f"ERRO: {e}")
    import traceback; traceback.print_exc()
finally:
    cur.close()
    conn.close()
