#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("relatorios.py")
src = CAMINHO.read_text(encoding="utf-8")

ANTIGO = '''    pdvs = query("""
        SELECT
            c.cliente_id,
            c.nome_fantasia,
            c.cidade,
            pdv.cluster,
            pdv.tamanho_pdv,
            pdv.tipo_pdv,
            c.status,
            COUNT(DISTINCT p.pedido_id)                               AS qtd_pedidos,
            ROUND(COALESCE(SUM(pi.quantidade * pi.preco_final
                * (1 - COALESCE(p.desconto_geral,0)/100.0)),0),2)     AS total_comprado,
            MAX(p.data_pedido)                                        AS ultimo_pedido
        FROM cliente c
        JOIN pdv ON pdv.pdv_id = c.cliente_id
        LEFT JOIN pedido p ON p.cliente_id = c.cliente_id
            AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
            AND (? = 'todos' OR p.fornecedor_id = ?)
        LEFT JOIN pedido_item pi ON pi.pedido_id = p.pedido_id
            AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
        WHERE c.status NOT IN ('Inativo','Encerrado')
          AND (? = 'Todos' OR pdv.cluster = ?)
          AND (? = 'Todos' OR pdv.tamanho_pdv = ?)
        GROUP BY c.cliente_id, c.nome_fantasia, c.cidade,
                 pdv.cluster, pdv.tamanho_pdv, pdv.tipo_pdv, c.status
        ORDER BY pdv.cluster, pdv.tamanho_pdv, total_comprado DESC
    """, (forn_sel[0], forn_sel[0], cl_sel, cl_sel, tam_sel, tam_sel))'''

NOVO = '''    _forn_where2 = "AND p.fornecedor_id = ?" if _forn_id_cob else ""
    _forn_params2 = (_forn_id_cob,) if _forn_id_cob else ()
    pdvs = query(f"""
        SELECT
            c.cliente_id,
            c.nome_fantasia,
            c.cidade,
            pdv.cluster,
            pdv.tamanho_pdv,
            pdv.tipo_pdv,
            c.status,
            COUNT(DISTINCT p.pedido_id)                               AS qtd_pedidos,
            ROUND(COALESCE(SUM(pi.quantidade * pi.preco_final
                * (1 - COALESCE(p.desconto_geral,0)/100.0)),0),2)     AS total_comprado,
            MAX(p.data_pedido)                                        AS ultimo_pedido
        FROM cliente c
        JOIN pdv ON pdv.pdv_id = c.cliente_id
        LEFT JOIN pedido p ON p.cliente_id = c.cliente_id
            AND p.status_pedido NOT IN (\'CANCELADO\',\'RECUSADO\')
            {_forn_where2}
        LEFT JOIN pedido_item pi ON pi.pedido_id = p.pedido_id
            AND pi.status_item NOT IN (\'PENDENTE\',\'DEVOLVIDO\')
        WHERE c.status NOT IN (\'Inativo\',\'Encerrado\')
          AND (? = \'Todos\' OR pdv.cluster = ?)
          AND (? = \'Todos\' OR pdv.tamanho_pdv = ?)
        GROUP BY c.cliente_id, c.nome_fantasia, c.cidade,
                 pdv.cluster, pdv.tamanho_pdv, pdv.tipo_pdv, c.status
        ORDER BY pdv.cluster, pdv.tamanho_pdv, total_comprado DESC
    """, _forn_params2 + (cl_sel, cl_sel, tam_sel, tam_sel))'''

if ANTIGO in src:
    src2 = src.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(src2, encoding="utf-8")
    print("✅ Corrigido")
else:
    print("⚠️  Padrão não encontrado")
