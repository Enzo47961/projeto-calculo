from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, diff, sympify

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
        # Converte o texto para matemática
        expressao = sympify(equacao)
        resultado = diff(expressao, x)
        
        return {
            "status": "sucesso",
            "original": str(expressao),
            "derivada": str(resultado)
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
