from keys import GPT4O_KEY,EMBEDDING_KEY, GPT4O_VERSION, EMBEDDING_VERSION, EMBEDDING_ENDPOINT, GPT4O_ENDPOINT
from config import get_client, get_CosmosDB
import azure.functions as func
from helpers.ErrorHandling import UserMessageError, SystemError
from Services.OpenAiServices import AiReply, ReplyToUser, TextEmbedding
from helpers.MessageFormatter import FormatConversation, CreateNewId, SummarizeLongHistory, ConversationHistory
from Services.CosmosDbServices import SaveConversation
from Services.CosmosDbServices import RetreiveRelevantChunks




ChatContainer = get_CosmosDB(container_name="Sessions", partitionKey="/sessionId")  
EmbeddingsContainer = get_CosmosDB(container_name="Documents", partitionKey="/id")  


GPT4oClient = get_client(KEY=GPT4O_KEY,ENDPOINT=GPT4O_ENDPOINT, VERSION=GPT4O_VERSION )
EmbeddingClient=get_client(KEY=EMBEDDING_KEY, VERSION=EMBEDDING_VERSION, ENDPOINT=EMBEDDING_ENDPOINT)


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        
        req_body = req.get_json()
        user_message = req_body.get("message")
        session_id = req_body.get("sessionId")  


        if not user_message:
            return UserMessageError

        if user_message.strip().lower() in ['exit', 'quit', 'bye']:
            return ReplyToUser("Goodbye! Have a nice day 🙂")

        if not session_id:
            session_id = CreateNewId()
        

        conversation, document_id = ConversationHistory(session_id=session_id, container=ChatContainer, user_message=user_message)
        
        
        
        query_embedding = TextEmbedding(EmbeddingClient=EmbeddingClient, message=user_message)
        print("0")
        top_chunks = RetreiveRelevantChunks(embeddings_container=EmbeddingsContainer,query_embedding=query_embedding, top_k=3)
        print("1")


        context_prompt = "\n\n".join(top_chunks)
        ai_message = AiReply(client=GPT4oClient, conversation=conversation, context=context_prompt)

        conversation.append({"role": "bot", "content": ai_message})
        SaveConversation(ChatContainer, document_id, session_id, conversation)
        conversation_history = FormatConversation(conversation)
        
        

        return ReplyToUser(ai_message, session_id, conversation_history)

    except Exception as e:
        return SystemError(e)
