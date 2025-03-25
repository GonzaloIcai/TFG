const cardsArray = [
    "🍎", "🍎", "🍌", "🍌", "🍒", "🍒", "🍇", "🍇",
    "🍉", "🍉", "🥑", "🥑", "🍍", "🍍", "🥕", "🥕"
];

let shuffledCards, flippedCards = [], matchedPairs = 0;
let startTime, attempts = 0;

function shuffle(array) {
    return array.sort(() => Math.random() - 0.5);
}

function startGame() {
    shuffledCards = shuffle([...cardsArray]);
    matchedPairs = 0;
    flippedCards = [];
    attempts = 0;
    startTime = Date.now();
    renderBoard();
}

function renderBoard() {
    const board = document.querySelector(".game-board");
    board.innerHTML = "";
    shuffledCards.forEach((symbol, index) => {
        const card = document.createElement("div");
        card.classList.add("memory-card");
        card.dataset.index = index;
        card.onclick = flipCard;
        board.appendChild(card);
    });
}

function flipCard(event) {
    const card = event.target;
    const index = card.dataset.index;

    if (flippedCards.length < 2 && !flippedCards.includes(index)) {
        card.textContent = shuffledCards[index];
        flippedCards.push(index);

        if (flippedCards.length === 2) {
            setTimeout(checkMatch, 500);
        }
    }
}

function checkMatch() {
    const [first, second] = flippedCards;
    const cards = document.querySelectorAll(".memory-card");

    attempts++; // Cada pareja intentada cuenta como intento

    if (shuffledCards[first] === shuffledCards[second]) {
        matchedPairs++;

        if (matchedPairs === cardsArray.length / 2) {
            const endTime = Date.now();
            const timeSpent = (endTime - startTime) / 1000; // En segundos

            alert("¡Felicidades! Has encontrado todas las parejas.");

            // Guardar resultados en el backend
            fetch("/memory/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    time_spent: timeSpent,
                    attempts: attempts
                })
            })
            .then(response => {
                if (response.ok) {
                    console.log("Resultado guardado exitosamente");
                } else {
                    console.error("Error al guardar resultado");
                }
            })
            .catch(error => console.error("Error de red:", error));
        }
    } else {
        cards[first].textContent = "";
        cards[second].textContent = "";
    }

    flippedCards = [];
}

document.addEventListener("DOMContentLoaded", startGame);
