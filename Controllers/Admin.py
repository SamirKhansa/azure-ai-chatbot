
from Services.DocumentIntelligence import extract_text_with_read

from Services.OpenAiServices import ChunkDocumentEmbeddings
from helpers.MessageFormatter import chunkText, AttributesExtraction
from Services.AiSearchServices import UploadingDocumentsAiSearch, DeletingDocument
from Services.CosmosDbServices import UploadingDocumentsToCosmosDB, DeleteDocumentsCosmosDb
from requests_toolbelt.multipart import decoder

def UploadingDocuments(req , content_type,DocumentContainer, DIClient, EmbeddingClient, search_client):

    body = req.get_body()
    multipart_data = decoder.MultipartDecoder(body, content_type)

    file_bytes = None
    resource = None
    Type=None
    UploadedBy=None
    DocumentName=None
    
    file_bytes, resource, Type, UploadedBy, DocumentName=AttributesExtraction(multipart_data, file_bytes, resource, Type, UploadedBy, DocumentName)
    
    
    document_text=extract_text_with_read(DIClient,file_bytes, locale="en")
    
    chunks = chunkText(document_text)
    embeddings = ChunkDocumentEmbeddings(chunks, EmbeddingClient)

    UploadingDocumentsToCosmosDB(DocumentContainer, Type, DocumentName, resource, UploadedBy, document_text)

    UploadingDocumentsAiSearch(search_client,chunks, embeddings, resource, Type, UploadedBy, DocumentName)
    return "File Uploaded Sucessfully"


def DeleteDocument(req_body, DocumentContainer, search_client):
    DeleteDocumentsCosmosDb(DocumentContainer, req_body.get("resource"))
    DeletingDocument(req_body, search_client)
    return "Document deleted Sucessfully!!!"
