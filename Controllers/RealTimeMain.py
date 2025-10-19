# Controllers/RealtimeMain.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from Services.RealTimeChat import RealtimeChatHandler  # your handler in Services/RealTimeChat.py

app = FastAPI(title="Realtime Chat API")
print("RealTime Main")
# For local dev allow all origins; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"status": "ok", "msg": "Realtime WebSocket server running"}


@app.websocket("/realtime")
async def websocket_endpoint(websocket: WebSocket):
    print("Going to the Real time chat")
    await RealtimeChatHandler(websocket)
