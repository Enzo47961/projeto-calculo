async function calcular() {
    const equacao = document.getElementById('equacao').value;
    const divResultado = document.getElementById('resultado');
    
    if (!equacao) {
        alert("Digite uma equação!");
        return;
    }

    divResultado.innerText = "Calculando...";

    try {
        const resposta = await fetch(
            `http://127.0.0.1:8000/resolver/${encodeURIComponent(equacao)}`
        );

        const dados = await resposta.json();

        if (dados.status === "sucesso") {

            divResultado.innerHTML = 
            `f(x) = \\(${dados.original}\\)<br>
            f'(x) = \\(${dados.derivada}\\)`;
            MathJax.typesetPromise([divResultado]);

            const trace1 = {
                x: dados.x,
                y: dados.y,
                mode: 'lines',
                name: 'f(x)'
            };

            const trace2 = {
                x: dados.x,
                y: dados.y_deriv,
                mode: 'lines',
                name: "f'(x)"
            };

            const layout = {
                title: "Função e Derivada"
            };

            Plotly.newPlot('grafico', [trace1, trace2], layout);
            

        } else {
            divResultado.innerHTML = 
                `<span style="color: red;">Erro: ${dados.mensagem}</span>`;
        }

    } catch (erro) {
        divResultado.innerHTML = 
            `<span style="color: red;">Erro ao conectar com o servidor.</span>`;
    }
}

async function integrar() {
    const equacao = document.getElementById('equacao').value;
    const divResultado = document.getElementById('resultado');

    document.getElementById('grafico').innerHTML = "";

    if (!equacao) {
        alert("Digite uma equação!");
        return;
    }

    divResultado.innerText = "Calculando...";

    try {
        const resposta = await fetch(
            `http://127.0.0.1:8000/integrar/${encodeURIComponent(equacao)}`
        );

        const dados = await resposta.json();

        if (dados.status === "sucesso") {

            divResultado.innerHTML = 
            `\\(\\int f(x)dx = ${dados.resultado}\\)`;
            MathJax.typesetPromise([divResultado]);
        } else {
            divResultado.innerHTML = 
                `<span style="color: red;">Erro: ${dados.mensagem}</span>`;
        }

    } catch (erro) {
        divResultado.innerHTML = 
            `<span style="color: red;">Erro ao conectar com o servidor.</span>`;
    }
}

async function calcularLimite() {
    const equacao = document.getElementById('equacao').value;
    const ponto = document.getElementById('ponto').value;
    const divResultado = document.getElementById('resultado');

    document.getElementById('grafico').innerHTML = "";

    if (!equacao || !ponto) {
        alert("Digite a equação e o ponto!");
        return;
    }

    divResultado.innerText = "Calculando...";

    try {
        const resposta = await fetch(`http://127.0.0.1:8000/limite?equacao=${encodeURIComponent(equacao)}&ponto=${ponto}`)

        const dados = await resposta.json();

        if (dados.status === "sucesso") {
            
            divResultado.innerHTML =
            `\\(\\lim_{x \\to ${ponto}} f(x) = ${dados.resultado}\\)`;
            MathJax.typesetPromise([divResultado]);
        } else {
            divResultado.innerHTML =
                `<span style="color: red;">Erro: ${dados.mensagem}</span>`;
        }

    } catch (erro) {
        divResultado.innerHTML =
            `<span style="color: red;">Erro ao conectar com o servidor.</span>`;
    }
}