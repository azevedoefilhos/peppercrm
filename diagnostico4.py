# diagnostico4.py
# Simula exatamente o que o app chama, mostrando erros que _query_safe engole
import os, sys
pasta = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pasta)

# Força reload
for mod in ["resultado_operacional", "database"]:
    if mod in sys.modules:
        del sys.modules[mod]

from database import query, _check_supabase

print(f"Usando PostgreSQL? {_check_supabase()}")

d_ini, d_fim = "2025-12-01", "2026-05-31"

# Testa cada query individualmente com erro visível
queries = {
    "comissoes_previsto": ("""
        SELECT ROUND(SUM(
            pi.quantidade * pi.preco_final
            * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
        ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2)
        FROM pedido p
        JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
            AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
        LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
        LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
        WHERE p.status_pedido = 'ENTREGUE'
          AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
          AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?
    """, (d_ini, d_fim)),

    "despesas_total": ("""
        SELECT ROUND(SUM(valor), 2)
        FROM despesa
        WHERE ativo IS NOT FALSE
          AND data_despesa BETWEEN ? AND ?
    """, (d_ini, d_fim)),

    "comissoes_por_mes": ("""
        SELECT
            CAST(strftime('%Y', COALESCE(p.data_entrega_realizada, p.data_pedido)) AS INTEGER) AS ano,
            CAST(strftime('%m', COALESCE(p.data_entrega_realizada, p.data_pedido)) AS INTEGER) AS mes,
            ROUND(SUM(
                pi.quantidade * pi.preco_final
                * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
            ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2) AS valor_com
        FROM pedido p
        JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
            AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
        LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
        LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
        WHERE p.status_pedido = 'ENTREGUE'
          AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
        GROUP BY ano, mes
    """, ()),
}

for nome, (sql, params) in queries.items():
    print(f"\n{'='*60}")
    print(f">>> {nome}")
    try:
        resultado = query(sql, params)
        print(f"    resultado bruto: {resultado}")
        if resultado:
            print(f"    [0][0] = {resultado[0][0]}")
    except Exception as e:
        import traceback
        print(f"    ERRO: {e}")
        traceback.print_exc()

# Agora testa _buscar_totais_periodo com print de debug dentro
print(f"\n{'='*60}")
print(">>> Chamando _buscar_totais_periodo com debug interno")

# Replica a função manualmente com prints
try:
    r_com = query("""
        SELECT ROUND(SUM(
            pi.quantidade * pi.preco_final
            * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
        ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2)
        FROM pedido p
        JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
            AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
        LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
        LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
        WHERE p.status_pedido = 'ENTREGUE'
          AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
          AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?
    """, (d_ini, d_fim))
    print(f"    r_com bruto: {r_com}")
    print(f"    r_com[0]: {r_com[0] if r_com else 'VAZIO'}")
    print(f"    r_com[0][0]: {r_com[0][0] if r_com else 'VAZIO'}")
    total_com = float((r_com or [[0]])[0][0] or 0)
    print(f"    total_com final: {total_com}")
except Exception as e:
    import traceback
    print(f"    ERRO: {e}")
    traceback.print_exc()

print("\nDiagnóstico 4 concluído.")
