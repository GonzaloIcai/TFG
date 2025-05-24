// Emojis agrupados por categoría visual
const emojiGrupos = {
    animales: ["🐶", "🐱", "🐭", "🐰", "🐼", "🦊", "🐸", "🐵"],
    frutas: ["🍎", "🍌", "🍇", "🍓", "🍉", "🍍", "🥝"],
    objetos: ["⚽", "🏀", "🏈", "⚾", "🥎", "🏐", "🏓", "🎾"],
    caritas: ["😀", "😅", "😂", "😍", "😎", "😡", "😭", "🤓"]
};

let round = 1;
let maxRounds = 5;
let startTime;
let responseTimes = [];
let errors = 0;

function getRandomFromGroup(group) {
    return group[Math.floor(Math.random() * group.length)];
}

function getTwoDistinctGroups() {
    const keys = Object.keys(emojiGrupos);
    const baseIndex = Math.floor(Math.random() * keys.length);
    let diffIndex;
    do {
        diffIndex = Math.floor(Math.random() * keys.length);
    } while (diffIndex === baseIndex);
    return [emojiGrupos[keys[baseIndex]], emojiGrupos[keys[diffIndex]]];
}

function startAttentionGame() {
    round = 1;
    responseTimes = [];
    errors = 0;
    loadRound();
}

function loadRound() {
    const board = document.getElementById("attention-board");
    board.innerHTML = "";

    const total = 12 + round * 4;
    const columns = 12;

    board.style.gridTemplateColumns = `repeat(${columns}, 60px)`;

    const [grupoBase, grupoDiferente] = getTwoDistinctGroups();

    const correctEmoji = getRandomFromGroup(grupoBase);
    const wrongEmoji = getRandomFromGroup(grupoDiferente);

    const differentIndex = Math.floor(Math.random() * total);

    for (let i = 0; i < total; i++) {
        const cell = document.createElement("div");
        cell.classList.add("memory-card");
        cell.style.fontSize = "2rem";
        cell.textContent = (i === differentIndex) ? wrongEmoji : correctEmoji;
        cell.onclick = () => handleClick(i === differentIndex);
        board.appendChild(cell);
    }

    startTime = Date.now();
}

function handleClick(isCorrect) {
    const timeTaken = (Date.now() - startTime) / 1000;
    responseTimes.push(timeTaken);

    if (isCorrect) {
        if (round < maxRounds) {
            round++;
            loadRound();
        } else {
            endGame();
        }
    } else {
        errors++;
        alert("¡Ese no es el emoji diferente! Intenta de nuevo.");
    }
}

function endGame() {
    const averageTime = (responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length).toFixed(2);
    alert(`¡Juego terminado!\nTiempo promedio de respuesta: ${averageTime}s\nErrores: ${errors}`);

    // Guardar resultados en Flask
    fetch("/attention/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            average_time: parseFloat(averageTime),
            errors: errors,
            rounds_completed: round
        })
    })
    .then(response => {
        if (response.ok) {
            console.log("Resultado de atención guardado correctamente");
        } else {
            console.error("Error al guardar resultado de atención");
        }
    })
    .catch(error => {
        console.error("Error de red:", error);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const instruccionesModal = new bootstrap.Modal(document.getElementById('instruccionesModal'));
    instruccionesModal.show();

    document.getElementById("btn-iniciar").addEventListener("click", () => {
        instruccionesModal.hide();
        setTimeout(() => {
            document.body.classList.remove('modal-open');
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) backdrop.remove();
            startAttentionGame();
        }, 300);
    });
});
