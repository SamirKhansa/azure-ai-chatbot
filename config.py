from openai import AzureOpenAI

from keys import COSMOS_ENDPOINT, COSMOS_KEY, DATABASE_NAME,SEARCH_ENDPOINT,SEARCH_KEY,INDEX_NAME, DI_ENDPOINT, DI_KEY, CONTAINER_NAME
from azure.cosmos import CosmosClient, PartitionKey

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


def get_client(KEY,VERSION,ENDPOINT):
    
    client = AzureOpenAI(
        api_key=KEY,
        api_version=VERSION,
        azure_endpoint=ENDPOINT
    )
    return client
    


def get_CosmosDB(container_name, partitionKey):
    
    client=CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    
    return  database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=partitionKey),
        
    )
    



def SearchClient1():
    
    return SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(SEARCH_KEY)
    )
    


def DIClient():
    
    return DocumentIntelligenceClient(
        endpoint=DI_ENDPOINT,
        credential=AzureKeyCredential(DI_KEY),
    )
   