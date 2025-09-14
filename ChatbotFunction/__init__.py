from keys import GPT4O_KEY,EMBEDDING_KEY, GPT4O_VERSION, EMBEDDING_VERSION, EMBEDDING_ENDPOINT, GPT4O_ENDPOINT
from config import get_client, get_CosmosDB, SearchClient1, SpeechClient, DIClient
import azure.functions as func
from helpers.ErrorHandling import UserMessageError, SystemError
from Services.OpenAiServices import AiReply, ReplyToUser, TextEmbedding, ChunkDocumentEmbeddings
from helpers.MessageFormatter import FormatConversation, CreateNewId, AddingRefrencesToAiMessage,chunkText
from Services.CosmosDbServices import SaveConversation, ConversationHistory
from Services.AiSearchServices import RetreiveRelevantChunks,UploadingDocuments
from Services.SpeechAPI import text_to_speech, speech_to_text

from Services.DocumentIntelligence import extract_text_with_read
ChatContainer = get_CosmosDB(container_name="Sessions", partitionKey="/sessionId")  
search_client=SearchClient1()
speechClient=SpeechClient()

GPT4oClient = get_client(KEY=GPT4O_KEY,ENDPOINT=GPT4O_ENDPOINT, VERSION=GPT4O_VERSION )
EmbeddingClient=get_client(KEY=EMBEDDING_KEY, VERSION=EMBEDDING_VERSION, ENDPOINT=EMBEDDING_ENDPOINT)

DIClient = DIClient()

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        
        req_body = req.get_json()
        print("Keys in request body:", list(req_body.keys()))
        user_message = req_body.get("message")
        audio_base64 = req_body.get("audioBase64")
        session_id = req_body.get("sessionId")
        print("1")

          
        if audio_base64:
            print("2")
            user_message=speech_to_text(audio_base64, speechClient)
            
        if not user_message:
            print("My fault")
            return UserMessageError()

        if user_message.strip().lower() in ['exit', 'quit', 'bye']:
            return ReplyToUser("Goodbye! Have a nice day 🙂")

        if not session_id:
            session_id = CreateNewId()
        print("2")
        

        conversation, document_id = ConversationHistory(session_id=session_id, container=ChatContainer, user_message=user_message)
        
        
        
        query_embedding = TextEmbedding(EmbeddingClient=EmbeddingClient, message=user_message)
        
        results = RetreiveRelevantChunks(search_client=search_client,query_embedding=query_embedding, top_k=3)
        
        


        
        retrieved_texts = [result["Content"] for result in results]
        
        context_prompt = "\n\n".join(retrieved_texts)
        

        ai_message = AiReply(client=GPT4oClient, conversation=conversation, context=context_prompt)
        audio_base64=text_to_speech(ai_message, speechClient)
        
        ai_message=AddingRefrencesToAiMessage(results=results, ai_message=ai_message)
       


        
        conversation.append({"role": "bot", "Content": ai_message})
        
        SaveConversation(ChatContainer, document_id, session_id, conversation)
        
        conversation_history = FormatConversation(conversation)
        
        
        

        return ReplyToUser(ai_message, session_id, conversation_history,audio_base64)

    except Exception as e:
        return SystemError(e)
    

def UploadingDocuments(file_path, Resource):
    document_text=extract_text_with_read(file_path, locale="en")
    chunks = chunkText(document_text)
    embeddings = ChunkDocumentEmbeddings(chunks, EmbeddingClient)
    UploadingDocuments(search_client,chunks, embeddings, Resource)




        
