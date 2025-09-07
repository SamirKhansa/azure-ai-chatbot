def RetreiveRelevantChunks(search_client, query_embedding, top_k=3):
    results = search_client.search(
        search_text="*", 
        vector_queries=[  # notice the list
            {
                "vector": query_embedding,
                "fields": "Embeddings", 
                "k_nearest_neighbors": top_k,
                "kind": "vector",
                
                
            }
        ]
    )
    return list(results)


def UploadingDocuments(search_client, chunks, embeddings, Resource):
    # Extract text using document intelligence
    #Chunk the text into 500 words
    # vectorize every chunk 
    # Upload the the chunks with the document into AI Search
    search_documents = []
    for i, chunk in enumerate(chunks):
        doc = {
            "id": str(i),  # unique ID per chunk
            "Content": chunk, 
            "resource": Resource , # the text chunk
            "Embeddings": embeddings[i]  # corresponding embedding
            
        }
        search_documents.append(doc)
    return search_client.upload_documents(documents=search_documents)
    
