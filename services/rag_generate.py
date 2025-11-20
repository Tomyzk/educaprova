import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.rag_index import buscar_similares
from openai import OpenAI

# CHAVE DIRETO NO CÓDIGO POR ENQUANTO 
client = OpenAI(
    api_key="MINHA CHAVE" 
)

GEN_MODEL = "gpt-4o-mini" 

PROMPT_SYS = """
Você é um gerador de questões de concurso de múltipla escolha.

REGRAS OBRIGATÓRIAS DO FORMATO:
- Responda SEMPRE em JSON VÁLIDO.
- Estrutura exata: {"questoes": [ { ... }, { ... } ]}
- Cada objeto dentro de "questoes" DEVE ter:
  - "enunciado": string com o enunciado completo da questão.
  - "alternativas": array com EXATAMENTE 5 strings.
      * Cada string é a frase COMPLETA da alternativa.
      * NÃO use apenas "A", "B", "C", "D", "E".
      * NÃO coloque a letra no texto (nada de "A) ...", "B) ...").
      * Apenas o texto da alternativa, por exemplo:
        "É um direito fundamental previsto no artigo X da Constituição..."
  - "correta": string com UMA letra entre "A", "B", "C", "D" ou "E".
  - "comentario": explicação textual da resposta correta.
- Não coloque nenhum texto fora do JSON.
- Não repita exatamente o mesmo enunciado ou comentário em várias questões.
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


# TESTE RÁPIDO PELO TERMINAL
if __name__ == "__main__":
    resultado = gerar_prova(tema="Direito Constitucional", qtd=3, dificuldade="médio")
    print(resultado)
