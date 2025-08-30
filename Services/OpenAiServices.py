
import json
import azure.functions as func

def AiReply(client, conversation, context=None):

    if not conversation:
        conversation = [{"role": "user", "content": "Hello"}]  

    system_message = "You are a helpful chatbot that is specialized as a chess instructor, you only answer questions related to chess."
    
    
    if context:
        system_message += f"\n\nUse the following context to answer the user's questions:\n{context}"

    messages = [{"role": "system", "content": system_message}]

    
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


def UploadingDocuments(EmbeddingClient,EmbeddingsContainer,file_path):
    from helpers.MessageFormatter import ExtractTextFromPDF, chunkText
    document_text=ExtractTextFromPDF(file_path)
    chunks =chunkText(document_text)
    embeddings=ChunkDocumentEmbeddings(chunks, EmbeddingClient)
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        EmbeddingsContainer.upsert_item({
            "id": f"chunk_{i}",
            "text": chunk,
            "embedding": embedding,
            "metadata": {
                "document": "The Journey of Jane Doe.pdf"
            }
        })


    