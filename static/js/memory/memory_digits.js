let sequence = [];
let startTime;
let intentos = 0;
const maxRondas = 5;
let rondaActual = 0;

function generateSequence(length = 5) {
    if (rondaActual >= maxRondas) {
        document.getElementById("sequence").textContent = "¡Ejercicio completado!";
        document.getElementById("user-input").disabled = true;
        return;
    }

    sequence = [];
    for (let i = 0; i < length; i++) {
        sequence.push(Math.floor(Math.random() * 9) + 1);
    }

    document.getElementById("sequence").textContent = sequence.join(" - ");

    setTimeout(() => {
        document.getElementById("sequence").textContent = "Ahora escríbela 👇";
        startTime = Date.now();
    }, 4000);
}

function checkSequence() {
    const input = document.getElementById("user-input").value.trim().split(" ");
    const userSeq = input.map(num => parseInt(num));
    const timeSpent = ((Date.now() - startTime) / 1000).toFixed(2);
    intentos++;

    const isCorrect = JSON.stringify(userSeq) === JSON.stringify(sequence);
    const feedback = document.getElementById("feedback");

    if (isCorrect) {
        feedback.textContent = `✅ ¡Correcto! Has tardado ${timeSpent} segundos.`;
        saveResult(timeSpent);
    } else {
        feedback.textContent = `❌ Incorrecto. La secuencia era: ${sequence.join(" ")}`;
    }

    document.getElementById("user-input").value = "";
    rondaActual++;
    generateSequence();
}

function saveResult(tiempo) {
    fetch("/memory/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            attempts: intentos,
            time_spent: parseFloat(tiempo)
        })
    }).then(res => console.log("Guardado!"));
}

function startGame() {
    document.getElementById("juegoMemoriaDigits").classList.remove("d-none");
    generateSequence();
}

document.addEventListener("DOMContentLoaded", () => {
    const instruccionesModal = new bootstrap.Modal(document.getElementById('instruccionesModal'));
    instruccionesModal.show();
});

