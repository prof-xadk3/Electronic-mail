#!/shebang
from fastapi import FastAPI, WebSocket

# from fastapi.responses import JSONResponse

api = FastAPI()


@api.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)
