# AI Engineering Foundations — Repositório do curso

Repositório prático do curso **AI Engineering Foundations: RAG + Agents + Production (2026)**.

Este projeto começa no **Módulo 0** como um ambiente-base reprodutível para chamar LLMs de vários fornecedores com uma única interface e cresce, módulo a módulo, até um assistente de IA com RAG, agentes LangGraph e deploy em produção.

> **Estado atual:** Módulo 0 concluído (ambiente, fábrica de modelos, comparação de modelos, tracing).

---

## Índice

- [Objetivo](#objetivo)
- [Stack](#stack)
- [Pré-requisitos](#pré-requisitos)
- [Instalação rápida](#instalação-rápida)
- [Configuração do `.env`](#configuração-do-env)
- [Como executar](#como-executar)
- [Trocar de modelo](#trocar-de-modelo)
- [Modelo local com Ollama (opcional)](#modelo-local-com-ollama-opcional)
- [Usar no Google Colab](#usar-no-google-colab)
- [Observabilidade com LangSmith](#observabilidade-com-langsmith)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Segurança](#segurança)
- [Resolução de problemas](#resolução-de-problemas)
- [Roadmap](#roadmap)
- [Autor](#autor)

---

## Objetivo

- Ter um projeto Python **reprodutível**: qualquer pessoa clona e executa em menos de 5 minutos.
- Chamar LLMs de **fornecedores diferentes** (Gemini, Groq, Ollama…) mudando apenas uma variável de ambiente.
- Manter **segredos fora do código** e fora do Git.
- Ter **tracing desde o primeiro dia** para ver prompt, resposta, tokens e latência de cada chamada.

## Stack

| Camada | Ferramenta |
|---|---|
| Linguagem | Python 3.12 |
| Ambiente e dependências | [uv](https://docs.astral.sh/uv/) |
| Abstração de modelos | LangChain 1.x (`init_chat_model`) |
| Orquestração (módulos seguintes) | LangGraph 1.x |
| Modelos | Google Gemini API, Groq, Ollama (local) |
| Observabilidade | LangSmith |
| Qualidade de código | ruff, pytest |

## Pré-requisitos

- **Git**
- **uv**
  ```bash
  # macOS / Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Windows (PowerShell)
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- Pelo menos **uma chave de API gratuita**:
  - Gemini: [Google AI Studio](https://aistudio.google.com/) → *Get API key*
  - Groq: [GroqCloud Console](https://console.groq.com/) → *API Keys*
- (Opcional) Conta no [LangSmith](https://smith.langchain.com/) para tracing
- (Opcional) [Ollama](https://ollama.com/download) para modelos locais

O uv instala o Python 3.12 automaticamente se ele não existir na máquina.

## Instalação rápida

```bash
git clone https://github.com/<seu-utilizador>/ai-eng-foundations.git
cd ai-eng-foundations

uv sync                 # cria .venv e instala as versões exatas do uv.lock
cp .env.example .env    # Windows (PowerShell): Copy-Item .env.example .env
```

Abra o `.env`, preencha as chaves e execute:

```bash
uv run python hello_llm.py
```

## Configuração do `.env`

O ficheiro `.env.example` (versionado) lista as variáveis necessárias. O `.env` (com os valores reais) **nunca** vai para o Git.

```bash
# Modelo usado por omissão, no formato fornecedor:modelo
LLM_MODEL=google_genai:gemini-2.5-flash

# Chaves dos fornecedores (preencha pelo menos a do modelo escolhido)
GOOGLE_API_KEY=
GROQ_API_KEY=
HF_TOKEN=

# Tracing (opcional, recomendado)
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=ai-eng-foundations
```

> Os nomes dos modelos mudam com frequência. Confirme o modelo atual no site do fornecedor e ajuste `LLM_MODEL`.

## Como executar

### 1. Primeira chamada a um LLM

```bash
uv run python hello_llm.py
```

Saída esperada: uma frase gerada pelo modelo e o dicionário de tokens:

```text
Um AI Engineer projeta, avalia e coloca em produção sistemas baseados em modelos de linguagem.
Tokens: {'input_tokens': 14, 'output_tokens': 21, 'total_tokens': 35}
```

### 2. Comparar modelos

Envia o mesmo prompt a vários modelos e mostra resposta, latência e tokens:

```bash
uv run python -m scripts.compare_models
```

```text
=== google_genai:gemini-2.5-flash (1.84s, 312 tokens) ===
...
=== groq:llama-3.3-70b-versatile (0.61s, 287 tokens) ===
...
```

A lista de modelos está no topo de `scripts/compare_models.py`. Comente os modelos para os quais não tem chave.

### 3. Testes e lint

```bash
uv run ruff check .
uv run pytest -q
```

## Trocar de modelo

Todo o código obtém o modelo através de `app/llm.py`:

```python
from app.llm import get_llm

llm = get_llm()                                    # usa LLM_MODEL do .env
llm = get_llm("groq:llama-3.3-70b-versatile")      # escolhe outro modelo explicitamente
llm = get_llm(temperature=0.7)                     # muda a temperatura
```

Para trocar o modelo por omissão, mude só o `.env`:

| Fornecedor | Exemplo de `LLM_MODEL` | Pacote de integração |
|---|---|---|
| Google Gemini | `google_genai:gemini-2.5-flash` | `langchain-google-genai` |
| Groq | `groq:llama-3.3-70b-versatile` | `langchain-groq` |
| Ollama (local) | `ollama:llama3.2:3b` | `langchain-ollama` |

Para outro fornecedor suportado pelo LangChain, instale o pacote dele (`uv add langchain-<fornecedor>`) e defina a chave correspondente no `.env`.

## Modelo local com Ollama (opcional)

```bash
ollama pull llama3.2:3b
uv add langchain-ollama
```

No `.env`:

```bash
LLM_MODEL=ollama:llama3.2:3b
```

Funciona sem internet e sem chave de API. A velocidade depende do seu hardware (16 GB de RAM é confortável para modelos de 3–8B).

## Usar no Google Colab

1. No Colab, abra **Secrets** (ícone de chave) e adicione `GOOGLE_API_KEY`, `GROQ_API_KEY` e `LANGSMITH_API_KEY`, com acesso ao notebook ativado.
2. Primeira célula:
   ```python
   !pip install -q -U langchain langgraph langchain-google-genai langchain-groq
   ```
3. Segunda célula:
   ```python
   import os
   from google.colab import userdata

   for k in ["GOOGLE_API_KEY", "GROQ_API_KEY", "LANGSMITH_API_KEY"]:
       os.environ[k] = userdata.get(k)
   os.environ["LANGSMITH_TRACING"] = "true"
   os.environ["LANGSMITH_PROJECT"] = "ai-eng-foundations-colab"

   from langchain.chat_models import init_chat_model
   llm = init_chat_model("google_genai:gemini-2.5-flash", temperature=0)
   print(llm.invoke("Olá! Responda em português.").text)
   ```

O repositório local continua a ser a fonte da verdade: quando uma experiência no Colab funcionar, passe o código limpo para cá.

## Observabilidade com LangSmith

Com `LANGSMITH_TRACING=true` e a chave definida, todas as chamadas feitas via LangChain/LangGraph são registadas automaticamente.

1. Execute `uv run python hello_llm.py`.
2. Abra o LangSmith → projeto `ai-eng-foundations`.
3. No trace mais recente, veja: prompt enviado, resposta, latência e tokens.

Para desativar, use `LANGSMITH_TRACING=false`.

## Estrutura do projeto

```text
ai-eng-foundations/
├── .env.example          # variáveis necessárias (sem valores reais)
├── .gitignore
├── pyproject.toml        # dependências e configuração
├── uv.lock               # versões exatas (versionado)
├── README.md
├── hello_llm.py          # primeira chamada a um LLM
├── app/
│   ├── __init__.py
│   ├── llm.py            # get_llm(): fábrica única de modelos
│   ├── prompts/          # prompts versionados            (Módulo 1)
│   ├── rag/              # ingestão, índice, recuperação  (Módulo 2)
│   ├── agent/            # agentes LangGraph              (Módulo 3)
│   └── api/              # API FastAPI                    (Módulo 4)
├── scripts/
│   └── compare_models.py # compara modelos: resposta, latência, tokens
├── data/
│   ├── raw/              # documentos originais
│   └── processed/
├── evals/                # conjuntos e scripts de avaliação
├── notebooks/            # experiências (Colab/Jupyter)
└── tests/
```

### Ficheiros principais

**`app/llm.py`**

```python
"""Fábrica única de modelos. Troque de fornecedor mudando LLM_MODEL no .env."""
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_llm(model: str | None = None, temperature: float = 0.0, **kwargs):
    model = model or os.environ["LLM_MODEL"]
    return init_chat_model(model, temperature=temperature, **kwargs)
```

**`hello_llm.py`**

```python
from app.llm import get_llm

llm = get_llm()
resposta = llm.invoke("Em uma frase, explique o que é um AI Engineer.")

print(resposta.text)
print("Tokens:", resposta.usage_metadata)
```

**`scripts/compare_models.py`**

```python
import time
from app.llm import get_llm

MODELOS = [
    "google_genai:gemini-2.5-flash",
    "groq:llama-3.3-70b-versatile",
    # "ollama:llama3.2:3b",
]
PROMPT = "Liste 3 riscos de colocar um chatbot em produção sem testes."

for m in MODELOS:
    llm = get_llm(m)
    t0 = time.perf_counter()
    r = llm.invoke(PROMPT)
    dt = time.perf_counter() - t0
    print(f"\n=== {m} ({dt:.2f}s, {r.usage_metadata.get('total_tokens')} tokens) ===")
    print(r.text)
```

## Segurança

- O `.env` está no `.gitignore`. Antes de cada commit, confirme com `git status` que ele **não** aparece.
- Nunca coloque chaves em código, notebooks partilhados ou issues.
- Se uma chave chegar ao GitHub: **revogue-a imediatamente** no painel do fornecedor, gere uma nova e remova o ficheiro do índice (`git rm --cached .env`). Apagar o commit não chega, porque a chave já pode ter sido copiada.

`.gitignore` usado:

```gitignore
.venv/
__pycache__/
.env
data/chroma/
*.db
.ipynb_checkpoints/
.DS_Store
```

## Resolução de problemas

| Sintoma | Solução |
|---|---|
| `uv: command not found` | Feche e reabra o terminal. No Linux/macOS, `source ~/.bashrc` ou `~/.zshrc` |
| `KeyError: 'LLM_MODEL'` | O `.env` não existe ou não está na raiz. Execute os comandos a partir da raiz do projeto |
| `Unable to infer model provider` | Use o formato `fornecedor:modelo` em `LLM_MODEL` |
| `ImportError: langchain_google_genai` (ou outro) | Instale o pacote do fornecedor: `uv add langchain-google-genai` |
| `ModuleNotFoundError: No module named 'app'` | Execute scripts dentro de `scripts/` com `-m`: `uv run python -m scripts.compare_models` |
| `429` / `RESOURCE_EXHAUSTED` | Limite do plano gratuito: espere um minuto ou troque de fornecedor |
| `404 model not found` | Nome de modelo descontinuado: confirme o nome atual e atualize `LLM_MODEL` |
| Nada aparece no LangSmith | Confirme `LANGSMITH_TRACING=true`, a chave e o nome do projeto |
| Ollama: `connection refused` | Abra a aplicação Ollama ou execute `ollama serve` |

## Roadmap

| Módulo | Entrega | Estado |
|---|---|---|
| 0 | Ambiente-base, fábrica de modelos, comparação, tracing | ✅ Concluído |
| 1 | Extrator estruturado com avaliação de prompts | ⬜ |
| 2 | DocuMind: perguntas e respostas sobre documentos, com citações | ⬜ |
| 3 | Assistente de pesquisa com agentes LangGraph | ⬜ |
| 4 | API em produção: FastAPI, Docker, CI com gate de avaliação, deploy | ⬜ |
| Final | Projeto Capstone | ⬜ |

## Autor

**Eliude Quintas Francisco**, Engenheiro de Software, Luanda, Angola
[eliudefrancisco.com](https://eliudefrancisco.com)
