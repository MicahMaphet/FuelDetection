import requests
import websocket

result = requests.get("http://127.0.0.1:5810")
if result is not None and result.ok:
    print("Connected to network tables")

ws = websocket.WebSocketApp("ws://127.0.0.1:5810/nt/micahvision")

def on_message(ws, message):
    print(message)
ws.on_message = on_message

def on_close(ws, status, message):
    print("Closed")
    print(f"status: {status}")
    print(f"message: {message}")
ws.on_close = on_close

def on_reconnect(ws):
    print("Reconnected")
ws.on_reconnect = on_reconnect

ws.run_forever(reconnect=2)

# res = ws.send('''[
#     {
#         method: "subscribe",
#         params: {
#             topics: ["AdvantageKit"],
#             subuid: 94608538,
#             options: {
#                 periodic: 0.1,
#                 all: false,
#                 topicsOnly: false,
#                 prefix: false
#             }
#         }
#     }
# ]''')
