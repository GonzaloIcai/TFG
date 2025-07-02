
const stroopPalabras = [
    { texto: "Rojo", color: "red" },
    { texto: "Azul", color: "blue" },
    { texto: "Verde", color: "green" },
    { texto: "Amarillo", color: "orange" },
    { texto: "Morado", color: "purple" },
    { texto: "Rosa", color: "pink" },
    { texto: "Negro", color: "black" },
    { texto: "Gris", color: "gray" },
    { texto: "Marrón", color: "brown" },
    { texto: "Cian", color: "cyan" }
];

let rondasTotales = 5;
let rondaActual = 0;
let errores = 0;
let tiempos = [];
let startTime;
let indiceCorrectoGlobal = null;

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

    const correctas = [];
    const yaUsadas = new Set();

    while (correctas.length < 3) {
        const opcion = stroopPalabras[Math.floor(Math.random() * stroopPalabras.length)];
        if (!yaUsadas.has(opcion.texto)) {
            correctas.push({ texto: opcion.texto, color: opcion.color });
            yaUsadas.add(opcion.texto);
        }
    }

    let textoIncorrecto, colorIncorrecto;
    do {
        textoIncorrecto = stroopPalabras[Math.floor(Math.random() * stroopPalabras.length)];
        colorIncorrecto = stroopPalabras[Math.floor(Math.random() * stroopPalabras.length)];
    } while (
        textoIncorrecto.texto === colorIncorrecto.texto ||
        textoIncorrecto.color === colorIncorrecto.color ||
        yaUsadas.has(textoIncorrecto.texto)
    );

    const opcionIncorrecta = {
        texto: textoIncorrecto.texto,
        color: colorIncorrecto.color
    };

    const opciones = [...correctas, opcionIncorrecta];
    const indiceDiferente = Math.floor(Math.random() * 4);
    [opciones[3], opciones[indiceDiferente]] = [opciones[indiceDiferente], opciones[3]];
    indiceCorrectoGlobal = indiceDiferente;

    opciones.forEach((opcion, index) => {
        const btn = document.createElement("button");
        btn.className = "btn fs-4 fw-bold m-2 px-4 py-3 border rounded shadow";
        btn.textContent = opcion.texto;
        btn.style.color = opcion.color;
        btn.dataset.index = index;
        btn.style.transition = "all 0.2s ease";
        btn.onmouseover = () => btn.style.transform = "scale(1.1)";
        btn.onmouseleave = () => btn.style.transform = "scale(1)";
        btn.onclick = (e) => verificarRespuesta(index === indiceCorrectoGlobal, e.target);
        board.appendChild(btn);
    });

    startTime = Date.now();
}

function verificarRespuesta(acertado, clickedBtn) {
    const tiempo = (Date.now() - startTime) / 1000;
    tiempos.push(tiempo);
    if (!acertado) errores++;

    const botones = document.querySelectorAll("#stroop-board button");

    // Desactivar todos los botones
    botones.forEach(btn => btn.onclick = null);

    if (acertado) {
        clickedBtn.style.backgroundColor = "#c8f7c5"; // verde claro
    } else {
        clickedBtn.style.backgroundColor = "#f8c8c8"; // rojo claro
        botones.forEach(btn => {
            if (parseInt(btn.dataset.index) === indiceCorrectoGlobal) {
                btn.style.backgroundColor = "#c8f7c5"; // correcta → verde claro
            }
        });
    }

    setTimeout(() => {
        rondaActual++;
        siguienteRonda();
    }, 1500);
}

function terminarJuego() {
    const promedio = tiempos.reduce((a, b) => a + b, 0) / tiempos.length;
    const feedback = `✅ Juego terminado. Errores: ${errores}, Tiempo promedio: ${promedio.toFixed(2)}s`;
    document.getElementById("feedback").textContent = feedback;

    fetch("/attention/stroop/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            average_time: promedio.toFixed(2),
            errors: errores,
            rounds_completed: rondasTotales
        })
    })
    .then(res => {
        if (res.ok) {
            console.log("Resultado de atención (Stroop) guardado correctamente");
        } else {
            console.error("Error al guardar el resultado de Stroop");
        }
    })
    .catch(err => console.error("Error de red:", err));
}

document.addEventListener("DOMContentLoaded", () => {
    const instruccionesModal = new bootstrap.Modal(document.getElementById('instruccionesModal'));
    instruccionesModal.show();

    document.getElementById("btn-iniciar").addEventListener("click", () => {
        instruccionesModal.hide();
        setTimeout(() => {
            document.body.classList.remove('modal-open');
            document.querySelector('.modal-backdrop')?.remove();
            startStroop();
        }, 300);
    });
});