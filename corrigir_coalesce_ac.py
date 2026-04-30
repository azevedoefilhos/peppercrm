#!/usr/bin/env python3
import pathlib, re

CAMINHO = pathlib.Path("analise_competitiva.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src

# Substitui todas as ocorrencias de COALESCE com pdv_id integer e cliente_id||texto
src = re.sub(
    r'COALESCE\(pp\.pdv_id,\s*pp\.cliente_id\s*\|\|\s*\'c\'\)',
    "COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c')",
    src
)
src = re.sub(
    r'COALESCE\(pdv_id,\s*cliente_id\s*\|\|\s*\'c\'\)',
    "COALESCE(pdv_id::TEXT, cliente_id::TEXT||'c')",
    src
)

count = original.count("COALESCE(pp.pdv_id, pp.cliente_id") + original.count("COALESCE(pdv_id, cliente_id")
CAMINHO.write_text(src, encoding="utf-8")
print(f"OK - {count} ocorrencia(s) corrigida(s)")
