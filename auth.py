# auth.py — PepperCRM
# Autenticação simples com login/senha e "lembrar de mim"

import streamlit as st
import hashlib
from datetime import datetime, timedelta
from database import query

# Tempo de sessão: 7 dias com "lembrar", 8h sem
TTL_LEMBRAR = 7 * 24 * 60  # minutos
TTL_NORMAL  = 8 * 60        # minutos


def _hash(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def _usuario_valido(login: str, senha: str):
    """Retorna dict com dados do usuário ou None se inválido."""
    rows = query(
        "SELECT usuario_id, nome, email, tipo, ativo FROM usuario WHERE email=? AND senha_hash=? AND ativo=1",
        (login.strip().lower(), _hash(senha))
    )
    if not rows:
        return None
    r = rows[0]
    return {"id": r[0], "nome": r[1], "email": r[2], "tipo": r[3]}


def _sessao_valida() -> bool:
    """Verifica se há sessão ativa e não expirada."""
    if not st.session_state.get("auth_ok"):
        return False
    expira = st.session_state.get("auth_expira")
    if not expira:
        return False
    return datetime.now() < expira


def _iniciar_sessao(usuario: dict, lembrar: bool):
    """Salva sessão no session_state."""
    ttl = TTL_LEMBRAR if lembrar else TTL_NORMAL
    st.session_state["auth_ok"]     = True
    st.session_state["auth_user"]   = usuario
    st.session_state["auth_expira"] = datetime.now() + timedelta(minutes=ttl)
    st.session_state["auth_lembrar"]= lembrar


def logout():
    """Encerra a sessão."""
    for k in ["auth_ok", "auth_user", "auth_expira", "auth_lembrar"]:
        st.session_state.pop(k, None)
    st.rerun()


def usuario_atual() -> dict:
    """Retorna dados do usuário logado."""
    return st.session_state.get("auth_user", {})


def tela_login():
    """Renderiza a tela de login. Retorna True se autenticado."""

    # Já autenticado e sessão válida
    if _sessao_valida():
        return True

    # Limpa auth expirada
    if st.session_state.get("auth_ok") and not _sessao_valida():
        for k in ["auth_ok", "auth_user", "auth_expira"]:
            st.session_state.pop(k, None)

    # Layout da tela de login
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align:center; color:#1A5C38;'>🌶️ PepperCRM</h1>"
            "<p style='text-align:center; color:#6B7280; margin-bottom:2rem;'>"
            "Gestão comercial para representantes</p>",
            unsafe_allow_html=True
        )

        with st.container(border=True):
            st.markdown("#### Acesso ao sistema")

            login = st.text_input(
                "Usuário",
                placeholder="seu usuário",
                key="login_input"
            )
            senha = st.text_input(
                "Senha",
                type="password",
                placeholder="sua senha",
                key="senha_input"
            )
            lembrar = st.checkbox("Lembrar por 7 dias", value=True, key="lembrar_input")

            entrar = st.button("Entrar", width="stretch", type="primary")

            if st.session_state.get("login_erro"):
                st.error("Usuário ou senha incorretos.")

        st.markdown(
            "<p style='text-align:center; color:#9CA3AF; font-size:0.75rem; margin-top:1rem;'>"
            "Azevedo e Filhos Representação Comercial</p>",
            unsafe_allow_html=True
        )

    if entrar:
        if not login or not senha:
            st.session_state["login_erro"] = True
            st.rerun()

        usuario = _usuario_valido(login.lower(), senha)
        if usuario:
            st.session_state.pop("login_erro", None)
            _iniciar_sessao(usuario, lembrar)
            st.rerun()
        else:
            st.session_state["login_erro"] = True
            st.rerun()

    return False
