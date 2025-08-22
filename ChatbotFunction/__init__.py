from config import get_client
import azure.functions as func
from helpers.ErrorHandling import UserMessageError, SystemError
from Services.OpenAiServices import AiReply, ReplyToUser
from helpers.MessageFormatter import FormatMessage,GreetingMessage

# Initialize the AzureOpenAI client with your deployment details
client = get_client()


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        user_message = req_body.get("message")

        if not user_message:
            return UserMessageError
        
        if user_message.strip().lower() in ['exit', 'quit', 'bye']:
            return ReplyToUser("Goodbye! Have a nice day 🙂")
        

        greeting=GreetingMessage(req_body=req_body)
        
        ai_message = AiReply(client=client, user_message=user_message)

        full_message = FormatMessage(Greetings=greeting, aiMessage=ai_message)

        return ReplyToUser(full_message)

    except Exception as e:
        return SystemError(e)
