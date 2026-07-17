"""
attempts_store.py — Controla o número de tentativas de avaliação por usuário.

Usa um arquivo JSON como "banco de dados" simples (não usar session_state puro:
ele reseta se o aluno fechar a aba ou recarregar a página, o que permitiria
tentativas infinitas). O arquivo persiste enquanto a instância do Streamlit
estiver no ar.

Se o app for reiniciado/redeployado no Streamlit Community Cloud, o arquivo
volta a zero — no ambiente gratuito o disco não é permanente entre deploys.
Se isso for um problema, o professor pode zerar/editar attempts.json manualmente,
ou trocar este módulo por uma planilha do Google Sheets / banco externo.
"""

import json
import os
import threading

ATTEMPTS_FILE = os.path.join(os.path.dirname(__file__), "attempts.json")
MAX_ATTEMPTS = 2

_lock = threading.Lock()


def _load() -> dict:
    if not os.path.exists(ATTEMPTS_FILE):
        return {}
    with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save(data: dict) -> None:
    with open(ATTEMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def attempts_used(username: str) -> int:
    with _lock:
        data = _load()
    return data.get(username, 0)


def attempts_remaining(username: str) -> int:
    return max(0, MAX_ATTEMPTS - attempts_used(username))


def has_attempts_left(username: str) -> bool:
    return attempts_remaining(username) > 0


def register_attempt(username: str) -> int:
    """Consome uma tentativa e retorna o total já usado após o registro."""
    with _lock:
        data = _load()
        data[username] = data.get(username, 0) + 1
        _save(data)
        return data[username]


def reset_attempts(username: str) -> None:
    """Utilitário para o professor zerar as tentativas de um grupo específico."""
    with _lock:
        data = _load()
        data.pop(username, None)
        _save(data)
