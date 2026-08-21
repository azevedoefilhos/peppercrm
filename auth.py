# auth.py — PepperCRM
# Autenticação com persistência via token em query_params + session_state

import streamlit as st
import hashlib
import secrets
from datetime import datetime, timedelta
from database import query, execute_write

TTL_LEMBRAR = 7 * 24 * 60
TTL_NORMAL  = 8 * 60
COOKIE_NAME = "pepper_token"


def _hash(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def _garantir_tabela_tokens():
    try:
        execute_write("""CREATE TABLE IF NOT EXISTS sessao_token (
            token       TEXT PRIMARY KEY,
            usuario_id  INTEGER NOT NULL,
            expira_em   TEXT NOT NULL,
            ativo       INTEGER DEFAULT 1
        )""")
    except Exception:
        pass


def _usuario_valido(login: str, senha: str):
    rows = query(
        "SELECT usuario_id, nome, email, tipo, empresa_id FROM usuario "
        "WHERE email=? AND senha_hash=? AND ativo=1",
        (login.strip().lower(), _hash(senha))
    )
    if not rows:
        return None
    r = rows[0]
    return {"id": r[0], "nome": r[1], "email": r[2], "tipo": r[3], "empresa_id": r[4] if len(r)>4 else 1}


def _criar_token(usuario_id: int, lembrar: bool) -> str:
    _garantir_tabela_tokens()
    token  = secrets.token_urlsafe(32)
    ttl    = TTL_LEMBRAR if lembrar else TTL_NORMAL
    expira = (datetime.now() + timedelta(minutes=ttl)).isoformat()
    execute_write(
        "INSERT INTO sessao_token (token, usuario_id, expira_em, ativo) VALUES (?,?,?,1)",
        (token, usuario_id, expira)
    )
    return token


def _validar_token(token: str):
    if not token or len(token) < 10:
        return None
    _garantir_tabela_tokens()
    rows = query("""
        SELECT u.usuario_id, u.nome, u.email, u.tipo, st.expira_em, u.empresa_id
        FROM sessao_token st
        JOIN usuario u ON u.usuario_id = st.usuario_id
        WHERE st.token=? AND st.ativo=1 AND u.ativo=1
    """, (token,))
    if not rows:
        return None
    r = rows[0]
    try:
        expira = datetime.fromisoformat(str(r[4])[:19])
        if datetime.now() > expira:
            execute_write("UPDATE sessao_token SET ativo=0 WHERE token=?", (token,))
            return None
    except Exception:
        return None
    return {"id": r[0], "nome": r[1], "email": r[2], "tipo": r[3], "empresa_id": r[4] if len(r)>4 else 1}


def logout():
    token = st.query_params.get(COOKIE_NAME, "") or st.session_state.get("_pepper_token", "")
    if token:
        try:
            execute_write("UPDATE sessao_token SET ativo=0 WHERE token=?", (token,))
        except Exception:
            pass
    st.query_params.clear()
    for k in ["auth_ok", "auth_user", "_pepper_token"]:
        st.session_state.pop(k, None)
    st.rerun()


def usuario_atual() -> dict:
    return st.session_state.get("auth_user", {})


def tela_login() -> bool:
    # 1. Sessao em memoria
    if st.session_state.get("auth_ok"):
        return True

    # 2. Token em query_params (URL salva como favorito com token)
    token = st.query_params.get(COOKIE_NAME, "") or st.session_state.get("_pepper_token", "")
    if token:
        usuario = _validar_token(token)
        if usuario:
            st.session_state["auth_ok"]      = True
            st.session_state["auth_user"]    = usuario
            st.session_state["_pepper_token"] = token
            # Mantem token na URL para persistir nos reloads
            st.query_params[COOKIE_NAME] = token
            return True
        else:
            st.query_params.clear()
            st.session_state.pop("_pepper_token", None)

    # 3. Tela de login
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align:center;color:#1A5C38;'>🌶️ PepperCRM</h1>"
            "<p style='text-align:center;color:#6B7280;margin-bottom:2rem;'>"
            "Gestao comercial para representantes</p>",
            unsafe_allow_html=True
        )
        with st.container(border=True):
            st.markdown("#### Acesso ao sistema")
            login   = st.text_input("Usuario", placeholder="seu usuario", key="login_input")
            senha   = st.text_input("Senha", type="password", placeholder="sua senha", key="senha_input")
            lembrar = st.checkbox("Lembrar por 7 dias", value=True, key="lembrar_input")
            if st.session_state.get("login_erro"):
                st.error("Usuario ou senha incorretos.")
            if st.button("Entrar", width="stretch", type="primary"):
                if login and senha:
                    usuario = _usuario_valido(login, senha)
                    if usuario:
                        st.session_state.pop("login_erro", None)
                        st.session_state["auth_ok"]   = True
                        st.session_state["auth_user"] = usuario
                        if lembrar:
                            token = _criar_token(usuario["id"], lembrar=True)
                            st.query_params[COOKIE_NAME]       = token
                            st.session_state["_pepper_token"]  = token
                        st.rerun()
                    else:
                        st.session_state["login_erro"] = True
                        st.rerun()
                else:
                    st.session_state["login_erro"] = True
                    st.rerun()
        st.markdown(
            "<p style='text-align:center;color:#9CA3AF;font-size:0.75rem;margin-top:1rem;'>"
            "Azevedo e Filhos Representacao Comercial</p>",
            unsafe_allow_html=True
        )
    return False
