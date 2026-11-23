from app.llm import get_llm

llm = get_llm()
resposta = llm.invoke("Em uma frase, explique o que é um AI Engineer.")
print(resposta.text)
print("Tokens:", resposta.usage_metadata)

