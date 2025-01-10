# bootstraping
from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect


app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@app.get('/')
async def read_main():
    return {'msg': 'Hello World'}

# noted we accept one connection at a time as this is very resource consuming task
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            header= await websocket.receive_json()
            print(header)
            #data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {header}", websocket)
            #await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        #await manager.send_personal_message(f"Client #{client_id} left the chat")
        #we are already being disconnected
        manager.disconnect(websocket)
        

