const ws = new WebSocket('ws://localhost:8765');

function submitQuiz() {
    const quizData = document.getElementById("quizData").value;
    ws.send(JSON.stringify({type: "submit_quiz", quiz: JSON.parse(quizData)}));
}

function startGame() {
    ws.send(JSON.stringify({type: "start_game"}));
}
