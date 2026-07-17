"""
auth.py — Tela de login simples com usuários/senhas pré-definidos.

Edite o dicionário USERS abaixo para trocar os 6 usuários/senhas dos grupos.
Nada aqui depende do restante do app: pode ser testado isoladamente.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Usuários pré-definidos (edite livremente antes da aula).
# Em produção real trocaríamos por hash de senha, mas para uso em sala,
# com 6 grupos fixos, texto puro é suficiente e mais simples de administrar.
# ---------------------------------------------------------------------------
USERS = {
    "grupo1": "senai2026-g1",
    "grupo2": "senai2026-g2",
    "grupo3": "senai2026-g3",
    "grupo4": "senai2026-g4",
    "grupo5": "senai2026-g5",
    "grupo6": "senai2026-g6",
}


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def current_user() -> str | None:
    return st.session_state.get("username")


def logout() -> None:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None


def render_login() -> None:
    """Renderiza a tela de login. Interrompe a execução do app (st.stop())
    até que o usuário informe credenciais válidas."""
    st.title("🔐 Acesso ao Agente Validador")
    st.write("Informe o usuário e a senha do seu grupo (fornecidos pelo professor).")

    with st.form("login_form"):
        username = st.text_input("Usuário").strip().lower()
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

    if submitted:
        if USERS.get(username) == password and password != "":
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

    st.stop()


def require_login() -> str:
    """Chame no topo do app.py. Retorna o username autenticado,
    ou interrompe a execução mostrando a tela de login."""
    if not is_authenticated():
        render_login()
    return current_user()
