import os
import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from keys import GPT_REALTIME_KEY, GPT_REALTIME_ENDPOINT, GPT_REALTIME_DEPLOYMENT_NAME, API_VERSION
from config import GetRealTimeClient  
from Services.OpenAiServices import GenerateChessImage, SuggestStrategy
from Controllers.RealTime import DocumentRealtime

async def RealtimeChatHandler(websocket: WebSocket):
    await websocket.accept()
    print("🎤 Frontend connected to Realtime")

    # Connect to Azure GPT Realtime WebSocket
    azure_ws = await GetRealTimeClient(
        api_key=GPT_REALTIME_KEY,
        endpoint=GPT_REALTIME_ENDPOINT,
        deployment_name=GPT_REALTIME_DEPLOYMENT_NAME,
        api_version=API_VERSION
    )
    print("🔊 Connected to Azure GPT Realtime WebSocket")

    # Configure session with server VAD
    await azure_ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "instructions": (
                "You are a helpful chess assistant. "
                "Always reply in English. "
                "Answer strictly based on the provided documents. "
                "Include a 'References' section at the end of answers. "
                "If the user speaks while you are talking, immediately stop your audio. "
                "Do not continue or ask further questions."
            ),
            "turn_detection": {"type": "server_vad"},
            "tools": [
                {
                    "type": "function",
                    "name": "GenerateChessImage",
                    "description": "Generate an image of a chess opening or position.",
                    "parameters": {
                        "type": "object",
                        "properties": {"opening_name": {"type": "string"}},
                        "required": ["opening_name"]
                    }
                },
                {
                    "type": "function",
                    "name": "DocumentRealtime",
                    "description": "Retrieve relevant chunks from documents.",
                    "parameters": {
                        "type": "object",
                        "properties": {"Question": {"type": "string"}},
                        "required": ["Question"]
                    }
                }
            ]
        }
    }))
    print("🧩 Session initialized with tool definitions")

    # Initial greeting
    await azure_ws.send(json.dumps({
        "type": "response.create",
        "response": {
            "modalities": ["audio", "text"],
            "instructions": "Welcome to Chess Assistant! How can I help you today?"
        }
    }))

    async def forward_to_azure():
        try:
            while True:
                msg_str = await websocket.receive_text()
                msg_json = json.loads(msg_str)
                print("Theeee Typeeee isssss =====  ",msg_json.get("type"))

                if msg_json.get("type") == "input_audio_buffer.append":
                    audio_b64 = msg_json.get("audio")
                    if audio_b64:
                        await azure_ws.send(json.dumps({
                            "type": "input_audio_buffer.append",
                            "audio": audio_b64
                        }))
                elif msg_json.get("type") == "input_audio_buffer.commit":
                    await azure_ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
                elif msg_json.get("type") == "response.generate":
                    await azure_ws.send(json.dumps({"type": "response.generate"}))
                # elif msg_json.get("type") == "stop":
                #     print("🛑 Stop command received from frontend")
                #     await azure_ws.send(json.dumps({"type": "response.cancel"}))
                #     await websocket.send_json({"type": "stop_audio"})

        except WebSocketDisconnect:
            print("Frontend disconnected")
            try:
                await azure_ws.close()
            except:
                pass
        except Exception as e:
            print("⚠️ Forward to Azure error:", e)
            await azure_ws.close()

    async def forward_to_frontend():
        try:
            print("🧠 Waiting for messages from Azure Realtime...")
            async for msg in azure_ws:
                msg_json = json.loads(msg)
                msg_type = msg_json.get("type")
                print("The message type is the following:", msg_type)

                # 🆕 Handle when server detects user has started speaking
                if msg_type == "input_audio_buffer.speech_started":
                    print("🎙️ Detected user speech (server_vad)")
                    # Tell frontend to stop playing AI audio immediately
                    await websocket.send_json({"type": "stop_audio"})
                    continue

                # Handle function calls
                if msg_type == "response.function_call_arguments.done":
                    fn_name = msg_json["name"]
                    fn_args = msg_json["arguments"]
                    if isinstance(fn_args, str):
                        fn_args = json.loads(fn_args)

                    if fn_name == "GenerateChessImage":
                        image_result = GenerateChessImage(fn_args.get("opening_name", ""))
                        await websocket.send_json({"type": "image_url", "name": fn_name, "url": image_result["image_url"]})

                    elif fn_name == "SuggestStrategy":
                        strategy_text = SuggestStrategy(fn_args.get("level", "beginner"))
                        await websocket.send_json({"type": "function_result", "name": fn_name, "result": strategy_text})

                    elif fn_name == "DocumentRealtime":
                        question = fn_args.get("Question", "")
                        context_text = DocumentRealtime(question)
                        await azure_ws.send(json.dumps({
                            "type": "response.create",
                            "response": {
                                "modalities": ["text", "audio"],
                                "instructions": f"Use this context:\n{context_text}\nNow answer: {question}"
                            }
                        }))

                # Handle audio deltas
                elif msg_type in ["response.audio_buffer.delta", "response.audio.delta"]:
                    delta_data = msg_json.get("delta")
                    if delta_data:
                        await websocket.send_json({"type": "audio.delta", "data": delta_data})

                # Handle transcript
                elif msg_type == "response.audio_transcript.done":
                    transcript = msg_json.get("transcript", "")
                    await websocket.send_json({"type": "transcript", "text": transcript})

                # Handle user interruption (explicitly detected)
                elif msg_type == "conversation.interrupted":
                    print("🛑 User interrupted the model!")
                    await websocket.send_json({"type": "stop_audio"})

                else:
                    await websocket.send_json({"type": "meta", "data": msg_json})

        except Exception as e:
            print("⚠️ Forward to Frontend error:", e)


    # Run both tasks concurrently
    asyncio.create_task(forward_to_frontend())
    await forward_to_azure()
