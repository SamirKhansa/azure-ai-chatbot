import uuid
def RetreiveRelevantChunks(search_client, query_embedding, top_k=3):
    results = search_client.search(
        search_text="*", 
        vector_queries=[  
            {
                "vector": query_embedding,
                "fields": "Embeddings", 
                "k_nearest_neighbors": top_k,
                "kind": "vector",
                
                
            }
        ]
    )
    return list(results)


def UploadingDocumentsAiSearch(search_client, chunks, embeddings, Resource,Type, UploadedBy, DocumentName):
    search_documents = []
    for i, chunk in enumerate(chunks):
        doc = {
            "id":str(uuid.uuid4()),  # unique ID per chunk
            "Content": chunk, 
            "resource": Resource ,
            "Type":Type,
            "UploadedBy":UploadedBy,
            "Name":DocumentName,
            "Embeddings": embeddings[i]  # corresponding embedding
            
        }
        search_documents.append(doc)
    return search_client.upload_documents(documents=search_documents)


def DeletingDocument(req_body, search_client):
    
    resource=req_body.get("resource")
    DocumentName=req_body.get("DocumentName")
    results = search_client.search(
        search_text="*",
        filter=f"resource eq '{resource}'"
    )
    doc_ids_to_delete = [doc['id'] for doc in results]
    if doc_ids_to_delete:
        search_client.delete_documents(documents=[{"id": id} for id in doc_ids_to_delete])
    return len(doc_ids_to_delete)
    

    
