import asyncio
import websockets
import json

clients = {}
quiz = None

def results():
    return str(clients)

async def handler(websocket, path):
    global quiz, results

    while True:
        try:
            msg = await websocket.recv()
            data = json.loads(msg)
            print("Got", data)

            response = None
            if data["type"] == "register":
                clients[data["name"]] = websocket
                await websocket.send(json.dumps({"type": "wait"}))
            elif data["type"] == "submit_quiz":
                quiz = data["quiz"]
            elif data["type"] == "start_game":
                for ws in clients.values():
                    if ws:  # Check if the websocket is still active
                        response = {"type": "start", "quiz": quiz}
            elif data["type"] == "submit_answer":
                results[data["name"]] = data["answer"]
                clients[data["name"]] = None
            elif data["type"] == "get_results":
                response = {"type": "results", "results": results()}

            if response is not None:
                response = json.dumps(response)
                print("Sending", response)
                await websocket.send(response)

        except websockets.ConnectionClosed:
            print(f"Connection with {websocket.remote_address} closed")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()