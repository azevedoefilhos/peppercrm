#!/usr/bin/env python3
"""
Corrige queries com HAVING alias no crm_app.py.
No PostgreSQL, aliases definidos no SELECT nao podem ser usados no HAVING.
Solucao: envolve a subquery em mais uma camada SELECT.
"""
import pathlib, re, sys

CAMINHO = pathlib.Path("crm_app.py")
if not CAMINHO.exists():
    print("ERRO: crm_app.py nao encontrado.")
    sys.exit(1)

texto = CAMINHO.read_text(encoding="utf-8")

# Corrige o padrao especifico da query neg_paradas
ANTIGO = '''    neg_paradas = query("""
        SELECT COUNT(*), MIN(dias) FROM (
            SELECT cr.contato_id,
                   CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) AS dias
            FROM contato_registro cr
            LEFT JOIN contato_interacao ci ON ci.contato_id=cr.contato_id AND ci.ativo=1
            WHERE cr.ativo=1 AND cr.tipo_topico='Negociação'
              AND cr.status NOT IN ('Concluído','Cancelado')
            GROUP BY cr.contato_id
            HAVING dias >= 15
        )""")'''

NOVO = '''    neg_paradas = query("""
        SELECT COUNT(*), MIN(dias) FROM (
            SELECT cr.contato_id,
                   CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) AS dias
            FROM contato_registro cr
            LEFT JOIN contato_interacao ci ON ci.contato_id=cr.contato_id AND ci.ativo=1
            WHERE cr.ativo=1 AND cr.tipo_topico='Negociação'
              AND cr.status NOT IN ('Concluído','Cancelado')
            GROUP BY cr.contato_id
            HAVING CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) >= 15
        )""")'''

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    print("✅ Query neg_paradas corrigida.")
else:
    # Busca flexível
    padrao = re.compile(
        r'(neg_paradas\s*=\s*query\(""".*?HAVING\s+)dias(\s*>=\s*15\s*\)\s*""")',
        re.DOTALL
    )
    if padrao.search(texto):
        novo = padrao.sub(
            r'\1CAST(julianday(\'now\') - julianday('
            r'COALESCE(MAX(ci.data_interacao), cr.data_contato)) AS INTEGER)\2',
            texto, count=1
        )
        print("✅ Query corrigida via regex.")
    else:
        print("⚠️  Padrão não encontrado. Buscando todas as ocorrências de HAVING dias...")
        # Substitui qualquer HAVING dias >= N por HAVING que repete o CAST
        # Estratégia mais simples: wrap em subquery
        padrao2 = re.compile(
            r'(SELECT COUNT\(\*\), MIN\(dias\) FROM \()(.*?)(HAVING dias >= \d+)(\s*\)""")',
            re.DOTALL
        )
        if padrao2.search(texto):
            def substituir(m):
                return f"SELECT COUNT(*), MIN(dias) FROM ({m.group(2)}HAVING CAST(julianday('now') - julianday(COALESCE(MAX(ci.data_interacao), cr.data_contato)) AS INTEGER) >= 15{m.group(4)}"
            novo = padrao2.sub(substituir, texto, count=1)
            print("✅ Substituição alternativa aplicada.")
        else:
            print("❌ Nenhum padrão encontrado. Edite manualmente a linha com HAVING dias.")
            sys.exit(1)

CAMINHO.write_text(novo, encoding="utf-8")

# Verificação
c = CAMINHO.read_text(encoding="utf-8")
if "HAVING dias" not in c:
    print("✅ 'HAVING dias' removido com sucesso.")
else:
    print("⚠️  Ainda há 'HAVING dias' no arquivo — verifique manualmente.")
