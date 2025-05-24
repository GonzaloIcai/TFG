const stroopPalabras = [
    { texto: "Rojo", color: "red" },
    { texto: "Azul", color: "blue" },
    { texto: "Verde", color: "green" },
    { texto: "Amarillo", color: "orange" }
];

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

    // 1. Elegimos una palabra base (texto y color coinciden)
    const base = stroopPalabras[Math.floor(Math.random() * stroopPalabras.length)];

    // 2. Creamos tres iguales
    const opciones = [
        { texto: base.texto, color: base.color },
        { texto: base.texto, color: base.color },
        { texto: base.texto, color: base.color }
    ];

    // 3. Escogemos la diferente (que tenga texto ≠ base.texto)
    let distinta;
    do {
        distinta = stroopPalabras[Math.floor(Math.random() * stroopPalabras.length)];
    } while (distinta.texto === base.texto);

    // 4. Color incorrecto ≠ texto de la palabra distinta y ≠ color de base
    const coloresDisponibles = stroopPalabras
        .map(p => p.color)
        .filter(c => c !== distinta.color && c !== base.color);

    const colorIncorrecto = coloresDisponibles[Math.floor(Math.random() * coloresDisponibles.length)];

    const opcionDiferente = {
        texto: distinta.texto,
        color: colorIncorrecto
    };

    // 5. Insertamos en posición aleatoria
    const indiceDiferente = Math.floor(Math.random() * 4);
    opciones.splice(indiceDiferente, 0, opcionDiferente);

    // 6. Renderizamos
    opciones.forEach((opcion, index) => {
        const btn = document.createElement("button");
        btn.className = "btn fs-4 m-2 px-4 py-3 border rounded shadow";
        btn.textContent = opcion.texto;
        btn.style.color = opcion.color;
        btn.style.transition = "all 0.2s ease";
        btn.onmouseover = () => btn.style.transform = "scale(1.1)";
        btn.onmouseleave = () => btn.style.transform = "scale(1)";
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
