from collections import Counter
from app.llm import get_llm

prompt = "Sugira um nome curto para uma startup angolana de logística. Responda só com o nome."
for t in [0.0, 0.7, 1.2]:
    llm = get_llm(temperature=t)
    nomes = [llm.invoke(prompt).text.strip() for _ in range(8)]
    print(f"temperature={t}: {len(set(nomes))} nomes distintos -> {Counter(nomes).most_common(3)}")
