from openai import AzureOpenAI

from keys import COSMOS_ENDPOINT, COSMOS_KEY, DATABASE_NAME
from azure.cosmos import CosmosClient, PartitionKey

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