# 📊 Calcly - Calculadora de Cálculo com FastAPI + Frontend

Projeto web que resolve e visualiza conceitos de Cálculo Diferencial e Integral, incluindo:

- Derivadas
- Integrais
- Limites
- Análise de funções (raízes, pontos críticos, máximos e mínimos)
- Gráficos interativos

---

## 🚀 Tecnologias usadas

### Backend

- FastAPI
- SymPy
- NumPy
- Uvicorn

### Frontend

- HTML5
- CSS3
- JavaScript
- Plotly.js
- MathJax

---

## ⚙️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/calcly.git
cd calcly
```

2. Crie o ambiente virtual
   python -m venv .venv

Ative:

Windows:

.venv\Scripts\activate

3. Instale as dependências
   pip install -r requirements.txt

4. Rode o backend

Entre na pasta backend:

cd backend
uvicorn main:app --reload

Servidor:

http://127.0.0.1:8000 5. Rode o frontend

Abra o arquivo:

frontend/index.html

Ou use Live Server no VSCode.

📡 Endpoints da API
Derivada
GET /resolver/{equacao}

Integral
GET /integrar/{equacao}

Limite
GET /limite?equacao=...&ponto=...

Exploração de função
GET /explorar/{equacao}

📈 Exemplo de entrada
x^2 + 5x
sin(x)/x
(e^(x^2) * cos(3*x)) / ln(x^2 + 1)

⚠️ Observações
Use ^ para potências (convertido automaticamente para \*\*)
Algumas funções precisam de forma compatível com SymPy (exp, ln, etc.)

👨‍💻 Autor

Enzo Ferrara

Projeto educacional focado em cálculo e visualização matemática.
