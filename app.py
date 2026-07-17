"""
app.py — Front-end Streamlit do Agente Validador de Campanhas.

Uso em sala:
1. O grupo escolhe a empresa que recebeu por sorteio.
2. Cola o texto da campanha (Voz de Interação) gerada a partir do prompt P-C-R-F-I.
3. Clica em "Avaliar campanha" e recebe o parecer do Agente (via Gemini).

Executar localmente:
    pip install -r requirements.txt
    streamlit run app.py

A chave de API do Gemini pode ser fornecida de duas formas:
    a) variável de ambiente / st.secrets: GEMINI_API_KEY
    b) campo de texto na barra lateral (útil para os alunos testarem com a chave do professor
       sem precisar configurar nada)
"""

import os

import streamlit as st

from companies_data import COMPANIES
from evaluator import DEFAULT_MODEL_NAME, evaluate_campaign

from auth import require_login, logout, current_user
from attempts_store import attempts_remaining, has_attempts_left, register_attempt, MAX_ATTEMPTS

st.set_page_config(
    page_title="Agente Validador de Campanhas | SENAI-SP",
    page_icon="🎯",
    layout="centered",
)

username = require_login()

# ---------------------------------------------------------------------------
# Barra lateral: configuração da API
# ---------------------------------------------------------------------------

default_key = os.environ.get("GEMINI_API_KEY", "")
try:
    default_key = st.secrets.get("GEMINI_API_KEY", default_key)  # type: ignore[attr-defined]
except Exception:
    pass  # st.secrets pode não existir se não houver secrets.toml configurado


st.sidebar.caption(
    "Curso: Marketing Digital com Inteligência Artificial — SENAI-SP\n\n"
    "Aula 2 — Ecossistema de IA e Engenharia de Prompt (P-C-R-F-I)"
)
st.sidebar.markdown('---')

st.sidebar.title("⚙️ Configuração")

st.sidebar.markdown(f"**Grupo logado:** `{username}`")
st.sidebar.markdown(f"**Tentativas restantes:** {attempts_remaining(username)} / {MAX_ATTEMPTS}")
if st.sidebar.button("Sair"):
    logout()
    st.rerun()

# ---------------------------------------------------------------------------
# Corpo principal
# ---------------------------------------------------------------------------
st.title("🎯 Agente Validador de Campanhas")
st.write(
    "Selecione a empresa que seu grupo recebeu, cole a campanha (Voz de Interação) gerada "
    "com o framework **P-C-R-F-I** e receba o parecer do Agente Validador."
)

company_name = st.selectbox(
    "Empresa sorteada para o seu grupo",
    options=list(COMPANIES.keys()),
)

company_info = COMPANIES[company_name]

with st.expander("📋 Ver briefing da empresa selecionada"):
    st.markdown(f"**Segmento:** {company_info['segmento']}")
    st.markdown(f"**Resumo do negócio:** {company_info['resumo']}")
    st.markdown(f"**Sintomas observados:** {company_info['sintomas']}")
    st.markdown(f"**Dados disponíveis:** {company_info['dados']}")

campaign_text = st.text_area(
    "Cole aqui a campanha gerada pelo seu grupo",
    height=260,
    placeholder=(
        "Ex: Prompt P-C-R-F-I completo (Persona, Contexto, Regras, Formato, Iteração) "
        "e/ou o texto final da mensagem gerada para o cliente..."
    ),
)

avaliar_clicado = st.button("🚀 Avaliar campanha", type="primary", use_container_width=True)

if avaliar_clicado:
    if not has_attempts_left(username):
        st.error("Seu grupo já usou as 2 tentativas disponíveis para esta atividade.")
    elif not default_key:
        st.error("Informe a chave de API do Gemini.")
    elif not campaign_text.strip():
        st.error("Cole o texto da campanha antes de avaliar.")
    else:
        with st.spinner("O Agente Validador está analisando a campanha..."):
            try:
                result = evaluate_campaign(
                    company_name=company_name,
                    company_info=company_info,
                    campaign_text=campaign_text,
                    api_key=default_key,
                    model_name=DEFAULT_MODEL_NAME,
                )
                register_attempt(username)
            except Exception as exc:  # noqa: BLE001 — queremos capturar qualquer erro de API/parsing
                st.error(f"Não foi possível avaliar a campanha: {exc}")
                result = None

        if result:
            st.markdown("---")
            st.subheader("📊 Resultado da avaliação")

            col1, col2 = st.columns(2)
            col1.metric("Nota geral", f"{result.nota:.1f} / 10")
            col2.metric("Classificação", result.classificacao)

            st.markdown("#### Parecer geral")
            st.info(result.parecer_geral)

            col_forte, col_fraco = st.columns(2)
            with col_forte:
                st.markdown("#### ✅ Pontos fortes")
                for item in result.pontos_fortes:
                    st.markdown(f"- {item}")
            with col_fraco:
                st.markdown("#### ⚠️ Pontos a melhorar")
                for item in result.pontos_fracos:
                    st.markdown(f"- {item}")

            st.markdown("#### 🧩 Aderência ao framework P-C-R-F-I")
            labels = {
                "persona": "Persona",
                "contexto": "Contexto",
                "regras": "Regras",
                "formato": "Formato",
                "iteracao": "Iteração",
            }
            for key, label in labels.items():
                item = result.aderencia_pcrfi.get(key)
                if item:
                    st.markdown(f"**{label} — nota {item.get('nota', '-')}/10**")
                    st.caption(item.get("comentario", ""))

            st.markdown("#### 💡 Recomendações do Agente")
            for rec in result.recomendacoes:
                st.markdown(f"- {rec}")

            with st.expander("Ver resposta bruta do modelo (depuração)"):
                st.code(result.raw_text, language="json")
