import time
from app.llm import get_llm

MODELOS = [
    # "google_genai:gemini-3.8-flash",
    "groq:openai/gpt-oss-120b",
    "ollama:qwen3:8b",
]
PROMPT = "Liste 3 riscos de colocar um chatbot em produção sem testes."

for m in MODELOS:
    llm = get_llm(m)
    t0 = time.perf_counter()
    r = llm.invoke(PROMPT)
    dt = time.perf_counter() - t0
    print(f"\n=== {m} ({dt:.2f}s, {r.usage_metadata.get('total_tokens')} tokens) ===")
    print(r.text)
