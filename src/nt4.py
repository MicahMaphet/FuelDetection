import json
import util
import requests
import websocket

result = requests.get("http://127.0.0.1:5810")
if result is not None and result.ok:
    print("Connected to network tables")

ws = websocket.WebSocketApp("ws://127.0.0.1:5810/nt/micahvision")

global state
state: dict = {}

def on_message(ws, message):
    global state
    print(10 * "*" + "Message" + 10 * "*")
    if type(message) is str:
        data = json.loads(message)
        for d in data:
            path: list = d["params"]["name"].split("/")[1:]
            print(path)
            state = util.merge(state, util.path_to_obj(path))

    elif type(message) is bytes:
        print(message)
        print(util.decode(message))
    else:
        print(type(message))

ws.on_message = on_message

def on_close(ws, status, message):
    print("Closed")
    print(f"status: {status}")
    print(f"message: {message}")
ws.on_close = on_close

def on_reconnect(ws):
    print("Reconnected")
ws.on_reconnect = on_reconnect

def on_open(ws):
    print("Open")
    ws.send('''[
        {
            "method": "subscribe",
            "params": {
                "topics": ["/AdvantageKit/DriverStation/Autonomous"],
                "subuid": 94608538,
                "options": {
                    "periodic": 0.02,
                    "all": false,
                    "topicsOnly": false,
                    "prefix": true
                }
            }
        }
    ]''')

ws.on_open = on_open


ws.run_forever(reconnect=2)

print(state)
