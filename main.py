#!/shebang
from subprocess import Popen
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse

from rsa import decrypt, encrypt


# from fastapi.responses import JSONResponse
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def Ecrypt(self, websocket: WebSocket, plain):
        await websocket.accept()
        await self.broadcast(encrypt(plain, [111111111, 111111111]))

    async def Dcrypt(self, websocket: WebSocket, plain):
        await websocket.accept()
        await self.broadcast(decrypt(plain, [111111111, 111111111]))

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
api = FastAPI()


@api.get("/")
def return_docs():
    return RedirectResponse("/docs")


"""
# relay here.
@api.websocket("/wz")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)

"""


@api.websocket("/ws/{cli_id}")
async def websocket_endpoint(websocket: WebSocket, cli_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            d = encrypt(str(data), [111111111, 111111111])
            print(d)
            await manager.send_personal_message(f"Pv! {d}", websocket)
            await manager.broadcast(f"Client #{cli_id} tells {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{cli_id} left the relay.")


if __name__ == "__main__":
    proc = Popen('/usr/bin/python3 -m http.server 2580', shell=True)
    print("Python3 server hosted on ://0.0.0.0:2580")
    __import__("uvicorn").run("main:api", host="0.0.0.0", port=55555, reload=True)
