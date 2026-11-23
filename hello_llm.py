from app.llm import get_llm, get_llm_local

# llm = get_llm()
# resposta = llm.invoke("Em uma frase, explique o que é um AI Engineer.")
# print(resposta.text)
# print("Tokens:", resposta.usage_metadata)

llm_local = get_llm_local()

resposta = llm_local.invoke("Em uma frase, explique o que é um AI Engineer.")
print(resposta.text)
