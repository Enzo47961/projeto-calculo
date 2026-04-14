from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, diff, sympify, solve
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application)
import numpy as np
from sympy import integrate
from sympy import limit
from sympy import latex

transformations = standard_transformations + (implicit_multiplication_application,)

app = FastAPI()

# --- ESSAS LINHAS LIBERAM O ACESSO ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que qualquer site acesse (ideal para teste)
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------

@app.get("/resolver/{equacao}")
def resolver_derivada(equacao: str):
    try:
        x = symbols('x')
        equacao = equacao.replace("^", "**")
        expressao = parse_expr(equacao, transformations=transformations)
        derivada = diff(expressao, x)

        # gera valores para o gráfico
        f = lambda val: float(expressao.subs(x, val))
        df = lambda val: float(derivada.subs(x, val))

        x_vals = np.linspace(-10, 10, 100)
        y_vals = [f(val) for val in x_vals]
        y_deriv = [df(val) for val in x_vals]

        return {
            "status": "sucesso",
            "original": latex(expressao),
            "derivada": latex(derivada),
            "x": list(x_vals),
            "y": y_vals,
            "y_deriv": y_deriv
        }

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    
@app.get("/integrar/{equacao}")
def resolver_integral(equacao: str):
    try:
        x = symbols('x')

        equacao = equacao.replace("^", "**")
        expressao = parse_expr(equacao, transformations=transformations)

        resultado = integrate(expressao, x)

        return {
            "status": "sucesso",
            "original": latex(expressao),
            "resultado": latex(resultado)
        }

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    
@app.get("/limite")
def resolver_limite(equacao: str, ponto: str):
    try:
        x = symbols('x')

        equacao = equacao.replace("^", "**")
        expressao = parse_expr(equacao, transformations=transformations)

        from sympy import simplify
        expressao = simplify(expressao)

        ponto = sympify(ponto)

        resultado = limit(expressao, x, ponto)

        return {
            "status": "sucesso",
            "original": latex(expressao),
            "resultado": latex(resultado)
        }

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/explorar/{equacao}")
def explorar(equacao: str):
    try:
        x = symbols('x')

        equacao = equacao.replace("^", "**")
        expressao = parse_expr(equacao, transformations=transformations)

        # 1. derivada e segunda derivada
        f1 = diff(expressao, x)
        f2 = diff(f1, x)

        # 3. pontos críticos (f'(x)=0)
        criticos = solve(f1, x)

         # 2. raízes da função
        raizes = solve(expressao, x)

        # 👇 ADICIONE ISSO AQUI
        raizes_num = [float(r.evalf()) for r in raizes if r.is_real]

        # 4. classificação (máx / mín)
        classificacao = []

        for p in criticos:
            val = f2.subs(x, p)

            if val > 0:
                classificacao.append("mínimo")
            elif val < 0:
                classificacao.append("máximo")
            else:
                classificacao.append("indefinido")

        pontos_criticos = [
            {
                "x": float(p.evalf()),
                "y": float(expressao.subs(x, p).evalf())
            }
            for p in criticos if p.is_real
        ]

        # 6. gráfico base
        f = lambda val: float(expressao.subs(x, val))

        x_vals = np.linspace(-10, 10, 200)
        y_vals = [f(val) for val in x_vals]

        return {
            "status": "sucesso",

            "funcao": latex(expressao),
            "derivada": latex(f1),
            "segunda_derivada": latex(f2),

            "raizes": [latex(r) for r in raizes],
            "raizes_num": raizes_num,
            "criticos": [latex(c) for c in criticos],

            "pontos_criticos": pontos_criticos,

            "classificacao": classificacao,

            "x": list(x_vals),
            "y": y_vals
        }

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}