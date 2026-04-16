from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, diff, sympify, solve, simplify, integrate, limit, latex
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application)
import numpy as np
import os

def safe_eval(expr, x, val):
    try:
        result = expr.subs(x, val).evalf()

        if result.is_real and result.is_finite:
            return float(result)

        return None  # ❗ JSON safe

    except:
        return None

transformations = standard_transformations + (implicit_multiplication_application,)

app = FastAPI()

# --- ESSAS LINHAS LIBERAM O ACESSO ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------
def limpar_equacao(equacao: str):
    return equacao.lower() \
        .replace("sen", "sin") \
        .replace("tg", "tan") \
        .replace("cossec", "csc") \
        .replace("cotg", "cot") \
        .replace("^", "**")



@app.get("/resolver")
def resolver_derivada(equacao: str):
    try:
        x = symbols('x')
        equacao = limpar_equacao(equacao) 
        expressao = parse_expr(equacao, transformations=transformations)
        derivada = diff(expressao, x)

        # gera valores para o gráfico
        f = lambda val: safe_eval(expressao, x, val)
        df = lambda val: safe_eval(derivada, x, val)

        x_vals = np.linspace(-10, 10, 100)
        y_vals = [f(val) for val in x_vals]
        y_deriv = [df(val) for val in x_vals]

        # 🔥 FILTRAR VALORES AQUI
        x_clean = []
        y_clean = []
        y_deriv_clean = []

        for xi, yi, ydi in zip(x_vals, y_vals, y_deriv):
            if yi is not None and ydi is not None:
                x_clean.append(xi)
                y_clean.append(yi)
                y_deriv_clean.append(ydi)

        original_latex = latex(expressao).replace(r'\log', r'\ln')
        derivada_latex = latex(derivada).replace(r'\log', r'\ln')

        return {
            "status": "sucesso",
            "original": original_latex,
            "derivada": derivada_latex,
            "x": x_clean,
            "y": y_clean,
            "y_deriv": y_deriv_clean
        }

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    
@app.get("/integrar")
def resolver_integral(equacao: str, a: str = None, b: str = None):
    try:
        x = symbols('x')

        equacao = limpar_equacao(equacao) 
        expressao = parse_expr(equacao, transformations=transformations)

        # Se a e b existirem e não forem vazios, faz a definida
        if a and b and a.strip() != "" and b.strip() != "":
            resultado = integrate(expressao, (x, sympify(a), sympify(b)))
        else:
            # Senão, faz a indefinida
            resultado = integrate(expressao, x)

        resultado_latex = latex(resultado).replace(r'\log', r'\ln')
        original_latex = latex(expressao).replace(r'\log', r'\ln')

        return {
            "status": "sucesso",
            "original": original_latex,
            "resultado": resultado_latex
        }

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    
@app.get("/limite")
def resolver_limite(equacao: str, ponto: str):
    try:
        x = symbols('x')

        equacao = limpar_equacao(equacao) 
        expressao = parse_expr(equacao, transformations=transformations)

        from sympy import simplify
        expressao = simplify(expressao)

        ponto = sympify(ponto)

        resultado = limit(expressao, x, ponto)

        original_latex = latex(expressao).replace(r'\log', r'\ln')
        resultado_latex = latex(resultado).replace(r'\log', r'\ln')

        return {
            "status": "sucesso",
            "original": original_latex,
            "resultado": resultado_latex
        }

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/explorar")
def explorar(equacao: str):
    try:
        x = symbols('x')

        equacao = limpar_equacao(equacao) 
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
        f = lambda val: safe_eval(expressao, x, val)

        x_vals = np.linspace(-10, 10, 200)
        y_vals = [f(val) for val in x_vals]

        return {
            "status": "sucesso",

            "funcao": latex(expressao).replace(r'\log', r'\ln'),
            "derivada": latex(f1).replace(r'\log', r'\ln'),
            "segunda_derivada": latex(f2).replace(r'\log', r'\ln'),

            "raizes": [latex(r).replace(r'\log', r'\ln') for r in raizes],
            "raizes_num": raizes_num,
            "criticos": [latex(c).replace(r'\log', r'\ln') for c in criticos],

            "pontos_criticos": pontos_criticos,

            "classificacao": classificacao,

            "x": list(x_vals),
            "y": y_vals
        }


    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    # O Render define a porta automaticamente na variável PORT
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
