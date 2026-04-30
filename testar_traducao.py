#!/usr/bin/env python3
"""Testa a tradução do SQL problemático e imprime o resultado."""
import sys
sys.path.insert(0, ".")

# Força modo Supabase para testar o tradutor
import os
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
        WHERE cr.ativo=1 AND cr.tipo_topico='Negociação'
          AND cr.status NOT IN ('Concluído','Cancelado')
        GROUP BY cr.contato_id
        HAVING dias >= 15
    )"""

resultado = database._traduzir_sql_pg(sql)
print("=== SQL TRADUZIDO ===")
print(resultado)
print("====================")

# Verifica se ainda tem julianday
if "julianday" in resultado.lower():
    print("❌ ERRO: julianday ainda presente!")
else:
    print("✅ julianday traduzido corretamente")

# Verifica HAVING dias (problemático no PostgreSQL - alias não funciona em HAVING)
if "HAVING dias" in resultado:
    print("⚠️  AVISO: 'HAVING dias' usa alias - pode falhar no PostgreSQL!")
    print("   Solução: usar subconsulta ou repetir a expressão no HAVING")
