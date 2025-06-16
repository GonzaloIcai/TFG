// reasoning_math.js - versión final con guardado de resultados

function generarPreguntaMatematica() {
    const tipo = Math.floor(Math.random() * 3); // Solo 3 tipos: 0, 1, 2
    let pregunta, respuestaCorrecta, opciones = [];

    if (tipo === 0) {
        // Serie de suma aleatoria con 5 términos
        const inicio = Math.floor(Math.random() * 10);
        const paso = Math.floor(Math.random() * 13) + 3;  // 3 a 15
        const serie = [inicio];
        for (let i = 1; i < 5; i++) {
            serie.push(serie[i - 1] + paso);
        }
        respuestaCorrecta = serie[4] + paso;
        pregunta = `Completa la serie: ${serie.join(", ")}, ?`;

    } else if (tipo === 1) {
        // Serie de multiplicación aleatoria con 5 términos
        const inicio = Math.floor(Math.random() * 3) + 1;
        const mult = Math.floor(Math.random() * 7) + 2;   // 2 a 8
        const serie = [inicio];
        for (let i = 1; i < 5; i++) {
            serie.push(serie[i - 1] * mult);
        }
        respuestaCorrecta = serie[4] * mult;
        pregunta = `Completa la serie: ${serie.join(", ")}, ?`;

    } else if (tipo === 2) {
        // Serie mixta aleatoria (suma + multiplicación con 5 términos)
        const a = Math.floor(Math.random() * 10) + 1;
        const suma = Math.floor(Math.random() * 4) + 2;
        const mult = Math.floor(Math.random() * 4) + 2;
        const serie = [a];
        for (let i = 1; i < 5; i++) {
            if (i % 2 === 1) {
                serie.push(serie[i - 1] + suma);
            } else {
                serie.push(serie[i - 1] * mult);
            }
        }
        respuestaCorrecta = serie[4] + suma;
        pregunta = `Completa la serie: ${serie.join(", ")}, ?`;
    }

    // Generar opciones
    opciones.push(respuestaCorrecta);
    while (opciones.length < 4) {
        const fake = respuestaCorrecta + Math.floor(Math.random() * 20) - 10;
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

    p.opciones.forEach(opt => {
        const btn = document.createElement("button");
        btn.textContent = opt;
        btn.className = "btn btn-outline-dark btn-opcion";
        btn.onclick = () => manejarRespuesta(btn, opt.toString() === p.respuestaCorrecta.toString());
        opcionesDiv.appendChild(btn);
    });
}

function manejarRespuesta(boton, correcto) {
    const botones = document.querySelectorAll(".btn-opcion");
    botones.forEach(b => b.disabled = true);

    boton.classList.add(correcto ? "btn-correcta" : "btn-incorrecta");

    setTimeout(() => {
        actual++;
        if (actual < preguntas.length) {
            mostrarPregunta();
        } else {
            document.getElementById("question").textContent = "¡Juego completado!";
            document.getElementById("options").innerHTML = "";
            document.getElementById("restartBtn").classList.remove("d-none");

            const correctas = document.querySelectorAll(".btn-correcta").length;
            const incorrectas = document.querySelectorAll(".btn-incorrecta").length;
            const tiempoTotal = ((Date.now() - tiempoInicioJuego) / 1000).toFixed(2);

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
    }, 1000);
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
