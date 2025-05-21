const patterns = [
    {
        question: "🔺🔺🔺, 🔺🔺, 🔺, ___",
        options: ["", "🔺", "🔺🔺🔺"],
        answer: "🔺"
    },
    {
        question: "🔵🔵, 🔴🔴, 🔵, 🔴, ___",
        options: ["🔵", "🔴", "🟢"],
        answer: "🔵"
    },
    {
        question: "🟥⬜🟥, ⬜🟥⬜, 🟥⬜🟥, ___",
        options: ["⬜🟥⬜", "🟥⬜", "🟥🟥🟥"],
        answer: "⬜🟥⬜"
    },
    {
        question: "⬛⬛⬛, ⬛⬛, ⬛, ___",
        options: ["⬛", "⬛⬛⬛⬛", ""],
        answer: ""
    },
    {
        question: "🔶🔷, 🔷🔶, 🔶🔷, ___",
        options: ["🔷🔶", "🔶🔶", "🔷🔷"],
        answer: "🔷🔶"
    }
];

let currentIndex = 0;
let correct = 0;
let incorrect = 0;
let startTime;

function startPatternGame() {
    currentIndex = 0;
    correct = 0;
    incorrect = 0;
    startTime = Date.now();
    showPattern();
}

function showPattern() {
    const q = patterns[currentIndex];
    document.getElementById("pattern-question").textContent = `Serie: ${q.question}`;

    const container = document.getElementById("pattern-options");
    container.innerHTML = "";

    q.options.forEach(option => {
        const btn = document.createElement("button");
        btn.className = "btn btn-outline-warning btn-lg m-2";
        btn.textContent = option;
        btn.onclick = () => checkPatternAnswer(option);
        container.appendChild(btn);
    });
}

function checkPatternAnswer(selected) {
    const correctAnswer = patterns[currentIndex].answer;

    if (selected === correctAnswer) {
        correct++;
    } else {
        incorrect++;
        alert("❌ Incorrecto.");
    }

    currentIndex++;
    if (currentIndex < patterns.length) {
        showPattern();
    } else {
        endPatternGame();
    }
}

function endPatternGame() {
    const timeSpent = ((Date.now() - startTime) / 1000).toFixed(2);
    alert(`🧠 Juego completado\nCorrectas: ${correct}\nIncorrectas: ${incorrect}\nTiempo: ${timeSpent}s`);

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
    }).then(res => console.log("Resultado de razonamiento guardado."));
}

document.addEventListener("DOMContentLoaded", startPatternGame);
