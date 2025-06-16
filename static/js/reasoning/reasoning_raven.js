const ejercicios = [
    { imagen: "raven_1.png", opciones: ["a", "b", "c", "d"], correcta: "d" },
    { imagen: "raven_2.png", opciones: ["1", "2", "3", "4", "5", "6"], correcta: "4" },
    { imagen: "raven_3.png", opciones: ["a", "b", "c", "d"], correcta: "c" },
    { imagen: "raven_4.png", opciones: ["1", "2", "3", "4"], correcta: "4" },
    { imagen: "raven_5.png", opciones: ["1", "2", "3", "4", "5", "6"], correcta: "3" },
    { imagen: "raven_6.png", opciones: ["a", "b", "c", "d"], correcta: "b" },
    { imagen: "raven_7.png", opciones: ["1", "2", "3", "4", "5", "6"], correcta: "5" },
    { imagen: "raven_8.png", opciones: ["a", "b", "c", "d"], correcta: "b" },
    { imagen: "raven_9.png", opciones: ["1", "2", "3", "4", "5", "6"], correcta: "1" },
    { imagen: "raven_10.png", opciones: ["1", "2", "3", "4", "5", "6"], correcta: "5" },
    { imagen: "raven_11.png", opciones: ["1", "2", "3", "4", "5", "6"], correcta: "5" },
    { imagen: "raven_12.png", opciones: ["1", "2", "3", "4", "5", "6"], correcta: "3" }
];

let rondaActual = 0;
let rondas = [];
let aciertos = 0;
let tiempoInicio = null;

function seleccionarRondas() {
    const copia = [...ejercicios];
    for (let i = copia.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copia[i], copia[j]] = [copia[j], copia[i]];
    }
    return copia.slice(0, 4);
}

function startGame() {
    rondaActual = 0;
    aciertos = 0;
    rondas = seleccionarRondas();
    tiempoInicio = Date.now();
    mostrarRonda();
}

function mostrarRonda() {
    const ejercicio = rondas[rondaActual];
    document.getElementById("raven-image").src = `/static/img/raven/${ejercicio.imagen}`;
    document.getElementById("feedback").textContent = "";
    const opcionesDiv = document.getElementById("options-container");
    opcionesDiv.innerHTML = "";

    ejercicio.opciones.forEach(opcion => {
        const btn = document.createElement("button");
        btn.className = "btn btn-outline-dark fs-5 btn-opcion";
        btn.textContent = opcion;
        btn.onclick = () => verificarRespuesta(opcion, btn);
        opcionesDiv.appendChild(btn);
    });
}

function verificarRespuesta(seleccion, botonSeleccionado) {
    const ejercicio = rondas[rondaActual];
    const esCorrecta = seleccion === ejercicio.correcta;

    const botones = document.querySelectorAll(".btn-opcion");
    botones.forEach(btn => {
        btn.disabled = true;
        if (btn.textContent === ejercicio.correcta) {
            btn.classList.add("btn-correcta");
        } else if (btn === botonSeleccionado) {
            btn.classList.add("btn-incorrecta");
        }
    });

    if (esCorrecta) aciertos++;
    rondaActual++;

    setTimeout(() => {
        if (rondaActual < 4) {
            mostrarRonda();
        } else {
            const tiempoTotal = ((Date.now() - tiempoInicio) / 1000).toFixed(2);
            const errores = 4 - aciertos;

            document.getElementById("feedback").textContent =
                `✅ Has acertado ${aciertos} de 4 rondas.`;

            fetch("/reasoning/raven/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    correct: aciertos,
                    incorrect: errores,
                    time_spent: tiempoTotal
                })
            }).then(res => {
                if (res.ok) {
                    console.log("Resultado de razonamiento visual guardado correctamente");
                } else {
                    console.error("Error al guardar resultado");
                }
            });
        }
    }, 2000);
}

// Modal instrucciones
document.addEventListener("DOMContentLoaded", () => {
    const modal = new bootstrap.Modal(document.getElementById('instruccionesModal'));
    modal.show();

    document.getElementById("btn-iniciar").addEventListener("click", () => {
        modal.hide();
        startGame();
    });
});
