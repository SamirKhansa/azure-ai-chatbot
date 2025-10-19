import os
import json
import base64
import asyncio
import websockets
from fastapi import WebSocket
from keys import GPT_REALTIME_KEY, GPT_REALTIME_ENDPOINT, GPT_REALTIME_DEPLOYMENT_NAME, API_VERSION
from config import GetRealTimeClient  




async def RealtimeChatHandler(websocket: WebSocket):
    await websocket.accept()
    print("🎤 Frontend connected to Realtime")

    azure_ws = await GetRealTimeClient(
        api_key=GPT_REALTIME_KEY,
        endpoint=GPT_REALTIME_ENDPOINT,
        deployment_name=GPT_REALTIME_DEPLOYMENT_NAME,
        api_version=API_VERSION
    )
    print("🔊 Connected to Azure GPT Realtime WebSocket")

    # Send initial greeting
    await azure_ws.send(json.dumps({
        "type": "response.create",
        "response": {
            "modalities": ["audio", "text"],
            "instructions": (
                "You are a helpful chess assistant. Always reply in English, "
                "even if the user talks in another language. "
                "Only answer questions related to chess. "
                
            )
        }
    }))

    async def forward_to_azure():
        """Forward audio from frontend to GPT Realtime"""
        print("1")
        try:
            while True:
                msg_str = await websocket.receive_text()
                msg_json = json.loads(msg_str)
                # print(msg_json)
                
                if msg_json.get("type") == "input_audio_buffer.append":
                    audio_b64 = msg_json.get("audio")
                    if audio_b64:
                        # print("Audio has been received from the frontend")
                        await azure_ws.send(json.dumps({
                            "type": "input_audio_buffer.append",
                            "audio": audio_b64
                        }))
                elif msg_json.get("type") == "input_audio_buffer.commit":
                    await azure_ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
                elif msg_json.get("type") == "response.generate":
                    await azure_ws.send(json.dumps({"type": "response.generate"}))
        except Exception as e:
            print("⚠️ Frontend disconnected or error in forward_to_azure:", e)
            await azure_ws.close()

    async def forward_to_frontend():
        """Send audio and text responses from GPT back to frontend"""
        print("2")
        try:
            print("🧠 Waiting for first message from Azure Realtime...")
            async for msg in azure_ws:
                # print("📩 Azure sent:", msg.keys())
                # print("Azure Sent this",msg) 
                msg_json = json.loads(msg)
                
                
                if msg_json.get("type") in ["response.audio_buffer.delta", "response.audio.delta"]:
                    delta_data = msg_json.get("delta")
                    if delta_data:  # only send if delta exists
                        await websocket.send_json({
                            "type": "audio.delta",
                            "data": delta_data
                        })
                elif msg_json.get("type") == "response.audio_transcript.done":
                    await websocket.send_json({
                        "type": "transcript",
                        "text": msg_json.get("transcript", "")
                    })
        except Exception as e:
            print("⚠️ Azure WS closed or error in forward_to_frontend:", e)

    # ✅ Start both simultaneously
    asyncio.create_task(forward_to_frontend())
    await forward_to_azure()
