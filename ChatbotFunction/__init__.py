from config import get_client,get_CosmosDB
import azure.functions as func
from helpers.ErrorHandling import UserMessageError, SystemError
from Services.OpenAiServices import AiReply, ReplyToUser
from helpers.MessageFormatter import  format_conversation, CreateNewId, manage_context, ConversationHistory
from Services.CosmosDbServices import SaveConversation
import json



container=get_CosmosDB()

client = get_client()

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


        conversation, document_id=ConversationHistory(session_id=session_id, container=container)

        conversation.append({"role": "user", "content": user_message})

        
        conversation = manage_context(conversation, max_messages=10)

        
        
        ai_message = AiReply(client=client, conversation=conversation)  

        
        conversation.append({"role": "bot", "content": ai_message})

        
        SaveConversation(container, document_id, session_id, conversation)

        
        conversation_history = format_conversation(conversation)

        return ReplyToUser(ai_message,session_id, conversation_history)
        

    except Exception as e:
        return SystemError(e)

