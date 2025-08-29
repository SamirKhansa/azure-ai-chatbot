
import json
import azure.functions as func

def AiReply(client, conversation):

    if not conversation:
        conversation = [{"role": "user", "content": "Hello"}]  

    
    messages = [{"role": "system", "content": "You are a helpful chatbot."}]
    
    
    for msg in conversation[-6:]:  
        role = "assistant" if msg["role"] == "bot" else "user"
        messages.append({"role": role, "content": msg["content"]})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=400,
        temperature=0.7,
        top_p=0.9
    )

    return response.choices[0].message.content.strip()



    # return response.choices[0].message.content.strip()


def ReplyToUser(ai_message, session_id, conversation_history):
    return func.HttpResponse(
        json.dumps({
            "sessionId": session_id,
            "reply": ai_message,
            "history": conversation_history
        }),
        mimetype="application/json"
    )



    