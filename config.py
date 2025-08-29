from openai import AzureOpenAI

from keys import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_VERSION, COSMOS_ENDPOINT, COSMOS_KEY, DATABASE_NAME, CONTAINER_NAME
from azure.cosmos import CosmosClient, PartitionKey

def get_client():
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_KEY,
        api_version=AZURE_OPENAI_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )
    return client


def get_CosmosDB():
    client=CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    
    return  database.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key=PartitionKey(path="/sessionId"),
        
    )