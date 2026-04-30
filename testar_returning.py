#!/usr/bin/env python3
"""Testa se SQLite suporta RETURNING e se execute_write retorna o ID corretamente."""
import sqlite3, sys

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE teste (teste_id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

# Teste 1: com RETURNING
try:
    cur = conn.execute("INSERT INTO teste (nome) VALUES (?) RETURNING teste_id", ("abc",))
    row = cur.fetchone()
    print(f"RETURNING suportado: ID={row[0] if row else None}")
except Exception as e:
    print(f"RETURNING NAO suportado: {e}")

# Teste 2: sem RETURNING (lastrowid)
cur2 = conn.execute("INSERT INTO teste (nome) VALUES (?)", ("def",))
conn.commit()
print(f"lastrowid: {cur2.lastrowid}")

import sqlite3
print(f"SQLite version: {sqlite3.sqlite_version}")
