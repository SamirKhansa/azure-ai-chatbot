
from Services.DocumentIntelligence import extract_text_with_read

from Services.OpenAiServices import ChunkDocumentEmbeddings
from helpers.MessageFormatter import chunkText
from helpers.ErrorHandling import UserMessageError
from Services.AiSearchServices import UploadingDocumentsAiSearch



def UploadingDocuments(file_bytes, Resource,Type,UploadedBy, DocumentName, DIClient, EmbeddingClient, search_client):
    print("Theoratically it should work from here!!!")
    
    if not file_bytes:
        return UserMessageError("No file uploaded")
    
    document_text=extract_text_with_read(DIClient,file_bytes, locale="en")
    chunks = chunkText(document_text)
    embeddings = ChunkDocumentEmbeddings(chunks, EmbeddingClient)
    UploadingDocumentsAiSearch(search_client,chunks, embeddings, Resource, Type, UploadedBy, DocumentName)


