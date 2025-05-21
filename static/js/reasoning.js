let questions = [];
let currentQuestion = 0;
let correct = 0;
let incorrect = 0;
let startTime;

function generateQuestion() {
    const type = Math.random() < 0.5 ? "sum" : "mult";

    let start = Math.floor(Math.random() * 5) + 1;
    let step = Math.floor(Math.random() * 4) + 1;

    let sequence = [];
    let correct;

    if (type === "sum") {
        for (let i = 0; i < 4; i++) {
            sequence.push(start + i * step);
        }
        correct = start + 4 * step;
    } else {
        for (let i = 0; i < 4; i++) {
            sequence.push(start * Math.pow(step, i));
        }
        correct = start * Math.pow(step, 4);
    }

    const seriesStr = sequence.join(", ") + ", __";

    // Crear opciones
    const options = new Set();
    options.add(correct);
    while (options.size < 3) {
        const offset = Math.floor(Math.random() * 6) + 1;
        options.add(correct + (Math.random() < 0.5 ? -offset : offset));
    }

    return {
        series: seriesStr,
        options: Array.from(options).sort(() => Math.random() - 0.5),
        answer: correct
    };
}

function startReasoningGame() {
    questions = [];
    for (let i = 0; i < 5; i++) {
        questions.push(generateQuestion());
    }

    currentQuestion = 0;
    correct = 0;
    incorrect = 0;
    startTime = Date.now();
    showQuestion();
}

function showQuestion() {
    const q = questions[currentQuestion];
    document.getElementById("question").textContent = `¿Qué número completa la serie: ${q.series}?`;

    const optionsDiv = document.getElementById("options");
    optionsDiv.innerHTML = "";

    q.options.forEach(option => {
        const btn = document.createElement("button");
        btn.className = "btn btn-outline-warning btn-lg";
        btn.textContent = option;
        btn.onclick = () => checkAnswer(option);
        optionsDiv.appendChild(btn);
    });
}

function checkAnswer(selected) {
    const q = questions[currentQuestion];
    if (selected === q.answer) {
        correct++;
    } else {
        incorrect++;
        alert("Respuesta incorrecta 😕");
    }

    currentQuestion++;
    if (currentQuestion < questions.length) {
        showQuestion();
    } else {
        endGame();
    }
}

function endGame() {
    const timeSpent = ((Date.now() - startTime) / 1000).toFixed(2);
    alert(`¡Juego terminado!\nCorrectas: ${correct}\nIncorrectas: ${incorrect}\nTiempo total: ${timeSpent}s`);

    fetch("/reasoning/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            correct: correct,
            incorrect: incorrect,
            time_spent: parseFloat(timeSpent)
        })
    })
    .then(response => {
        if (response.ok) {
            console.log("Resultado de razonamiento guardado");
        } else {
            console.error("Error al guardar resultado de razonamiento");
        }
    })
    .catch(error => {
        console.error("Error de red:", error);
    });
}

document.addEventListener("DOMContentLoaded", startReasoningGame);
