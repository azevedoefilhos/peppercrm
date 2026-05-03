#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix 1: Renomear "Campo" para "Rápido" em todos os lugares
replacements = [
    ('"⚡ Campo" if st.session_state[modo_key] != "campo" else "⚡ Campo ✓"',
     '"⚡ Rápido" if st.session_state[modo_key] != "campo" else "⚡ Rápido ✓"'),
    ('help="Escanear EAN ou buscar por nome/categoria — modo campo unificado"',
     'help="Escanear EAN ou buscar por nome/categoria — modo rápido unificado"'),
    ('st.subheader("⚡ Modo Campo")',
     'st.subheader("⚡ Modo Rápido")'),
]

for old, new in replacements:
    if old in src:
        src = src.replace(old, new, 1)
        print(f"✅ Renomeado: {old[:40]}...")
    else:
        print(f"⚠️  Não encontrado: {old[:40]}...")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
