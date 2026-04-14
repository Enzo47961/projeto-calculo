def prompt_derivada(expr, resultado):
    return f"""
Você é um professor de matemática claro e didático.

Explique passo a passo como calcular a derivada da função abaixo.

Função:
{expr}

Resultado já calculado:
{resultado}

Regras:
- Explique passo a passo
- Mostre quais regras foram usadas (ex: regra da potência)
- Seja simples e direto
- Não pule etapas importantes
- Não invente contas além do necessário

Formato da resposta:

Passo 1:
Passo 2:
Passo 3:

Resultado final:
"""

def prompt_integral(expr, resultado):
    return f"""
Você é um professor de matemática.

Explique passo a passo como calcular a integral da função abaixo.

Função:
{expr}

Resultado já calculado:
{resultado}

Regras:
- Explique de forma didática
- Indique a regra usada (ex: regra da potência, integral básica)
- Não complique desnecessariamente
- Não invente métodos avançados

Formato:

Passo 1:
Passo 2:
Passo 3:

Resultado final:
"""

def prompt_limite(expr, ponto, resultado):
    return f"""
Você é um professor de matemática.

Explique como calcular o limite abaixo:

lim x → {ponto} de {expr}

Resultado já calculado:
{resultado}

Regras:
- Explique o raciocínio
- Diga se foi substituição direta ou indeterminação
- Se houver indeterminação, explique como resolver (ex: simplificação)
- Seja claro e direto

Formato:

Passo 1:
Passo 2:
Passo 3:

Conclusão:
"""

def prompt_explorar(funcao, derivada, segunda_derivada, pontos_criticos, classificacao):
    return f"""
Você é um professor de cálculo.

Analise a função abaixo e explique o comportamento dela de forma clara.

Função:
{funcao}

Derivada:
{derivada}

Segunda derivada:
{segunda_derivada}

Pontos críticos:
{pontos_criticos}

Classificação:
{classificacao}

Explique:

- Onde a função cresce
- Onde decresce
- Onde existem máximos e mínimos
- O que a concavidade indica

Regras:
- Não use linguagem muito técnica
- Seja didático
- Explique como se estivesse ensinando um aluno

Formato:

Crescimento e decrescimento:
...

Máximos e mínimos:
...

Concavidade:
...

Resumo final:
"""