from helpers.ChromoDbDocuments import RankingChunks

def SaveConversation(container, document_id, session_id, conversation):
    container.upsert_item({
        "id": document_id,
        "sessionId": session_id,
        "messages": conversation
    })


def RetreiveRelevantChunks(embeddings_container, query_embedding, top_k=3):
    query = "SELECT * FROM c"
    items = list(embeddings_container.query_items(
        query=query,
        enable_cross_partition_query=True  
    ))

    return RankingChunks(query_embedding=query_embedding, top_k=top_k, items=items)