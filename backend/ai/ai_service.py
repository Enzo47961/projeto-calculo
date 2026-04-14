from openai import OpenAI
from .prompts import (
    prompt_derivada,
    prompt_integral,
    prompt_limite,
    prompt_explorar
)

client = OpenAI(api_key="SUA_API_KEY_AQUI")


def gerar_explicacao(tipo, dados):

    if tipo == "derivada":
        prompt = prompt_derivada(
            dados["expressao"],
            dados["resultado"]
        )

    elif tipo == "integral":
        prompt = prompt_integral(
            dados["expressao"],
            dados["resultado"]
        )

    elif tipo == "limite":
        prompt = prompt_limite(
            dados["expressao"],
            dados["ponto"],
            dados["resultado"]
        )

    elif tipo == "explorar":
        prompt = prompt_explorar(
            dados["funcao"],
            dados["derivada"],
            dados["segunda_derivada"],
            dados["pontos_criticos"],
            dados["classificacao"]
        )

    else:
        return "Tipo não suportado"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Você é um professor de matemática didático."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content