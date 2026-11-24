from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm

SYSTEM = """Você é um revisor técnico sénior.
<regras>
- Responda em português, em no máximo 5 tópicos.
- Cada tópico começa com um verbo no imperativo.
- Se o código estiver correto, diga apenas "Sem problemas relevantes".
</regras>"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("human", "Reveja este código:\n<codigo>\n{codigo}\n</codigo>"),
])
chain = prompt | get_llm()

codigo = '''
def media(xs):
    return sum(xs) / len(xs)
'''
print(chain.invoke({"codigo": codigo}).text)
