#!/shebang
from fastapi import FastAPI, WebSocket
from fastapi.responses import RedirectResponse

# from fastapi.responses import JSONResponse

api = FastAPI()


@api.get("/")
def return_docs():
    return RedirectResponse("/docs")


# relay here.
@api.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)


if __name__ == "__main__":
    __import__("uvicorn").run("main:api", host="0.0.0.0", port=55555, reload=True)
