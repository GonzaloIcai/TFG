
function generarPreguntaMatematica() {
    const tipo = Math.floor(Math.random() * 3); // 0 = suma, 1 = resta, 2 = multiplicación
    let pregunta, respuestaCorrecta, opciones = [];

    let inicio = Math.floor(Math.random() * 11) + 1;

    if (tipo === 0) {
        // Suma
        const paso = Math.floor(Math.random() * 5) + 2; // +2 a +6
        const serie = [inicio];
        for (let i = 1; i < 5; i++) {
            serie.push(serie[i - 1] + paso);
        }
        respuestaCorrecta = serie[4] + paso;
        pregunta = `Completa la serie: ${serie.join(", ")}, ?`;

    } else if (tipo === 1) {
        // Resta
        const paso = Math.floor(Math.random() * 4) + 2; // -2 a -5
        inicio += paso * 5; // asegurar que no sea negativo
        const serie = [inicio];
        for (let i = 1; i < 5; i++) {
            serie.push(serie[i - 1] - paso);
        }
        respuestaCorrecta = serie[4] - paso;
        pregunta = `Completa la serie: ${serie.join(", ")}, ?`;

    } else if (tipo === 2) {
        // Multiplicación sencilla
        const factor = Math.floor(Math.random() * 2) + 2; // ×2 o ×3
        inicio = Math.floor(Math.random() * 4) + 1;
        const serie = [inicio];
        for (let i = 1; i < 5; i++) {
            serie.push(serie[i - 1] * factor);
        }
        respuestaCorrecta = serie[4] * factor;
        pregunta = `Completa la serie: ${serie.join(", ")}, ?`;
    }

    // Generar opciones
    opciones.push(respuestaCorrecta);
    while (opciones.length < 4) {
        const fake = respuestaCorrecta + Math.floor(Math.random() * 10) - 5;
        if (!opciones.includes(fake) && fake >= 0) opciones.push(fake);
    }

    opciones = opciones.sort(() => Math.random() - 0.5);
    return { pregunta, opciones, respuestaCorrecta: respuestaCorrecta.toString() };
}


let preguntas = [];
let actual = 0;
let tiempoInicioJuego = null;

function startGame() {
    tiempoInicioJuego = Date.now();
    preguntas = Array.from({ length: 4 }, generarPreguntaMatematica);
    actual = 0;
    document.getElementById("restartBtn").classList.add("d-none");
    mostrarPregunta();
}

function mostrarPregunta() {
    const p = preguntas[actual];
    document.getElementById("question").textContent = p.pregunta;
    const opcionesDiv = document.getElementById("options");
    opcionesDiv.innerHTML = "";

    p.opciones.forEach((opt, index) => {
        const btn = document.createElement("button");
        btn.textContent = opt;
        btn.className = "btn fs-4 m-2 px-4 py-3 border rounded shadow btn-opcion";
        btn.style.transition = "all 0.2s ease";
        btn.style.minWidth = "110px";
        btn.onmouseover = () => btn.style.transform = "scale(1.1)";
        btn.onmouseleave = () => btn.style.transform = "scale(1)";
        btn.onclick = () => manejarRespuesta(btn, opt.toString() === p.respuestaCorrecta.toString(), p.respuestaCorrecta);
        opcionesDiv.appendChild(btn);
    });
}


function manejarRespuesta(boton, correcto, respuestaCorrecta) {
    const botones = document.querySelectorAll(".btn-opcion");
    botones.forEach(b => b.disabled = true);

    if (correcto) {
        boton.style.backgroundColor = "#c8f7c5"; // verde claro
    } else {
        boton.style.backgroundColor = "#f8c8c8"; // rojo claro
        botones.forEach(b => {
            if (b.textContent === respuestaCorrecta) {
                b.style.backgroundColor = "#c8f7c5"; // resaltar correcta
            }
        });
    }

    setTimeout(() => {
        actual++;
        if (actual < preguntas.length) {
            mostrarPregunta();
        } else {
            document.getElementById("question").textContent = "¡Juego completado!";
            document.getElementById("options").innerHTML = "";
            document.getElementById("restartBtn").classList.remove("d-none");

            const tiempoTotal = ((Date.now() - tiempoInicioJuego) / 1000).toFixed(2);
            const correctas = document.querySelectorAll(".btn-opcion").filter(b => b.style.backgroundColor === "#c8f7c5").length;
            const incorrectas = document.querySelectorAll(".btn-opcion").filter(b => b.style.backgroundColor === "#f8c8c8").length;

            fetch("/reasoning/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    correct: correctas,
                    incorrect: incorrectas,
                    time_spent: tiempoTotal
                })
            }).then(res => {
                if (res.ok) {
                    console.log("Resultado de razonamiento guardado correctamente");
                } else {
                    console.error("Error al guardar resultado de razonamiento");
                }
            });
        }
    }, 1500);
}


document.addEventListener("DOMContentLoaded", () => {
    const instruccionesModal = new bootstrap.Modal(document.getElementById('instruccionesModal'));
    instruccionesModal.show();

    document.getElementById("iniciarBtn").addEventListener("click", () => {
        instruccionesModal.hide();
        setTimeout(() => {
            document.body.classList.remove('modal-open');
            document.querySelector('.modal-backdrop')?.remove();
            startGame();
        }, 300);
    });
});
