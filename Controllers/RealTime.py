from Services.AiSearchServices import RetreiveRelevantChunks
from Services.OpenAiServices import TextEmbedding
from helpers.MessageFormatter import AddingRefrencesToAiMessage
from keys import EMBEDDING_KEY, EMBEDDING_VERSION, EMBEDDING_ENDPOINT
from config import get_client, SearchClient1

EmbeddingClient=get_client(KEY=EMBEDDING_KEY, VERSION=EMBEDDING_VERSION, ENDPOINT=EMBEDDING_ENDPOINT)
search_client=SearchClient1()


def DocumentRealtime(Question):
    Embedding=TextEmbedding(EmbeddingClient, Question)
    results=RetreiveRelevantChunks(search_client=search_client, query_embedding=Embedding)
    
    retrieved_texts = [result["Content"] for result in results]
    
    context_prompt = "\n\n".join(retrieved_texts)
    reply=AddingRefrencesToAiMessage(results=results, ai_message=context_prompt)
    return reply
    
