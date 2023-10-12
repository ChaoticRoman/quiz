import asyncio
import websockets
import json

clients = {}
quiz = None
results = {}

async def handler(websocket, path):
    global quiz, results

    try:
        msg = await websocket.recv()
        data = json.loads(msg)
        print(data)
        if data["type"] == "register":
            clients[data["name"]] = websocket
            await websocket.send(json.dumps({"type": "wait"}))
        elif data["type"] == "submit_quiz":
            quiz = data["quiz"]
        elif data["type"] == "start_game":
            for ws in clients.values():
                await ws.send(json.dumps({"type": "start", "quiz": quiz}))
        elif data["type"] == "submit_answer":
            results[data["name"]] = data["answer"]
            clients[data["name"]] = None
        elif data["type"] == "get_results":
            await websocket.send(json.dumps({"type": "results", "results": results}))

    except Exception as e:
        print(f"Error: {e}")

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()