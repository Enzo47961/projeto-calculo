📊 Calcly - Calculadora de Cálculo com FastAPI + Frontend
Projeto web que resolve e visualiza conceitos de Cálculo Diferencial e Integral.

## 🌍 Link do Projeto

Acesse agora: https://projeto-calculo.vercel.app/

🚀 Tecnologias usadas

Backend
FastAPI: Framework web moderno e rápido.
SymPy: Biblioteca para matemática simbólica (o "cérebro" dos cálculos).
NumPy: Para processamento numérico dos gráficos.
Uvicorn: Servidor ASGI para rodar o backend.

Frontend
HTML5/CSS3: Interface responsiva e moderna.
JavaScript (Vanilla): Lógica de integração e manipulação do DOM.
Plotly.js: Renderização de gráficos interativos.
MathJax: Exibição de fórmulas matemáticas elegantes (LaTeX).

⚙️ Como rodar o projeto localmente

1. Clone o repositório
   bash
   git clone https://github.com
   cd projeto-calculo
   Use o código com cuidado.

2. Prepare o ambiente
   bash

# Criar ambiente virtual

python -m venv .venv

# Ativar (Windows)

.venv\Scripts\activate

# Instalar dependências

pip install -r backend/requirements.txt
Use o código com cuidado.

3. Rode o backend
   bash
   uvicorn backend.main:app --reload
   Use o código com cuidado.
   O servidor estará em: http://127.0.0.1:8000

4. Rode o frontend
   Abra o arquivo frontend/index.html diretamente no navegador ou use a extensão Live Server do VS Code.

📡 Endpoints da API
Derivada: GET /resolver?equacao=x^2
Integral: GET /integrar?equacao=x^2&a=0&b=5 (suporta definida e indefinida)
Limite: GET /limite?equacao=x^2&ponto=2
Exploração: GET /explorar?equacao=x^2

📈 Exemplos de Entrada Suportados
O sistema aceita notação matemática comum graças à limpeza automática de strings:
x^2 + 5x
sen(x)/x
e^(x^2) * cos(3*x)
sqrt(x)

👨‍💻 Autor
Enzo Ferrara
Projeto educacional focado em automação de cálculo e visualização de dados matemáticos.
