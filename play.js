const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === "start") {
        // Display the quiz and handle the logic to answer
        // For simplicity, just displaying the question and options
        document.getElementById("quiz").innerText = data.quiz.question;
        // Add options and logic to submit answer
    }
};

function register() {
    const name = document.getElementById("name").value;
    ws.send(JSON.stringify({type: "register", name: name}));
}
