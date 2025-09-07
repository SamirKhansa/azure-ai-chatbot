
import json
import azure.functions as func

def AiReply(client, conversation, context=None):

    if not conversation:
        conversation = [{"role": "user", "Content": "Hello"}]  

    system_message = (
        "You are a highly knowledgeable and professional chess instructor AI. "
        "Your role is to provide clear, accurate, and insightful guidance on all aspects of chess, "
        "including rules, strategies, tactics, openings, middlegame concepts, and endgames. "
        "You must only respond to questions directly related to chess and politely decline unrelated topics. "
        "Ensure that your explanations are tailored to the user's skill level, whether beginner, intermediate, or advanced, "
        "and maintain a supportive, educational, and professional tone at all times."
    )
    
    
    if context:
        system_message += f"\n\nUse the following context to answer the user's questions:\n{context}"

    messages = [{"role": "system", "content": system_message}]

    
    for msg in conversation[-6:]:
        role = "assistant" if msg["role"] == "bot" else "user"
        messages.append({"role": role, "content": msg["Content"]})

    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=400,
        temperature=0.7,
        top_p=0.9
    )

    return response.choices[0].message.content.strip()





def ReplyToUser(ai_message, session_id, conversation_history):
    return func.HttpResponse(
        json.dumps({
            "sessionId": session_id,
            "reply": ai_message,
            "history": conversation_history
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







    