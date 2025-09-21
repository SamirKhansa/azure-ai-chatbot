from keys import GPT4O_KEY,EMBEDDING_KEY, GPT4O_VERSION, EMBEDDING_VERSION, EMBEDDING_ENDPOINT, GPT4O_ENDPOINT
from config import get_client, get_CosmosDB, SearchClient1, SpeechClient, DIClient
import azure.functions as func
from helpers.ErrorHandling import SystemError
from Services.OpenAiServices import SendReply
from Services.AiSearchServices import DeletingDocument

from Services.CosmosDbServices import PromoteDenoteUsers, DeleteUser
from Controllers.Chat import ChatBot
from Controllers.Admin import UploadingDocuments
from requests_toolbelt.multipart import decoder

from Controllers.Authentication import LogIn, SignUp


ChatContainer = get_CosmosDB(container_name="Sessions", partitionKey="/sessionId")  
UserContainer = get_CosmosDB(container_name="Users", partitionKey="/UserId")  
search_client=SearchClient1()
speechClient=SpeechClient()

GPT4oClient = get_client(KEY=GPT4O_KEY,ENDPOINT=GPT4O_ENDPOINT, VERSION=GPT4O_VERSION )
EmbeddingClient=get_client(KEY=EMBEDDING_KEY, VERSION=EMBEDDING_VERSION, ENDPOINT=EMBEDDING_ENDPOINT)

DIClients = DIClient()

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    print("0")
    
    try:
        print("1")
        content_type = req.headers.get("content-type", "")
        if "multipart/form-data" in content_type:
            print("============================================================================")
            body = req.get_body()
            
            print("3")
            multipart_data = decoder.MultipartDecoder(body, content_type)

            uploaded_file = None
            resource = None
            Type=None
            UploadedBy=None
            DocumentName=None

            # Loop through each part
            for part in multipart_data.parts:
                content_disposition = part.headers.get(b'Content-Disposition', b'').decode()
                if 'name="file"' in content_disposition:
                    uploaded_file = part.content
                if 'name="Resource"' in content_disposition:
                    resource = part.content.decode()
                if('name="Type"' in content_disposition):
                    Type=part.content.decode()
                if('name="UploadedBy"' in content_disposition):
                    UploadedBy=part.content.decode()
                if('name="name"' in content_disposition):
                    DocumentName=part.content.decode()


            if not uploaded_file:
                return func.HttpResponse("No file uploaded", status_code=400)

            if not resource:
                resource = "Unknown Resource"
            UploadingDocuments(uploaded_file, resource,Type,UploadedBy, DocumentName, DIClients, EmbeddingClient, search_client)
            return SendReply("File Uploaded Sucessfully")
    
        req_body = req.get_json()
        route=req.route_params.get('route','')
        
        print("route")
        
        if(route=='Chat'):
            return ChatBot(req_body ,EmbeddingClient, GPT4oClient, speechClient, search_client, ChatContainer)
        elif(route=="Client Uploading document/image"):
            return
        elif(route=="Promote" or route=="Denote"):
            print("i am correct route ",route)
            if(route=="Promote"):
                Role="Admin"
            else:
                Role="User"
            print("email will be printed soon")
            email=req_body.get("email")
            print("I am Role ",Role," Now email ",email)
            Message=PromoteDenoteUsers( UserContainer=UserContainer, emails=email, Role=Role)
            print("Now the message ",Message)
            return SendReply(Message=Message)
        
        elif(route=="DeleteUser"):
            return SendReply(DeleteUser(UserContainer=UserContainer, email=req_body.get("email")))
        elif(route=="Clear Conversation"):
            return
        
        elif(route=="LogIn"):
            return LogIn(UserContainer, req_body, search_client)
        elif(route=="SignUp"):
            return SignUp(UserContainer, req_body)
        
        elif(route=="DeleteDocument"):
            DeletingDocument(req_body=req_body, search_client=search_client)
            return SendReply("Deletion is Sucessfull total number of chunks deleted is ")
        
        
        elif(route=="Face Recognition"):
            return
        






        

    except Exception as e:
        return SystemError(e)
    






        
