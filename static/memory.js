const cardsArray = [
    "🍎", "🍎", "🍌", "🍌", "🍒", "🍒", "🍇", "🍇",
    "🍉", "🍉", "🥑", "🥑", "🍍", "🍍", "🥕", "🥕"
];

let shuffledCards, flippedCards = [], matchedPairs = 0;

function shuffle(array) {
    return array.sort(() => Math.random() - 0.5);
}

function startGame() {
    shuffledCards = shuffle([...cardsArray]);
    matchedPairs = 0;
    flippedCards = [];
    renderBoard();
}

function renderBoard() {
    const board = document.querySelector(".game-board");
    board.innerHTML = "";
    shuffledCards.forEach((symbol, index) => {
        const card = document.createElement("div");
        card.classList.add("card");
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
    const cards = document.querySelectorAll(".card");

    if (shuffledCards[first] === shuffledCards[second]) {
        matchedPairs++;
        if (matchedPairs === cardsArray.length / 2) {
            alert("¡Felicidades! Has encontrado todas las parejas.");
        }
    } else {
        cards[first].textContent = "";
        cards[second].textContent = "";
    }

    flippedCards = [];
}

document.addEventListener("DOMContentLoaded", startGame);
