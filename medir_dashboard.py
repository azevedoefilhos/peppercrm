# medir_dashboard.py
from dotenv import load_dotenv
load_dotenv()
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import query
from datetime import date, timedelta

hoje        = date.today().isoformat()
mes_ini     = date.today().strftime("%Y-%m-01")
amanha      = (date.today() + timedelta(days=1)).isoformat()
depois      = (date.today() + timedelta(days=2)).isoformat()
tres_dias   = (date.today() - timedelta(days=3)).isoformat()
trinta_dias = (date.today() - timedelta(days=30)).isoformat()
sete_dias   = (date.today() + timedelta(days=7)).isoformat()
limite_neg  = (date.today() - timedelta(days=15)).isoformat()

t_total = time.time()

def medir(nome, sql, params=()):
    t0 = time.time()
    try:
        r = query(sql, params)
        t = time.time() - t0
        n = len(r) if r else 0
        print(f"  {nome}: {t:.2f}s ({n} linhas)")
        return r
    except Exception as e:
        print(f"  {nome}: ERRO {e}")
        return []

print("Medindo queries do dashboard...")

medir("pedidos abertos",
    "SELECT COUNT(*) FROM pedido WHERE status_pedido IN ('ABERTO','ENVIADO')")

medir("pedidos do mes + faturamento",
    """SELECT COUNT(DISTINCT p.pedido_id),
              ROUND(COALESCE(SUM(pi.quantidade*pi.preco_final*(1-COALESCE(p.desconto_geral,0)/100.0)),0)::NUMERIC,2)
       FROM pedido p
       LEFT JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
           AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
       WHERE p.status_pedido NOT IN ('CANCELADO','RECUSADO')
         AND p.data_pedido >= ?""", (mes_ini,))

medir("comissao do mes",
    """SELECT ROUND(COALESCE(SUM(
           pi.quantidade*pi.preco_final*(1-COALESCE(p.desconto_geral,0)/100.0)
           *COALESCE(p.comissao_percentual,COALESCE(com.percentual,0))/100.0
       ),0)::NUMERIC,2)
       FROM pedido p
       LEFT JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
           AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
       LEFT JOIN comissao com ON p.fornecedor_id=com.fornecedor_id AND com.ativo=1
       WHERE p.status_pedido='ENTREGUE' AND p.data_pedido >= ?""", (mes_ini,))

medir("entregas proximas",
    """SELECT COUNT(*) FROM pedido
       WHERE data_entrega BETWEEN ? AND ?
         AND status_pedido NOT IN ('CANCELADO','RECUSADO','ENTREGUE','DEVOLVIDO')""",
    (hoje, sete_dias))

medir("contatos e followups",
    """SELECT
           COUNT(DISTINCT CASE WHEN cr.ativo!=0 AND cr.data_contato >= ? THEN cr.contato_id END),
           COUNT(DISTINCT CASE WHEN cr.ativo!=0 AND cr.tipo_topico='Negociação'
                 AND cr.status NOT IN ('Concluído','Cancelado') THEN cr.contato_id END),
           COUNT(DISTINCT CASE WHEN cr.ativo!=0 AND cr.data_followup BETWEEN ? AND ?
                 AND cr.status NOT IN ('Concluído','Cancelado') THEN cr.contato_id END)
       FROM contato_registro cr""", (mes_ini, amanha, depois))

medir("misc (clientes, pesquisas, visitas, rupturas)",
    """SELECT
           (SELECT COUNT(*) FROM cliente WHERE status NOT IN ('Encerrado','Cancelado')),
           (SELECT COUNT(*) FROM pesquisa_preco WHERE data_pesquisa >= ?),
           (SELECT COUNT(*) FROM visita_cliente WHERE data_visita >= ?),
           (SELECT COUNT(*) FROM pesquisa_preco WHERE status='rascunho' AND data_pesquisa <= ?),
           (SELECT COUNT(*) FROM pesquisa_preco_item pi
               JOIN pesquisa_preco pp ON pi.pesquisa_id=pp.pesquisa_id
               WHERE pi.ruptura=1 AND pp.data_pesquisa >= ?)""",
    (mes_ini, mes_ini, tres_dias, trinta_dias))

medir("clientes sem pedido 30d",
    """SELECT COUNT(*) FROM cliente c WHERE c.ativo!=0
       AND NOT EXISTS (SELECT 1 FROM pedido p WHERE p.cliente_id=c.cliente_id
           AND p.data_pedido >= ? AND p.status_pedido NOT IN ('CANCELADO','RECUSADO'))""",
    (trinta_dias,))

medir("followups vencidos",
    """SELECT cr.contato_id, cr.assunto, cr.data_followup
       FROM contato_registro cr
       WHERE cr.ativo!=0 AND cr.data_followup < ?
         AND cr.status NOT IN ('Concluído','Cancelado','Proposta enviada')
       ORDER BY cr.data_followup""", (hoje,))

medir("negociacoes paradas",
    """SELECT cr.contato_id, COALESCE(MAX(ci.data_interacao), cr.data_contato)
       FROM contato_registro cr
       LEFT JOIN contato_interacao ci ON ci.contato_id=cr.contato_id AND ci.ativo!=0
       WHERE cr.ativo!=0 AND cr.tipo_topico='Negociação'
         AND cr.status NOT IN ('Concluído','Cancelado')
       GROUP BY cr.contato_id
       HAVING COALESCE(MAX(ci.data_interacao), cr.data_contato) <= ?""", (limite_neg,))

medir("pedidos abertos detalhe",
    """SELECT p.pedido_id, p.data_pedido, c.nome_fantasia, f.nome_fantasia, p.status_pedido
       FROM pedido p JOIN cliente c ON p.cliente_id=c.cliente_id
       JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
       WHERE p.status_pedido IN ('ABERTO','ENVIADO')
       ORDER BY p.data_pedido DESC LIMIT 10""")

print(f"\nTOTAL: {time.time()-t_total:.2f}s")
print("\nSe total < 5s, o dashboard pode ficar na home com st.cache_data.")
