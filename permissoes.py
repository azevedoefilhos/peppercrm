# permissoes.py — PepperCRM
# Controle central de perfis de acesso e permissoes
# Usado por crm_app.py e todos os modulos para filtrar dados e menus

import streamlit as st

# ═══════════════════════════════════════════════════════════════
# HIERARQUIA DE PERFIS
# ═══════════════════════════════════════════════════════════════
NIVEL = {
    'MASTER':             99,  # super-admin — acessa todas as empresas
    'REPRESENTANTE_ADM':   5,  # admin da empresa — acesso total
    'REPRESENTANTE':       4,  # vendedor com carteira propria
    'VENDEDOR':            4,  # mesmo nivel que REPRESENTANTE
    'SUPERVISOR':          3,  # coordena grupo de promotores
    'PROMOTOR':            2,  # execucao em campo
}

# ═══════════════════════════════════════════════════════════════
# MODULOS PERMITIDOS POR PERFIL
# ═══════════════════════════════════════════════════════════════
MODULOS = {
    'MASTER': [
        "fornecedores", "clientes", "produtos", "tabelas_preco",
        "pedido", "ver_pedidos", "comissoes", "resultado_operacional",
        "contatos", "metas", "pesquisa", "despesas", "relatorios",
        "visitas", "configuracao", "usuarios", "empresas",
        "mix_analise", "concorrentes", "analise_competitiva",
    ],
    'REPRESENTANTE_ADM': [
        "fornecedores", "clientes", "produtos", "tabelas_preco",
        "pedido", "ver_pedidos", "comissoes", "resultado_operacional",
        "contatos", "metas", "pesquisa", "despesas", "relatorios",
        "visitas", "configuracao", "usuarios",
        "mix_analise", "concorrentes", "analise_competitiva",
    ],
    'REPRESENTANTE': [
        "clientes", "pedido", "ver_pedidos", "comissoes",
        "resultado_operacional", "contatos", "metas",
        "pesquisa", "despesas", "visitas",
        "mix_analise", "analise_competitiva",
    ],
    'VENDEDOR': [
        "clientes", "pedido", "ver_pedidos", "comissoes",
        "resultado_operacional", "contatos", "metas",
        "pesquisa", "despesas", "visitas",
    ],
    'SUPERVISOR': [
        "clientes", "pesquisa", "visitas", "relatorios",
    ],
    'PROMOTOR': [
        "visitas", "pesquisa",
    ],
}

# ═══════════════════════════════════════════════════════════════
# FUNCOES PRINCIPAIS
# ═══════════════════════════════════════════════════════════════

def usuario_atual() -> dict:
    """Retorna dados do usuario logado."""
    return st.session_state.get("auth_user", {})


def perfil_atual() -> str:
    """Retorna o tipo/perfil do usuario logado."""
    return usuario_atual().get("tipo", "PROMOTOR")


def empresa_id_atual() -> int:
    """Retorna empresa_id do usuario logado."""
    return int(usuario_atual().get("empresa_id", 1) or 1)


def usuario_id_atual() -> int:
    """Retorna usuario_id do usuario logado."""
    return int(usuario_atual().get("id", 0) or 0)


def nivel_atual() -> int:
    """Retorna nivel numerico do perfil atual."""
    return NIVEL.get(perfil_atual(), 0)


def e_master() -> bool:
    return perfil_atual() == 'MASTER'


def e_admin() -> bool:
    return perfil_atual() in ('MASTER', 'REPRESENTANTE_ADM')


def e_vendedor() -> bool:
    return perfil_atual() in ('REPRESENTANTE', 'VENDEDOR')


def e_supervisor() -> bool:
    return perfil_atual() == 'SUPERVISOR'


def e_promotor() -> bool:
    return perfil_atual() == 'PROMOTOR'


def pode_acessar(modulo: str) -> bool:
    """Verifica se o usuario atual pode acessar o modulo."""
    perfil = perfil_atual()
    permitidos = MODULOS.get(perfil, [])
    return modulo in permitidos


def pode(nivel_minimo: str) -> bool:
    """Verifica se usuario tem nivel minimo de acesso."""
    return nivel_atual() >= NIVEL.get(nivel_minimo, 99)


# ═══════════════════════════════════════════════════════════════
# FILTROS DE DADOS
# ═══════════════════════════════════════════════════════════════

def get_filtro_vendedor() -> tuple:
    """
    Retorna (where_clause, params) para filtrar clientes por carteira.
    ADM e MASTER: sem filtro (veem todos).
    VENDEDOR/REPRESENTANTE: so sua carteira.
    """
    if e_admin() or e_master():
        return "", []
    uid = usuario_id_atual()
    return "AND c.vendedor_id = %s", [uid]


def get_filtro_promotor() -> tuple:
    """
    Retorna (where_clause, params) para filtrar por promotor.
    ADM/MASTER: sem filtro.
    SUPERVISOR: so promotores do seu grupo.
    PROMOTOR: so ele mesmo.
    """
    from database import query
    perfil = perfil_atual()
    uid    = usuario_id_atual()

    if e_admin() or e_master():
        return "", []

    if e_supervisor():
        # Busca IDs dos promotores do supervisor
        rows = query("""
            SELECT promotor_id FROM supervisor_promotor
            WHERE supervisor_id=%s AND ativo=1
        """, (uid,)) or []
        ids = [r[0] for r in rows]
        if not ids:
            return "AND 1=0", []  # supervisor sem promotores — nao ve nada
        placeholders = ",".join(["%s"] * len(ids))
        return f"AND p.promotor_id IN ({placeholders})", ids

    if e_promotor():
        # Busca o promotor_id vinculado ao usuario
        rows = query(
            "SELECT promotor_id FROM promotor WHERE usuario_id=%s AND ativo!=0 LIMIT 1",
            (uid,)
        ) or []
        if not rows:
            return "AND 1=0", []
        return "AND p.promotor_id = %s", [rows[0][0]]

    return "", []


def get_ids_promotores_visiveis() -> list:
    """
    Retorna lista de promotor_ids visiveis para o usuario atual.
    Usado em queries de visitas e pesquisas.
    """
    from database import query
    perfil = perfil_atual()
    uid    = usuario_id_atual()

    if e_admin() or e_master():
        rows = query("SELECT promotor_id FROM promotor WHERE ativo!=0") or []
        return [r[0] for r in rows]

    if e_supervisor():
        rows = query("""
            SELECT promotor_id FROM supervisor_promotor
            WHERE supervisor_id=%s AND ativo=1
        """, (uid,)) or []
        return [r[0] for r in rows]

    if e_promotor():
        rows = query(
            "SELECT promotor_id FROM promotor WHERE usuario_id=%s AND ativo!=0 LIMIT 1",
            (uid,)
        ) or []
        return [r[0] for r in rows]

    if e_vendedor():
        # Vendedor ve promotores que atendem seus clientes
        rows = query("""
            SELECT DISTINCT ap.promotor_id
            FROM att_promotor ap
            JOIN pdv p ON ap.pdv_id = p.pdv_id
            JOIN cliente c ON p.cliente_id = c.cliente_id
            WHERE c.vendedor_id = %s AND ap.ativo != 0
        """, (uid,)) or []
        return [r[0] for r in rows]

    return []


# ═══════════════════════════════════════════════════════════════
# MENU VISIVEL POR PERFIL
# ═══════════════════════════════════════════════════════════════

def get_menu() -> dict:
    """
    Retorna dicionario com botoes de menu visiveis para o perfil atual.
    Formato: {"chave": ("emoji Label", "pagina")}
    """
    perfil = perfil_atual()

    # Todos os modulos disponiveis
    todos = {
        "fornecedores":          ("🏭 Fornecedores",              "fornecedores"),
        "clientes":              ("👥 Clientes",                  "clientes"),
        "produtos":              ("📦 Produtos",                  "produtos"),
        "tabelas_preco":         ("💲 Tabelas de Preço",          "tabelas_preco"),
        "pedido":                ("🧾 Novo Pedido",               "pedido"),
        "ver_pedidos":           ("📊 Ver Pedidos",               "ver_pedidos"),
        "contatos":              ("📞 Contatos & Negociações",    "contatos"),
        "comissoes":             ("💰 Comissões",                 "comissoes"),
        "resultado_operacional": ("📈 Resultado Operacional",     "resultado_operacional"),
        "metas":                 ("🎯 Metas",                     "metas"),
        "pesquisa":              ("🔍 Pesquisa PDV",              "pesquisa"),
        "mix_analise":           ("🎯 Mix / Oferta",              "mix_analise"),
        "concorrentes":          ("🏷️ Concorrentes",             "concorrentes"),
        "analise_competitiva":   ("📊 Inteligência Competitiva", "analise_competitiva"),
        "relatorios":            ("📋 Relatórios",                "relatorios"),
        "despesas":              ("💸 Despesas",                  "despesas"),
        "visitas":               ("🗺️ Promotores & Roteiros",     "visitas"),
        "configuracao":          ("⚙️ Configuração",              "configuracao"),
        "usuarios":              ("👤 Usuários",                  "usuarios"),
        "empresas":              ("🏢 Empresas",                  "empresas"),
    }

    permitidos = MODULOS.get(perfil, [])
    return {k: v for k, v in todos.items() if k in permitidos}


# ═══════════════════════════════════════════════════════════════
# GUARDIAO DE ACESSO (usar no inicio de cada modulo)
# ═══════════════════════════════════════════════════════════════

def exigir_acesso(modulo: str):
    """
    Chama no inicio de cada tela de modulo.
    Se usuario nao tem permissao, mostra erro e para execucao.
    """
    if not pode_acessar(modulo):
        st.error("Voce nao tem permissao para acessar este modulo.")
        if st.button("Voltar ao menu"):
            st.session_state["pagina"] = "home"
            st.rerun()
        st.stop()


def exigir_admin():
    """Exige perfil ADM ou MASTER. Para execucao se nao tiver."""
    if not e_admin():
        st.error("Esta funcao e restrita ao administrador.")
        st.stop()
