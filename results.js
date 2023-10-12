const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === "results") {
        // Display results on leaderboard
        let html = "";
        for (let name in data.results) {
            html += name + ": " + data.results[name] + "<br>";
        }
        document.getElementById("leaderboard").innerHTML = html;
    }
};

function fetchResults() {
    ws.send(JSON.stringify({type: "get_results"}));
}