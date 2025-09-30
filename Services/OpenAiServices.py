
import json
import azure.functions as func
from config import DallE3Client


def AiReply(client, conversation, context=None, tools=None):
    if not conversation:
        conversation = [{"role": "user", "Content": "Hello"}]

    # System message
    system_message = (
        "You are a highly knowledgeable and professional chess instructor AI. "
        "Your role is to provide clear, accurate, and insightful guidance on all aspects of chess, "
        "including rules, strategies, tactics, openings, middlegame concepts, and endgames. "
        "You must only respond to questions directly related to chess and politely decline unrelated topics. "
        "Ensure that your explanations are tailored to the user's skill level, whether beginner, intermediate, or advanced, "
        "and maintain a supportive, educational, and professional tone at all times."
        "If the user wants to see an image please provide the chess position of that image"
    )

    if context:
        system_message += f"\n\nUse the following context to answer the user's questions:\n{context}"

    # Build messages
    messages = [{"role": "system", "content": system_message}]
    for msg in conversation[-6:]:
        role = "assistant" if msg["role"] == "bot" else "user"
        messages.append({"role": role, "content": msg["Content"]})

    # Send request to GPT
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=400,
        temperature=0.7,
        top_p=0.9,
        tools=tools
    )

    messages = response.choices[0].message

    # Check if GPT wants to call a tool
    print("1")
    # print(messages)
    print("2")
    print(type(messages))
    print(messages.tool_calls)
    if messages.tool_calls !=None:
        for call in messages.tool_calls:
            
            if call.function.name == "GenerateChessImage":
                
                args = json.loads(call.function.arguments)
                
                result = GenerateChessImage(args["opening_name"])
                return {
                        "type": "image",
                        "url": result["image_url"],
                        "text": "Here is the image for opening you want."
                        }
            elif call.function.name=="SuggestStrategy":
                args = json.loads(call.function.arguments)
                result = SuggestStrategy(args["level"])
                return {
                    "type": "text",
                    "Content": result
                }
                

    # Otherwise, return text reply
    print("Before AI Reply ")
    return {
        "type":"text",
        "Content":messages.content.strip()
    }






def ReplyToChat(session_id, conversation_history, type, ai_message=None, Image_url=None, audio_base64=None):
    return func.HttpResponse(
        json.dumps({
            "sessionId": session_id,
            "type": type,
            "text": ai_message,
            "url": Image_url,  
            "history": conversation_history,
            "audioBase64": audio_base64
        }),
        mimetype="application/json"
    )

def ReplyToAdmin(response_data):
    return func.HttpResponse(
        json.dumps(response_data),  
        mimetype="application/json",
        status_code=response_data.get("Status", 200)
    )

def SendReply(Message):
    return func.HttpResponse(
        json.dumps({
            "Message":Message
        }),
        mimetype="application/json"
    )



def TextEmbedding(EmbeddingClient, message):
     query_embedding_resp = EmbeddingClient.embeddings.create(
            model="text-embedding-3-small",
            input=message
        )
        
     return query_embedding_resp.data[0].embedding





def ChunkDocumentEmbeddings(text_chunks, client):
    embeddings = []
    for chunk in text_chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",  
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
    return embeddings



DallE3_Client=DallE3Client()

def GenerateChessImage(opening_name: str):
    result=DallE3_Client.images.generate(
        model="dall-e-3",
        prompt=f"Top-down chessboard setup of the opening: {opening_name}",
        size="1024x1024"
    )
    
    image_url = result.data[0].url
    return {"image_url": image_url}



def SuggestStrategy(level: str) -> str:
    tips = {
        "beginner": "Focus on controlling the center of the board, developing your pieces, and keeping your king safe.",
        "intermediate": "Pay attention to pawn structures, plan your middlegame attacks, and watch for tactical opportunities.",
        "advanced": "Study positional concepts, calculate deeper variations, and anticipate your opponent's strategy."
    }
    return tips.get(level.lower(), "I can provide strategies for beginner, intermediate, or advanced players.")


    