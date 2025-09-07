from keys import GPT4O_KEY,EMBEDDING_KEY, GPT4O_VERSION, EMBEDDING_VERSION, EMBEDDING_ENDPOINT, GPT4O_ENDPOINT
from config import get_client, get_CosmosDB, SearchClient1
import azure.functions as func
from helpers.ErrorHandling import UserMessageError, SystemError
from Services.OpenAiServices import AiReply, ReplyToUser, TextEmbedding
from helpers.MessageFormatter import FormatConversation, CreateNewId, AddingRefrencesToAiMessage
from Services.CosmosDbServices import SaveConversation, ConversationHistory
from Services.AiSearchServices import RetreiveRelevantChunks

ChatContainer = get_CosmosDB(container_name="Sessions", partitionKey="/sessionId")  
search_client=SearchClient1()


GPT4oClient = get_client(KEY=GPT4O_KEY,ENDPOINT=GPT4O_ENDPOINT, VERSION=GPT4O_VERSION )
EmbeddingClient=get_client(KEY=EMBEDDING_KEY, VERSION=EMBEDDING_VERSION, ENDPOINT=EMBEDDING_ENDPOINT)


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        
        req_body = req.get_json()
        user_message = req_body.get("message")
        session_id = req_body.get("sessionId")  


        if not user_message:
            return UserMessageError()

        if user_message.strip().lower() in ['exit', 'quit', 'bye']:
            return ReplyToUser("Goodbye! Have a nice day 🙂")

        if not session_id:
            session_id = CreateNewId()
        

        conversation, document_id = ConversationHistory(session_id=session_id, container=ChatContainer, user_message=user_message)
        
        
        
        query_embedding = TextEmbedding(EmbeddingClient=EmbeddingClient, message=user_message)
        
        results = RetreiveRelevantChunks(search_client=search_client,query_embedding=query_embedding, top_k=3)
        
        


        
        retrieved_texts = [result["Content"] for result in results]
        
        context_prompt = "\n\n".join(retrieved_texts)
        

        ai_message = AiReply(client=GPT4oClient, conversation=conversation, context=context_prompt)
        
        ai_message=AddingRefrencesToAiMessage(results=results, ai_message=ai_message)
       


        
        conversation.append({"role": "bot", "Content": ai_message})
        
        SaveConversation(ChatContainer, document_id, session_id, conversation)
        
        conversation_history = FormatConversation(conversation)
        
        
        

        return ReplyToUser(ai_message, session_id, conversation_history)

    except Exception as e:
        return SystemError(e)
