#!/usr/bin/env python3
import pathlib

src = pathlib.Path("contatos.py").read_text(encoding="utf-8")
original = src

# Fix: usar data da ultima interacao OU data do contato
OLD = '''    if fil_periodo == "Hoje":
        where.append("cr.data_contato::date = CURRENT_DATE")
    elif fil_periodo == "Esta semana":
        where.append("cr.data_contato::date >= CURRENT_DATE - INTERVAL '7 days'")
    elif fil_periodo == "Este mês":
        where.append("cr.data_contato::date >= DATE_TRUNC('month', CURRENT_DATE)")
    elif fil_periodo == "Últimos 30 dias":
        where.append("cr.data_contato::date >= CURRENT_DATE - INTERVAL '30 days'")
    elif fil_periodo == "Últimos 90 dias":
        where.append("cr.data_contato::date >= CURRENT_DATE - INTERVAL '90 days'")'''

NEW = '''    # Filtro de periodo: considera data do contato OU data da ultima interacao
    _ult_int = """(SELECT MAX(ci.data_interacao) FROM contato_interacao ci
                   WHERE ci.contato_id=cr.contato_id AND ci.ativo=1)"""
    if fil_periodo == "Hoje":
        where.append(f"(cr.data_contato::date = CURRENT_DATE OR ({_ult_int})::date = CURRENT_DATE)")
    elif fil_periodo == "Esta semana":
        where.append(f"(cr.data_contato::date >= CURRENT_DATE - INTERVAL '7 days' OR ({_ult_int})::date >= CURRENT_DATE - INTERVAL '7 days')")
    elif fil_periodo == "Este mês":
        where.append(f"(cr.data_contato::date >= DATE_TRUNC('month', CURRENT_DATE) OR ({_ult_int})::date >= DATE_TRUNC('month', CURRENT_DATE))")
    elif fil_periodo == "Últimos 30 dias":
        where.append(f"(cr.data_contato::date >= CURRENT_DATE - INTERVAL '30 days' OR ({_ult_int})::date >= CURRENT_DATE - INTERVAL '30 days')")
    elif fil_periodo == "Últimos 90 dias":
        where.append(f"(cr.data_contato::date >= CURRENT_DATE - INTERVAL '90 days' OR ({_ult_int})::date >= CURRENT_DATE - INTERVAL '90 days')")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("contatos.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
