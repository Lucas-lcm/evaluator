"""
evaluator.py — Backend do Agente Validador de Campanhas.

Responsável por:
1. Montar o prompt de avaliação (com o contexto da empresa + a campanha do aluno);
2. Chamar a API do Gemini;
3. Interpretar a resposta e devolver um dicionário estruturado para o front-end (app.py).

Este módulo não depende do Streamlit — pode ser testado isoladamente
ou reutilizado em outro front-end no futuro.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

import google.generativeai as genai

# Modelo padrão. Ajuste aqui caso o professor tenha acesso a outra versão
# no Google AI Studio (ex.: "gemini-2.5-flash", "gemini-2.5-pro").
DEFAULT_MODEL_NAME = "gemini-3.5-flash"


@dataclass
class EvaluationResult:
    nota: float                 # 0 a 10
    classificacao: str          # "Aprovada" | "Precisa de ajustes" | "Reprovada"
    pontos_fortes: list[str]
    pontos_fracos: list[str]
    aderencia_pcrfi: dict       # avaliação de cada letra do P-C-R-F-I (0-10 + comentário)
    recomendacoes: list[str]
    parecer_geral: str
    raw_text: str                # resposta bruta do modelo (fallback/depuração)


SYSTEM_INSTRUCTIONS = """\
Você é um Diretor de Marketing sênior atuando como banca avaliadora em um curso profissional \
de Marketing Digital com Inteligência Artificial (SENAI-SP). Sua tarefa é avaliar CAMPANHAS DE \
COMUNICAÇÃO escritas por alunos, no papel de um "Agente Validador" técnico e rigoroso — mas \
educativo, nunca genérico.

Fundamente sua avaliação OBRIGATORIAMENTE nos seguintes referenciais teóricos:

1. Framework P-C-R-F-I para engenharia de prompt/voz de marca:
   - Persona: a campanha deixa claro QUEM está falando (tom, papel, posicionamento)?
   - Contexto: a campanha demonstra entendimento real do atrito/problema do cliente?
   - Regras: existem limites claros de tom, promessas e compliance (ex: não prometer o que não pode cumprir)?
   - Formato: a estrutura da mensagem é adequada ao canal (WhatsApp, e-mail, etc.) e ao público?
   - Iteração: a campanha prevê algum mecanismo de ajuste, follow-up ou personalização?

2. Os 4 Cs de Martha Gabriel (a campanha deve resolver o atrito pela ótica do cliente, não da empresa):
   - Cliente (Solução): resolve uma necessidade/desejo real, não apenas empurra produto.
   - Custo: considera o custo total de transação (não só preço, mas tempo, esforço, risco percebido).
   - Conveniência: reduz fricção de acesso.
   - Comunicação: é um diálogo de duas vias, não um monólogo publicitário.

3. Os 4 As de Raimar Richers: a campanha deve estar coerente com o ponto de atrito diagnosticado \
   (falha de Ativação ou de Adaptação) na empresa avaliada — ou seja, ela precisa atacar a causa raiz, \
   não só "vender mais".

Você receberá o perfil da empresa (segmento, sintomas de negócio e dados) e o texto da campanha \
elaborada pelo aluno. Avalie com rigor profissional (nível SENAI, aplicável ao mercado real), \
identificando se a campanha é genérica/desconectada dos dados apresentados ou se de fato ataca \
a causa raiz do atrito com posicionamento estratégico.

RESPONDA ESTRITAMENTE EM JSON VÁLIDO, sem markdown, sem crases, sem texto fora do JSON, \
seguindo exatamente este schema:

{
  "nota": <número de 0 a 10, pode ter uma casa decimal>,
  "classificacao": "<Aprovada | Precisa de ajustes | Reprovada>",
  "pontos_fortes": ["...", "..."],
  "pontos_fracos": ["...", "..."],
  "aderencia_pcrfi": {
    "persona": {"nota": <0-10>, "comentario": "..."},
    "contexto": {"nota": <0-10>, "comentario": "..."},
    "regras": {"nota": <0-10>, "comentario": "..."},
    "formato": {"nota": <0-10>, "comentario": "..."},
    "iteracao": {"nota": <0-10>, "comentario": "..."}
  },
  "recomendacoes": ["...", "..."],
  "parecer_geral": "Parágrafo curto (3-5 frases) resumindo o parecer, escrito em tom de banca avaliadora."
}
"""


def _build_user_prompt(company_name: str, company_info: dict, campaign_text: str) -> str:
    return f"""\
### Empresa avaliada: {company_name}

**Segmento:** {company_info['segmento']}

**Resumo do negócio:** {company_info['resumo']}

**Sintomas de negócio observados (pistas do atrito nos 4 As):** {company_info['sintomas']}

**Dados disponíveis:** {company_info['dados']}

---

### Campanha submetida pelo aluno (Voz de Interação gerada via P-C-R-F-I):

{campaign_text}

---

Avalie esta campanha seguindo rigorosamente as instruções de sistema e devolva APENAS o JSON.
"""


def _extract_json(raw_text: str) -> dict:
    """Extrai o primeiro bloco JSON válido da resposta do modelo,
    mesmo que ele tenha vindo com crases de markdown por engano."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned.strip())
    cleaned = re.sub(r"```$", "", cleaned.strip())
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # fallback: tenta localizar o maior bloco {...} da string
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def configure_gemini(api_key: str) -> None:
    """Configura a chave de API do Gemini para a sessão atual."""
    genai.configure(api_key=api_key)


def evaluate_campaign(
    company_name: str,
    company_info: dict,
    campaign_text: str,
    api_key: str,
    model_name: str = DEFAULT_MODEL_NAME,
) -> EvaluationResult:
    """
    Envia a campanha para o Gemini e retorna um EvaluationResult estruturado.
    Levanta exceção em caso de falha de API ou resposta fora do schema esperado
    (o front-end é responsável por capturar e exibir o erro ao usuário).
    """
    configure_gemini(api_key)

    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=SYSTEM_INSTRUCTIONS,
    )

    user_prompt = _build_user_prompt(company_name, company_info, campaign_text)

    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,  # baixa temperatura: queremos avaliação consistente, não criativa
            response_mime_type="application/json",
        ),
    )

    raw_text = response.text
    data = _extract_json(raw_text)

    return EvaluationResult(
        nota=float(data.get("nota", 0)),
        classificacao=data.get("classificacao", "Não classificada"),
        pontos_fortes=data.get("pontos_fortes", []),
        pontos_fracos=data.get("pontos_fracos", []),
        aderencia_pcrfi=data.get("aderencia_pcrfi", {}),
        recomendacoes=data.get("recomendacoes", []),
        parecer_geral=data.get("parecer_geral", ""),
        raw_text=raw_text,
    )
