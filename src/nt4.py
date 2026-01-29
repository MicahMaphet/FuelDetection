import json
import random
import util
import requests
import websocket

result = requests.get("http://127.0.0.1:5810")
if result is not None and result.ok:
    print("Connected to network tables")

ws = websocket.WebSocketApp("ws://127.0.0.1:5810/nt/micahvision")

class Topic:
    name: str
    id: int
    value = None
    def toString(self):
        return \
f'''{{
    "name": {self.name},
    "id": {self.id},
    "value": {self.value}
}}'''
    def toPubString(self):
        return \
f'''{{
    "name": "{self.name}",
    "type": "int",
    "pubuid": {self.id},
    "properties": {{}}
}}'''

class SubscriptionOptions:
    periodic: float = 0.02
    all: bool = True
    topicsOnly: bool = False
    prefix: bool = True
    def toString(self):
        return \
f'''{{
    "periodic": {self.periodic},
    "all": {str(self.all).lower()},
    "topicsOnly": {str(self.topicsOnly).lower()},
    "prefix": {str(self.prefix).lower()}
}}'''

class Subscription:
    uid: int = -1
    topics = []
    options = SubscriptionOptions()

    def toString(self):
        return \
f'''{{
    "topics": {self.topics},
    "subuid": {self.uid},
    "options": {self.options.toString()}
}}'''

global topics
topics: dict[int, Topic] = {}

def on_message(ws, message):
    global topics
    print(10 * "*" + "Message" + 10 * "*")
    if type(message) is str:
        data = json.loads(message)
        for d in data:
            params = d["params"]
            topic = Topic()
            topic.name = params["name"]
            topic.id = int(params["id"])
            topics[topic.id] = topic
            print(topic.toString())

    elif type(message) is bytes:
        data = util.decode(message)
        for d in data:
            (id, _, _, value) = d
            topics[id].value = value
            print(f'{topics[id].name}: {topics[id].value}')
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
    subscribe("/AdvantageKit/DriverStation")
    publish("/MicahVision/val")
ws.on_open = on_open

def subscribe(topic: str):
    sub = Subscription()
    sub.topics = [topic]
    sub.uid = getNewUid()
    sub.options = SubscriptionOptions()
    sendJson("subscribe", sub.toString())

def publish(topic: str):
    newTopic = Topic()
    newTopic.name = topic
    newTopic.id = getNewUid()
    sendJson("publish", newTopic.toPubString())

def sendJson(method: str, params):
    payload = \
f'''[{{
    "method": "{method}",
    "params": {params}
}}]'''.replace("'", "\"")

    print(payload)
    ws.send(payload)

def getNewUid() -> int:
    return random.randint(0, 99999999)

ws.run_forever(reconnect=2)
