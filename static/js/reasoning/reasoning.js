function generarPreguntaMatematica() {
    const tipo = Math.floor(Math.random() * 3); // 0: suma, 1: multiplicacion, 2: serie mixta
    let pregunta, respuestaCorrecta, opciones = [];

    if (tipo === 0) {
        const inicio = Math.floor(Math.random() * 10);
        const paso = Math.floor(Math.random() * 5) + 1;
        const serie = [inicio, inicio + paso, inicio + 2 * paso];
        respuestaCorrecta = inicio + 3 * paso;
        pregunta = `Completa la serie: ${serie.join(", ")}, ?`;
    } else if (tipo === 1) {
        const inicio = Math.floor(Math.random() * 3) + 1;
        const mult = 2;
        const serie = [inicio, inicio * mult, inicio * mult * mult];
        respuestaCorrecta = inicio * Math.pow(mult, 3);
        pregunta = `Completa la serie: ${serie.join(", ")}, ?`;
    } else {
        const a = Math.floor(Math.random() * 5) + 1;
        const b = Math.floor(Math.random() * 3) + 2;
        const x = a;
        const y = a + b;
        const z = (a + b) * b;
        respuestaCorrecta = z + b;
        pregunta = `Completa la serie: ${x}, ${y}, ${z}, ?`;
    }

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

function startGame() {
    preguntas = Array.from({ length: 4 }, generarPreguntaMatematica);
    actual = 0;
    document.getElementById("restartBtn").classList.remove("d-none");
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
        btn.onclick = () => manejarRespuesta(btn, opt.toString() === p.respuestaCorrecta);
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
