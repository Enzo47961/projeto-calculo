from sympy import symbols, diff

# Definimos que 'x' é a nossa variável simbólica
x = symbols('x')

# A função que queremos derivar: x ao quadrado + 5x
expressao = x**2 + 5*x

# A mágica acontece aqui:
resultado = diff(expressao, x)

print(f"A derivada de {expressao} é: {resultado}")
