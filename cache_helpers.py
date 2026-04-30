"""
cache_helpers.py — Funções cacheadas para dados estáticos do PepperCRM.
Use estas funções em vez de query() direto para dados que mudam raramente.
TTL padrão: 5 minutos (300s). Dados de configuração: 10 minutos.
"""
import streamlit as st
from database import query

@st.cache_data(ttl=300, show_spinner=False)
def cache_clientes():
    return query("""
        SELECT cliente_id, nome_fantasia, cidade, estado, status
        FROM cliente WHERE ativo=1 ORDER BY nome_fantasia
    """)

@st.cache_data(ttl=300, show_spinner=False)
def cache_fornecedores():
    return query("""
        SELECT fornecedor_id, nome_fantasia
        FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia
    """)

@st.cache_data(ttl=600, show_spinner=False)
def cache_categorias():
    return query("""
        SELECT categoria_id, nome_categoria
        FROM categoria WHERE ativo=1 ORDER BY nome_categoria
    """)

@st.cache_data(ttl=600, show_spinner=False)
def cache_linhas():
    return query("""
        SELECT linha_id, nome_linha
        FROM linha WHERE ativo=1 ORDER BY nome_linha
    """)

@st.cache_data(ttl=300, show_spinner=False)
def cache_produtos_fornecedor(fornecedor_id):
    return query("""
        SELECT produto_id, descricao_curta, descricao, codigo_produto,
               peso, unidade_medida, unidades_caixa, ean
        FROM produto WHERE fornecedor_id=? AND ativo=1 ORDER BY descricao_curta
    """, (fornecedor_id,))

@st.cache_data(ttl=300, show_spinner=False)
def cache_pdvs_cliente(cliente_id):
    return query("""
        SELECT pdv_id, numero_loja, nome_loja, cidade, estado
        FROM pdv WHERE cliente_id=? AND ativo=1 ORDER BY numero_loja, nome_loja
    """, (cliente_id,))

@st.cache_data(ttl=600, show_spinner=False)
def cache_concorrentes_fornecedor(fornecedor_id):
    return query("""
        SELECT c.concorrente_id, c.marca_concorrente
        FROM concorrente c
        WHERE c.fornecedor_id=? AND c.ativo=1
        ORDER BY c.marca_concorrente
    """, (fornecedor_id,))

def invalidar_cache():
    """Chama quando dados são alterados para forçar recarga."""
    cache_clientes.clear()
    cache_fornecedores.clear()
    cache_categorias.clear()
    cache_linhas.clear()
    cache_produtos_fornecedor.clear()
    cache_pdvs_cliente.clear()
    cache_concorrentes_fornecedor.clear()
