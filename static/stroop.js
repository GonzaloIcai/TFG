const colors = ["🔴", "🔵", "🟢", "🟡"];
let rondasTotales = 5;
let rondaActual = 0;
let errores = 0;
let tiempos = [];
let startTime;

function startStroop() {
    rondaActual = 0;
    errores = 0;
    tiempos = [];
    document.getElementById("feedback").textContent = "";
    document.getElementById("stroop-board").innerHTML = "";
    siguienteRonda();
}

function siguienteRonda() {
    if (rondaActual >= rondasTotales) {
        terminarJuego();
        return;
    }

    const board = document.getElementById("stroop-board");
    board.innerHTML = "";

    const simboloBase = colors[Math.floor(Math.random() * colors.length)];

    let simbolos = [simboloBase, simboloBase, simboloBase];
    let simboloDiferente;
    do {
        simboloDiferente = colors[Math.floor(Math.random() * colors.length)];
    } while (simboloDiferente === simboloBase);

    const indiceDiferente = Math.floor(Math.random() * 4);
    simbolos.splice(indiceDiferente, 0, simboloDiferente);

    simbolos.forEach((simbolo, index) => {
        const btn = document.createElement("button");
        btn.className = "btn btn-light fs-1 m-2";
        btn.textContent = simbolo;
        btn.onclick = () => verificarRespuesta(index === indiceDiferente);
        board.appendChild(btn);
    });

    startTime = Date.now();
}

function verificarRespuesta(acertado) {
    const tiempo = (Date.now() - startTime) / 1000;
    tiempos.push(tiempo);
    if (!acertado) errores++;

    rondaActual++;
    siguienteRonda();
}

function terminarJuego() {
    const promedio = tiempos.reduce((a, b) => a + b, 0) / tiempos.length;
    const feedback = `✅ Juego terminado. Errores: ${errores}, Tiempo promedio: ${promedio.toFixed(2)}s`;
    document.getElementById("feedback").textContent = feedback;

    fetch("/attention/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            average_time: promedio.toFixed(2),
            errors: errores,
            rounds_completed: rondasTotales
        })
    }).then(res => console.log("Resultado de atención guardado."));
}

document.addEventListener("DOMContentLoaded", startStroop);
