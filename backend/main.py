from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, diff, sympify
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application)
import numpy as np
from sympy import integrate
from sympy import limit

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
            "derivada": str(derivada),
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
            "resultado": str(resultado)
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
            "resultado": str(resultado)
        }

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
