let modoAtual = "derivada";

function resetUI() {
    const divResultado = document.getElementById("resultado");
    const grafico = document.getElementById("grafico");

    divResultado.innerHTML = "";
    grafico.innerHTML = "";
}

function setModo(modo) {

    resetUI(); // 🔥 LIMPA TUDO AO TROCAR MODO

    modoAtual = modo;

    const inputPonto = document.getElementById("ponto");
    const inputA = document.getElementById("ponto_a"); // Novo
    const inputB = document.getElementById("ponto_b"); // Novo
    

    // Mostrar/esconder input de ponto
    if (modo === "limite") {
        inputPonto.style.display = "block";
    } else {
        inputPonto.style.display = "none";
    }

        // Mostrar/esconder inputs de integral (Definida)
    if (modo === "integral") {
        inputA.style.display = "block";
        inputB.style.display = "block";
    } else {
        inputA.style.display = "none";
        inputB.style.display = "none";
    }

    // 🔥 NOVO: destacar botão ativo
    const botoes = document.querySelectorAll(".modo-btn");

    botoes.forEach(btn => {
        btn.classList.remove("ativo");
    });

    botoes.forEach(btn => {
        if (btn.innerText.toLowerCase() === modo) {
            btn.classList.add("ativo");
        }
    });
}

async function calcular() {
    const equacao = document.getElementById('equacao').value;
    const divResultado = document.getElementById('resultado');
    document.getElementById('grafico').innerHTML = "";

    if (!equacao) {
        alert("Digite uma equação!");
        return;
    }

    divResultado.innerHTML = "⏳ Calculando...";

    try {
        const resposta = await fetch(
            `https://projeto-calculo.onrender.com/resolver?equacao=${encodeURIComponent(equacao)}`
        );

        const dados = await resposta.json();

        if (dados.status === "sucesso") {

            divResultado.innerHTML = `
            <div>
                <p><strong>Função:</strong></p>
                <p>\\(${dados.original}\\)</p>

                <p><strong>Derivada:</strong></p>
                <p>\\(${dados.derivada}\\)</p>
            </div>
            `;
            MathJax.typesetPromise([divResultado]);

            const trace1 = {
                x: dados.x,
                y: dados.y,
                mode: 'lines',
                name: 'f(x)',
                line: {
                    width: 3,
                    shape: 'spline'
                }
            };

            const trace2 = {
                x: dados.x,
                y: dados.y_deriv,
                mode: 'lines',
                name: "f'(x)",
                line: {
                    width: 3,
                    dash: 'dot',
                    shape: 'spline'
                }
            };

            const layout = {
                title: {
                    text: "Função e Derivada",
                    font: { color: "white" }
                },

                paper_bgcolor: "#0f0f1a",
                plot_bgcolor: "#0f0f1a",

                xaxis: {
                    gridcolor: "rgba(255,255,255,0.1)",
                    zerolinecolor: "rgba(255,255,255,0.3)",
                    color: "white"
                },

                yaxis: {
                    gridcolor: "rgba(255,255,255,0.1)",
                    zerolinecolor: "rgba(255,255,255,0.3)",
                    color: "white"
                },

                legend: {
                    font: { color: "white" }
                }
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
    const a = document.getElementById('ponto_a')?.value || ""; // Limite inferior
    const b = document.getElementById('ponto_b')?.value || ""; // Limite superior
    const divResultado = document.getElementById('resultado');

    document.getElementById('grafico').innerHTML = "";

    if (!equacao) {
        alert("Digite uma equação!");
        return;
    }

    divResultado.innerText = "Calculando...";

    try {
        const resposta = await fetch(
            `https://projeto-calculo.onrender.com/integrar?equacao=${encodeURIComponent(equacao)}&a=${a}&b=${b}`
        );

        const dados = await resposta.json();

        if (dados.status === "sucesso") {

            // Se houver limites, mostramos o símbolo da integral definida
            let simboloIntegral = (a && b) ? `\\int_{${a}}^{${b}}` : `\\int`;

            divResultado.innerHTML = `
            <div>
                <p><strong>Integral:</strong></p>
                <p>\\(\\int ${dados.original} \\, dx = ${dados.resultado}\\)</p>
            </div>
            `;
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
        const resposta = await fetch(`https://projeto-calculo.onrender.com/limite?equacao=${encodeURIComponent(equacao)}&ponto=${ponto}`)

        const dados = await resposta.json();

        if (dados.status === "sucesso") {
            
            divResultado.innerHTML = `
            <div>
                <p><strong>Limite:</strong></p>
                <p>\\(\\lim_{x \\to ${ponto}} ${dados.original} = ${dados.resultado}\\)</p>
            </div>
            `;
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

function executar() {
    if (modoAtual === "derivada") {
        calcular();
    } else if (modoAtual === "integral") {
        integrar();
    } else if (modoAtual === "limite") {
        calcularLimite();
    } else if (modoAtual === "explorar") {
        explorar();
    }
}

window.onload = () => {
    setModo("derivada");
};

async function explorar() {
    const equacao = document.getElementById('equacao').value;
    const divResultado = document.getElementById('resultado');

    document.getElementById('grafico').innerHTML = "";

    if (!equacao) {
        alert("Digite uma equação!");
        return;
    }

    divResultado.innerText = "Explorando...";

    try {
        const resposta = await fetch(
            `https://projeto-calculo.onrender.com/explorar?equacao=${encodeURIComponent(equacao)}`
        );

        const dados = await resposta.json();

        if (dados.status === "sucesso") {

            divResultado.innerHTML = `
            <div>
                <p><strong>Função:</strong> \\(${dados.funcao}\\)</p>

                <p><strong>Derivada:</strong> \\(${dados.derivada}\\)</p>

                <p><strong>Segunda derivada:</strong> \\(${dados.segunda_derivada}\\)</p>

                <p><strong>Raízes:</strong> ${dados.raizes.join(", ")}</p>

                <p><strong>Pontos críticos:</strong></p>
                <ul>
                    ${dados.pontos_criticos.map((p, i) =>
                        `<li>x = ${p.x.toFixed(3)} → ${dados.classificacao[i]}</li>`
                    ).join("")}
                </ul>
            </div>
            `;

            MathJax.typesetPromise([divResultado]);

            const trace1 = {
                x: dados.x,
                y: dados.y,
                mode: 'lines',
                name: 'f(x)',
                line: {
                    width: 3,
                    shape: 'spline'
                }
            };

            const traceCriticos = {
                x: dados.pontos_criticos.map(p => parseFloat(p.x.toFixed(3))),
                y: dados.pontos_criticos.map(p => parseFloat(p.y.toFixed(3))),
                mode: 'markers',
                name: 'Pontos críticos',
                marker: {
                    size: 10,
                    color: 'red'
                }
            };

            const traceRaizes = {
                x: dados.raizes_num,
                y: dados.raizes_num.map(() => 0),
                mode: 'markers',
                name: 'Raízes',
                marker: {
                    size: 10,
                    color: 'green'
                }
            };

            const layout = {
                title: {
                    text: "Exploração da Função",
                    font: { color: "white" }
                },
                paper_bgcolor: "#0f0f1a",
                plot_bgcolor: "#0f0f1a",
                xaxis: {
                    gridcolor: "rgba(255,255,255,0.1)",
                    zerolinecolor: "rgba(255,255,255,0.3)",
                    color: "white"
                },
                yaxis: {
                    gridcolor: "rgba(255,255,255,0.1)",
                    zerolinecolor: "rgba(255,255,255,0.3)",
                    color: "white"
                },
                legend: {
                    font: { color: "white" }
                }
            };

            Plotly.newPlot('grafico', [trace1, traceCriticos, traceRaizes], layout);

        } else {
            divResultado.innerHTML =
                `<span style="color:red;">Erro: ${dados.mensagem}</span>`;
        }

    } catch (erro) {
        divResultado.innerHTML =
            `<span style="color:red;">Erro ao conectar com servidor.</span>`;
    }
}