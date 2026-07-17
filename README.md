# Agente Validador de Campanhas — Aula 2

Aplicação Streamlit + Gemini para validar as campanhas (Voz de Interação) que os alunos
produzem a partir do framework **P-C-R-F-I**, com base no ponto de atrito identificado
pelos **4 As de Raimar Richers** e ancoradas nos **4 Cs de Martha Gabriel**.

## Arquivos

- `companies_data.py` — base das 10 empresas fictícias (mesmo conteúdo do documento `empresas_ficticias.md`, em formato Python).
- `evaluator.py` — back-end: monta o prompt de avaliação e chama a API do Gemini.
- `app.py` — front-end Streamlit.
- `requirements.txt` — dependências.
- `secrets.toml.example` — modelo de arquivo de segredo para a chave do Gemini.

## Como executar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Opção A: variável de ambiente
export GEMINI_API_KEY="sua_chave_aqui"

# Opção B: arquivo de secrets do Streamlit
mkdir -p .streamlit
cp secrets.toml.example .streamlit/secrets.toml
# edite .streamlit/secrets.toml com sua chave

streamlit run app.py
```

Se preferir, a chave também pode ser colada diretamente no campo da barra lateral do app —
útil para deixar o link público e cada aluno/grupo usar a chave fornecida por você.

## Como publicar no Streamlit Community Cloud

1. Suba os arquivos deste projeto em um repositório GitHub.
2. Em [share.streamlit.io](https://share.streamlit.io), crie um novo app apontando para `app.py`.
3. Em **Settings → Secrets**, adicione:
   ```toml
   GEMINI_API_KEY = "sua_chave_aqui"
   ```
4. Compartilhe o link público com os alunos.

## Obtendo a chave de API do Gemini

1. Acesse https://aistudio.google.com/apikey
2. Crie uma chave gratuita (há cota gratuita para uso educacional/teste).
3. Cole a chave na barra lateral do app, na variável de ambiente ou no `secrets.toml`.

## Personalizações rápidas

- **Trocar o modelo:** altere o campo "Modelo Gemini" na barra lateral, ou o valor padrão
  `DEFAULT_MODEL_NAME` em `evaluator.py`, caso sua conta tenha acesso a outra versão.
- **Ajustar o rigor da avaliação:** o critério de avaliação (P-C-R-F-I + 4 Cs + 4 As) está
  todo em `SYSTEM_INSTRUCTIONS`, dentro de `evaluator.py` — pode ser editado livremente sem
  tocar no front-end.
- **Adicionar/editar empresas:** basta alterar o dicionário `COMPANIES` em `companies_data.py`.
