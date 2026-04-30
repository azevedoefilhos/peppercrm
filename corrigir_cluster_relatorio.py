#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("relatorios.py")
src = CAMINHO.read_text(encoding="utf-8")

ANTIGO = '''    cob = query("""
        SELECT
            pdv.cluster,
            pdv.tamanho_pdv,
            COUNT(DISTINCT c.cliente_id)                              AS total_pdvs,
            COUNT(DISTINCT CASE WHEN p.pedido_id IS NOT NULL
                  THEN c.cliente_id END)                              AS pdvs_com_pedido,
            ROUND(COUNT(DISTINCT CASE WHEN p.pedido_id IS NOT NULL
                  THEN c.cliente_id END) * 100.0
                  / NULLIF(COUNT(DISTINCT c.cliente_id),0), 1)        AS cobertura_pct
        FROM cliente c
        JOIN pdv ON pdv.pdv_id = c.cliente_id
        LEFT JOIN pedido p ON p.cliente_id = c.cliente_id
            AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
            AND (? = 'todos' OR p.fornecedor_id = ?)
        WHERE c.status NOT IN ('Inativo','Encerrado')
          AND (? = 'Todos' OR pdv.cluster = ?)
          AND (? = 'Todos' OR pdv.tamanho_pdv = ?)
        GROUP BY pdv.cluster, pdv.tamanho_pdv, f.nome_fantasia
        ORDER BY pdv.cluster, pdv.tamanho_pdv
    """, (forn_sel[0], forn_sel[0], cl_sel, cl_sel, tam_sel, tam_sel))'''

NOVO = '''    _forn_id_cob = int(forn_sel[0]) if str(forn_sel[0]).lower() != 'todos' else None
    _forn_where  = "AND p.fornecedor_id = ?" if _forn_id_cob else ""
    _forn_params = (_forn_id_cob,) if _forn_id_cob else ()
    cob = query(f"""
        SELECT
            pdv.cluster,
            pdv.tamanho_pdv,
            COUNT(DISTINCT c.cliente_id)                              AS total_pdvs,
            COUNT(DISTINCT CASE WHEN p.pedido_id IS NOT NULL
                  THEN c.cliente_id END)                              AS pdvs_com_pedido,
            ROUND(COUNT(DISTINCT CASE WHEN p.pedido_id IS NOT NULL
                  THEN c.cliente_id END) * 100.0
                  / NULLIF(COUNT(DISTINCT c.cliente_id),0), 1)        AS cobertura_pct
        FROM cliente c
        JOIN pdv ON pdv.pdv_id = c.cliente_id
        LEFT JOIN pedido p ON p.cliente_id = c.cliente_id
            AND p.status_pedido NOT IN (\'CANCELADO\',\'RECUSADO\')
            {{_forn_where}}
        WHERE c.status NOT IN (\'Inativo\',\'Encerrado\')
          AND (? = \'Todos\' OR pdv.cluster = ?)
          AND (? = \'Todos\' OR pdv.tamanho_pdv = ?)
        GROUP BY pdv.cluster, pdv.tamanho_pdv
        ORDER BY pdv.cluster, pdv.tamanho_pdv
    """, _forn_params + (cl_sel, cl_sel, tam_sel, tam_sel))'''

if ANTIGO in src:
    src2 = src.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(src2, encoding="utf-8")
    print("✅ Corrigido")
else:
    print("⚠️  Padrão não encontrado")
