#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("analise_competitiva.py")
src = CAMINHO.read_text(encoding="utf-8")

old = "COALESCE(pdv_id, cliente_id||'c')"
new = "COALESCE(pdv_id::TEXT, cliente_id::TEXT||'c')"

if old in src:
    src2 = src.replace(old, new)
    CAMINHO.write_text(src2, encoding="utf-8")
    print(f"OK - {src.count(old)} ocorrencia(s) substituida(s)")
else:
    print("NAO ENCONTRADO")
    # Mostra trecho relevante
    idx = src.find("COALESCE(pdv_id")
    if idx >= 0:
        print("Encontrado:", repr(src[idx:idx+50]))
