from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, diff, sympify
import numpy as np

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
        expressao = sympify(equacao)
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
