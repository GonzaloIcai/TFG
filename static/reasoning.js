const questions = [
    {
        series: "2, 4, 6, __",
        options: [7, 8, 10],
        answer: 8
    },
    {
        series: "5, 10, 15, __",
        options: [20, 18, 22],
        answer: 20
    },
    {
        series: "1, 4, 9, 16, __",
        options: [20, 25, 36],
        answer: 25
    },
    {
        series: "100, 90, 80, __",
        options: [60, 70, 75],
        answer: 70
    },
    {
        series: "1, 2, 4, 8, __",
        options: [10, 12, 16],
        answer: 16
    }
];

let currentQuestion = 0;
let correct = 0;
let incorrect = 0;
let startTime;

function startReasoningGame() {
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
