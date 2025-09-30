import uuid
from helpers.MessageFormatter import CreateNewId, SummarizeLongHistory


def SaveConversation(container, document_id, session_id, conversation):
    container.upsert_item({
        "id": document_id,
        "sessionId": session_id,
        "messages": conversation
    })


def ConversationHistory(session_id, container, user_message):
    query = f"SELECT * FROM c WHERE c.sessionId = '{session_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    if items:
        conversation = items[0]["messages"]
        doc_id = items[0]["id"]
    else:
        conversation = []
        doc_id = CreateNewId()
    
    conversation.append({"role": "user", "Content": user_message})
    conversation = SummarizeLongHistory(conversation, max_messages=10)

    return conversation,doc_id




def PromoteDenoteUsers(UserContainer, emails, route):

    try:
        Role="User"
        if(route=="Promote"):
                Role="Admin"
        

        # Query by email since it's not the id
        query = "SELECT * FROM c WHERE c.email = @email"
        params = [{"name": "@email", "value": emails}]
        items = list(UserContainer.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))

        if not items:
            return f"User with email {emails} not found."

        # Take the first matching user
        user = items[0]
        

        # Update the role
        user["role"] = Role
        

        # Replace the document using its id and partition key
        UserContainer.replace_item(item=user["id"], body=user)
        print("User role updated successfully.")

        return f"The user {emails} has successfully been set to {Role}"

    
        
    except Exception as e:
        print("Unexpected error:", e)
        return f"Failed to update user role: {e}"

def DeleteUser(UserContainer, email):
    try:
        print("Searching for user to delete...")

        # Query by email
        query = "SELECT * FROM c WHERE c.email = @email"
        params = [{"name": "@email", "value": email}]
        items = list(UserContainer.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))

        if not items:
            return f"User with email {email} not found."

        # Take the first matching user
        user = items[0]
        print("User found:", user)

        # Delete by id (and partition key if needed)
        UserContainer.delete_item(item=user["id"], partition_key=user["email"])

        return f"The user {email} has been successfully deleted!!"

    except Exception as e:
        return f"Failed to delete user: {str(e)}"



def UploadingDocumentsToCosmosDB(DocumentsContainer,Type ,DocumentName, Resource, UploadedBy, Content):
   new_doc={
       "id":str(uuid.uuid4()),
       "Resource":Resource,
       "documents":DocumentName,
       "UploadedBy":UploadedBy,
       "Type":Type,
       "Content":Content
   } 
   DocumentsContainer.create_item(body=new_doc)


def DeleteDocumentsCosmosDb(container, resource: str):
    print("Deleting documents for resource:", resource)


    # Query items that match the resource
    query = "SELECT c.id, c.documents FROM c WHERE c.Resource=@Resource"
    params = [{"name": "@Resource", "value": resource}]

    items = list(container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))

    print("Found items to delete:", len(items))

    deleted_count = 0
    for item in items:
        # Delete each item using its id and partition key
        container.delete_item(item=item["id"], partition_key=item["documents"])
        deleted_count += 1

    print("Deleted items:", deleted_count)
    return deleted_count



def RetreivingDocuments(Container, DocumentName, Resource):
    query = "SELECT * FROM c WHERE c.documents=@Name AND c.Resource=@Resource"
    params = [
        {"name": "@Name", "value": DocumentName},
        {"name": "@Resource", "value": Resource}
    ]

    items = list(Container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))

    if not items:
        print("Document not found")
        return None

    # Assuming name+resource is unique, return the first match
    document = items[0]
    
    return document




def GetUser(UserContainer, email):
    query = "SELECT * FROM c WHERE c.email=@email"
    params = [{"name": "@email", "value": email}]
    users = list(UserContainer.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))
    
    if not users:
        raise ValueError ("Invalid email or password", 401)
    return users[0]



def GetAllUsers(UserContainer):
    return list(UserContainer.query_items(
            query="SELECT c.name, c.email, c.role FROM c",
            enable_cross_partition_query=True
        ))

def GetAllDocuments(DocumentContainer):
    return list(DocumentContainer.query_items(
            query="SELECT c.documents, c.Type ,c.Resource, c.UploadedBy FROM c",
            enable_cross_partition_query=True
        ))

def CreateUser(UserContainer, user):
    UserContainer.create_item(body=user)


def ClearHistory(ChatContainer, SessionId):
    try:
        # Query all documents with the given sessionId
        query = "SELECT c.id FROM c WHERE c.sessionId = @sessionId"
        params = [{"name": "@sessionId", "value": SessionId}]
        items = list(ChatContainer.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))

        deleted_count = 0
        for item in items:
            ChatContainer.delete_item(item=item['id'], partition_key=SessionId)
            deleted_count += 1

        return "History deleted Sucessfully"

    except ChatContainer.CosmosHttpResponseError as e:
        print(f"Cosmos DB error: {e.message}")
        return 0
