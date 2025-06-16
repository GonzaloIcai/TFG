const emojiPairs = [
    ["😀", "😃"], ["✋", "🖐"], ["🧒", "👦"], ["👩‍🍳", "👨‍🍳"],
    ["👨‍🏫", "👩‍🏫"], ["👩‍⚕️", "👨‍⚕️"], ["👨‍🎓", "👩‍🎓"],
    ["👨‍🚒", "👩‍🚒"], ["👨‍✈️", "👩‍✈️"], ["👨‍🔧", "👩‍🔧"],
    ["👨‍🌾", "👩‍🌾"], ["👨‍🎨", "👩‍🎨"], ["🧑‍🏫", "👩‍🏫"],
    ["🧑‍⚕️", "👨‍⚕️"], ["🧑‍🔬", "👩‍🔬"], ["🧑‍🍳", "👩‍🍳"],
    ["😐", "😶"], ["🙂", "😊"], ["😯", "😲"],
    ["🌕", "🌝"], ["🐶", "🐕"], ["🍏", "🍎"],
    ["💡", "🔦"], ["📕", "📗"], ["🧊", "❄️"], ["🪙", "💰"]
];

let usedPairs = [];
let round = 1;
const maxRounds = 5;
let startTime;
let responseTimes = [];
let errors = 0;
let correctIndexGlobal = null;

function startAttentionGame() {
    round = 1;
    errors = 0;
    usedPairs = [];
    responseTimes = [];
    loadRound();
}

function loadRound() {
    const board = document.getElementById("attention-board");
    board.innerHTML = "";

    if (usedPairs.length === emojiPairs.length) usedPairs = []; // Reinicio total si ya se usaron todos los pares

    let pair;
    do {
        pair = emojiPairs[Math.floor(Math.random() * emojiPairs.length)];
    } while (usedPairs.includes(pair.toString()));

    usedPairs.push(pair.toString());

    const [emoji1, emoji2] = pair;
    const total = 25;
    const correctIndex = Math.floor(Math.random() * total);
    correctIndexGlobal = correctIndex;

    for (let i = 0; i < total; i++) {
        const div = document.createElement("div");
        div.className = "attention-card";
        div.textContent = (i === correctIndex) ? emoji2 : emoji1;
        div.onclick = () => handleClick(i, div);
        board.appendChild(div);
    }

    startTime = Date.now();
}

function handleClick(index, clickedDiv) {
    const timeTaken = (Date.now() - startTime) / 1000;
    responseTimes.push(timeTaken);

    const board = document.getElementById("attention-board");
    const allCards = board.querySelectorAll(".attention-card");

    if (index === correctIndexGlobal) {
        clickedDiv.classList.add("correct");
    } else {
        clickedDiv.classList.add("incorrect");
        allCards[correctIndexGlobal].classList.add("correct");
        errors++;
    }

    allCards.forEach(card => card.onclick = null); // deshabilita clics

    setTimeout(() => {
        if (round < maxRounds) {
            round++;
            loadRound();
        } else {
            endGame();
        }
    }, 1200);
}

function endGame() {
    const averageTime = (responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length).toFixed(2);
    alert(`¡Juego terminado!\nTiempo promedio: ${averageTime}s\nErrores: ${errors}`);

    fetch("/attention/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            average_time: parseFloat(averageTime),
            errors: errors,
            rounds_completed: round
        })
    }).then(res => console.log("Resultado guardado."));
}

document.addEventListener("DOMContentLoaded", () => {
    const instruccionesModal = new bootstrap.Modal(document.getElementById('instruccionesModal'));
    instruccionesModal.show();

    document.getElementById("btn-iniciar").addEventListener("click", () => {
        instruccionesModal.hide();
        setTimeout(() => {
            document.body.classList.remove('modal-open');
            document.querySelector('.modal-backdrop')?.remove();
            startAttentionGame();
        }, 300);
    });
});
