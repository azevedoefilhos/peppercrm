# minha_conta.py — PepperCRM
# Tela de conta do usuario: trocar senha, ver dados, esqueci senha

import streamlit as st
import hashlib
from database import query, execute_write
from permissoes import usuario_id_atual, usuario_atual

def _ir(p):
    st.session_state["pagina"] = p; st.rerun()

def _hash(s):
    return hashlib.sha256(s.encode()).hexdigest()

def tela_minha_conta():
    st.header("👤 Minha Conta")
    if st.button("⬅ Voltar"): _ir("home")

    u = usuario_atual()
    uid = usuario_id_atual()

    # Dados atuais
    dados = query("""SELECT nome, email, whatsapp, tipo FROM usuario
        WHERE usuario_id=%s""", (uid,)) or []
    if not dados:
        st.error("Usuário não encontrado.")
        return

    nome, email, wa, tipo = dados[0][0], dados[0][1], dados[0][2], dados[0][3]

    st.subheader("📋 Seus dados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nome", nome)
    col2.metric("Perfil", tipo)
    col3.metric("WhatsApp", wa or "—")
    st.caption(f"Login: {email}")

    st.divider()

    # Atualizar dados básicos
    with st.expander("✏️ Atualizar dados"):
        with st.form("form_dados"):
            novo_nome = st.text_input("Nome", value=nome)
            novo_wa   = st.text_input("WhatsApp", value=wa or "",
                                      placeholder="11 9 9999-9999")
            salvar = st.form_submit_button("💾 Salvar", type="primary")
        if salvar:
            execute_write("UPDATE usuario SET nome=%s, whatsapp=%s WHERE usuario_id=%s",
                          (novo_nome.strip(), novo_wa.strip() or None, uid))
            st.success("✅ Dados atualizados!")
            st.rerun()

    st.divider()

    # Trocar senha
    st.subheader("🔑 Alterar senha")
    with st.form("form_senha"):
        senha_atual  = st.text_input("Senha atual", type="password", key="sc_atual")
        nova_senha   = st.text_input("Nova senha", type="password", key="sc_nova",
                                     help="Mínimo 6 caracteres")
        confirmar    = st.text_input("Confirmar nova senha", type="password", key="sc_conf")
        alterar      = st.form_submit_button("🔑 Alterar senha", type="primary")

    if alterar:
        if not senha_atual or not nova_senha or not confirmar:
            st.error("Preencha todos os campos.")
        elif len(nova_senha) < 6:
            st.error("A nova senha deve ter pelo menos 6 caracteres.")
        elif nova_senha != confirmar:
            st.error("A nova senha e a confirmação não coincidem.")
        else:
            # Verifica senha atual
            ok = query("""SELECT 1 FROM usuario
                WHERE usuario_id=%s AND senha_hash=%s""",
                (uid, _hash(senha_atual))) or []
            if not ok:
                st.error("❌ Senha atual incorreta.")
            else:
                execute_write("UPDATE usuario SET senha_hash=%s WHERE usuario_id=%s",
                              (_hash(nova_senha), uid))
                # Invalida todos os tokens para forçar novo login
                execute_write("UPDATE sessao_token SET ativo=0 WHERE usuario_id=%s", (uid,))
                st.success("✅ Senha alterada com sucesso! Faça login novamente.")
                # Limpa sessão
                for k in ["auth_ok", "auth_user", "_pepper_token"]:
                    st.session_state.pop(k, None)
                st.query_params.clear()
                st.rerun()

    st.divider()

    # Esqueci minha senha (via ADM)
    with st.expander("🆘 Esqueci minha senha"):
        st.info(
            "Se você esqueceu sua senha atual, solicite ao administrador "
            "que redefina sua senha em **Configuração → Usuários**.\n\n"
            "O administrador gerará uma nova senha temporária e enviará "
            "via WhatsApp para você."
        )
        if wa:
            st.caption(f"Seu WhatsApp cadastrado: {wa}")
        else:
            st.caption("⚠️ Você não tem WhatsApp cadastrado. "
                       "Peça ao ADM para cadastrar em Configuração → Usuários.")
