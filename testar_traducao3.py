#!/usr/bin/env python3
import sys, os
sys.path.insert(0, ".")
os.environ["SUPABASE_URL"] = "https://fake.supabase.co"
os.environ["SUPABASE_DB_PASSWORD"] = "fake"
import database

sql = """
        SELECT COUNT(*), MIN(dias) FROM (
            SELECT cr.contato_id,
                   CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) AS dias
            FROM contato_registro cr
            LEFT JOIN contato_interacao ci ON ci.contato_id=cr.contato_id AND ci.ativo=1
            WHERE cr.ativo=1 AND cr.tipo_topico='Negociacao'
              AND cr.status NOT IN ('Concluido','Cancelado')
            GROUP BY cr.contato_id
            HAVING CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) >= 15
        )"""

r = database._traduzir_sql_pg(sql)
print("=== RESULTADO ===")
print(r)
print("=================")
print("julianday presente:", "julianday" in r.lower())
print("EXTRACT presente:", "EXTRACT" in r.upper())
