from keys import GPT4O_KEY,EMBEDDING_KEY, GPT4O_VERSION, EMBEDDING_VERSION, EMBEDDING_ENDPOINT, GPT4O_ENDPOINT
from config import get_client, get_CosmosDB, SearchClient1, SpeechClient, DIClient
import azure.functions as func
from helpers.ErrorHandling import SystemError
from Services.OpenAiServices import SendReply, ReplyToAdmin



from Services.CosmosDbServices import PromoteDenoteUsers, DeleteUser, RetreivingDocuments, ClearHistory
from Controllers.Chat import ChatBot
from Controllers.Admin import UploadingDocuments, DeleteDocument



from Controllers.Authentication import LogIn, SignUp


ChatContainer = get_CosmosDB(container_name="Sessions", partitionKey="/sessionId")  

UserContainer = get_CosmosDB(container_name="Users", partitionKey="/UserId")  

DocumentContainer=get_CosmosDB(container_name="Documents", partitionKey="/documents")



search_client=SearchClient1()
speechClient=SpeechClient()

GPT4oClient = get_client(KEY=GPT4O_KEY,ENDPOINT=GPT4O_ENDPOINT, VERSION=GPT4O_VERSION )
EmbeddingClient=get_client(KEY=EMBEDDING_KEY, VERSION=EMBEDDING_VERSION, ENDPOINT=EMBEDDING_ENDPOINT)

DIClients = DIClient()

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
       
        content_type = req.headers.get("content-type", "")

        if "multipart/form-data" in content_type:  #Uploading a document
            return SendReply(UploadingDocuments(req,content_type, DocumentContainer, DIClients, EmbeddingClient, search_client))
    
        req_body = req.get_json()
        route=req.route_params.get('route','')
        
        if(route=='Chat'):
            return ChatBot(req_body ,EmbeddingClient, GPT4oClient, speechClient, search_client, ChatContainer)
        
        elif(route=="Promote" or route=="Denote"):
            return SendReply(PromoteDenoteUsers( UserContainer, req_body.get("email"), route))
        
        elif(route=="DeleteUser"):
            return SendReply(DeleteUser(UserContainer=UserContainer, email=req_body.get("email")))
        
        elif(route=="ViewDocument"):
            return ReplyToAdmin(RetreivingDocuments(DocumentContainer, req_body.get("name"), req_body.get("resource")))
        
        elif(route=="LogIn"):
            return LogIn(UserContainer,DocumentContainer ,req_body, search_client)
        
        elif(route=="SignUp"):
            return SendReply(SignUp(UserContainer, req_body))
        
        elif(route=="DeleteDocument"):
            return SendReply(DeleteDocument(req_body, DocumentContainer, search_client))
        elif(route=="ClearHistory"):
            return SendReply(ClearHistory(ChatContainer, req_body.get("SessionId")))
        return SendReply("No message has returned")
        
        
        






        

    except Exception as e:
        print("Error ",e)
        return SystemError(e)
    






        
