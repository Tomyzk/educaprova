import os, textwrap
from dotenv import load_dotenv
from openai import OpenAI
from .rag_index import buscar_similares

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GEN_MODEL = "gpt-4o-mini" 

PROMPT_SYS = """Você é um gerador de questões de concurso.
Siga rigorosamente o ESTILO dos exemplos fornecidos (formato, linguagem, nível).
Produza questões originais, sem copiar trechos literais.
Sempre retorne em JSON com campos: questoes: [{enunciado, alternativas: [A,B,C,D,E], correta, comentario}].
"""

def _montar_contexto(exemplos):
    blocos = []
    for i, ex in enumerate(exemplos, 1):
        t = ex["meta"]["texto"]
        blocos.append(f"### EXEMPLO {i}\n{t}")
    return "\n\n".join(blocos)

def gerar_prova(tema: str, qtd: int = 5, dificuldade: str = "médio"):
    exemplos = buscar_similares(tema, top_k=6)
    contexto = _montar_contexto(exemplos)

    user_prompt = f"""
Gere {qtd} questões de {tema} no nível {dificuldade}.
Respeite o estilo dos EXEMPLOS abaixo (formatação, enunciado, alternativas e gabarito).
Não repita as questões dos exemplos; crie novas, no mesmo estilo.

EXEMPLOS (APENAS PARA ESTILO):
{contexto}

Responda SOMENTE em JSON:
"""
    msgs = [
        {"role": "system", "content": PROMPT_SYS},
        {"role": "user", "content": user_prompt},
    ]
    resp = client.chat.completions.create(
        model=GEN_MODEL,
        messages=msgs,
        temperature=0.5,
        max_tokens=1600,
    )
    return resp.choices[0].message.content
