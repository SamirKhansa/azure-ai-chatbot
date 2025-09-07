# Chatbot Architecture Documentation

---

## 1. Overview
This document describes the architecture, data flow, and setup instructions for the Azure OpenAI chatbot implementation. The chatbot is capable of:

- Maintaining persistent conversation history in Cosmos DB

- Retrieving information from documents using RAG (Retrieval-Augmented Generation)

- Processing and extracting content from PDFs, text files, and images using Azure Document Intelligence

- Performing vector similarity search with Azure AI Search to retrieve the most relevant chunks

- Operating with a specific role or prompt to guide responses

- Being deployed to Azure for cloud accessibility

---

## 2. Resources Used
| Resource | Description |
|----------|-------------|
| **Resource Group** | A container that holds all project resources, making them easier to manage and organize. |
| **Function App** | Hosts Python code, accessible via HTTP requests, allowing the chatbot to run independently of a local machine. |
| **CosmosDB** | Hosts chat history that is divided by every user unique session id. Furthermore, this database also hosts the documents with their embeddings.   |
| **Azure AI Foundary Resource** | Contains the GPT-4o deployment, gpt text-embedding and handles AI processing. |
| **GPT-4o Deployment** | AI model that generates responses based on user input and developer-defined prompts. |
| **text-embedding-3-small** | AI model that generates an embedding  based on the text provided. |
| **Azure Document Intelligence** | Extracts text from PDFs, scanned documents, and images, preparing them for chunking and embedding. |
| **Azure AI Search** | Stores document chunks and embeddings, supports similarity (vector) search to retrieve relevant knowledge. |


---

## 3. Architecture Diagram
![Chatbot Architecture](/Assets/Architecturev2.jpg) 


---

## 4. Data Flow and Component Interactions
1. **User → Function App:** The user sends an HTTP request containing their message. 
2. **Function APP -> CosmosDb Resource:** Retrieves previous chat history for the session.
3. **Function App -> Document Intelligence:** Previously, new documents would be uploaded (PDFs, images, handwritten notes), Document Intelligence extracts and cleans the text.
4. **Function App:** The script then divides the text retreived from document intelligence into multiple chunks.
4. **Function App → Embeddings Model (text-embedding-3-small):** Every chunk are converted into embeddings using text-embedding-3-small.
3. **Function App → Azure AI Foundary Resource:** The Function App hosts the code, including prompts that instruct GPT-4o how to respond. Furhtermore, Azure AI Foundary has also deployed a model called text-embedding-3-small to turn text into embedding.  
4. **Azure AI Foundary → text-embedding-3-small:** text-embedding-3-small processes the user message and transforms it into an embedding to be used with the embedding of the chunks. This model is also used when a new document is saved, divided into chunks, turned into an embedding and saved to CosmosDB.  
5. **Azure AI Foundary- AI Search**: The script uses AI Search to retreive the most relavent chunks of document with the prespective of the user question.
6. **Azure AI Foundary → GPT-4o Deployment:** GPT-4o processes the user message, provided chunks of document and prompt to generate a response.  
7. **GPT-4o Deployment → Function App:** The generated response is sent back to the Function App.
8. **GPT-4o Deployment → Chosmos Db:** The generated response is saved in Cosmos DB chatHistory of the user .  
9. **Function App → User:** The Function App returns the response to the user immediately.

---
## 5.Features Implemented
- Persistent chat history stored in Cosmos DB

- Clear conversation or session restart command support

- Prompt customization for system role (topic-specific responses)

- RAG knowledgebase for document-based answers

- Vector similarity search for accurate retrieval

- References to original document sources in chatbot replies

- Deployed solution in Azure for live access
--

## 6. Future Updates
- Enhanced conversational flows and multi-turn context summarization

- Expanded knowledgebase with more documents

- Integration of multi-modal input (images, audio)

- Analytics dashboard to monitor chatbot usage

---

## 7. Setup Instructions

### Prerequisites
- Python 3.10+  
- Azure Portal account  
- Azure CLI  
- Azure Functions Core Tools  
- Azure Resource Group (via VS Code)  
- Git  

### Azure Portal Setup
1. Choose a subscription plan.  
2. Create a **Resource Group**. Ensure all resources are in the same region.  
3. Create an **Azure OpenAI resource** in the same Resource Group and region.  
4. Open **Azure AI Foundry** to deploy the GPT-4o model and text-embedding-3-small.  
5. Create an Azure Document Intelligence resource for extracting text from PDFs, images, and handwritten files.
6. Create an Azure AI Search resource (Basic or Standard tier, not Free) with vector search enabled.
7. Define an index with fields like:
    - id (Edm.String, key)
    - Content (Edm.String, retrievable)
    - resource (Edm.String, retrievable)
    - Embeddings (Collection(Edm.Single), vector field)
8. Create a Cosmos DB resource with database name ChatBot02 and add one container called Sessions with partition key /sessionId.  


### Local Setup
1. Clone the repository:
```
git clone https://github.com/SamirKhansa/azure-ai-chatbot
cd azure-ai-chatbot

```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run the function locally:
```
func start
```
4. Test the function using CLI (curl) or Postman with the endpoint provided by func.

## 7. API Configuration

| Item | Details |
|------|---------|
| **Deployed Endpoint** | `https://<your-function-app>.azurewebsites.net/api/ChatbotFunction` |
| **Local Endpoint** | `http://localhost:7071` (provided by `func start`) |
| **Method** | POST |
| **Headers** | `Content-Type: application/json` |
| **Response Example** | JSON object containing the chatbot reply |
| **Error Handling** | **User Input Error:** Invalid or missing JSON message <br> **System Error:** Backend issues |

### Usage Examples

**Using curl**
```
curl -X POST "https://<your-function-app>.azurewebsites.net/api/ChatbotFunction" \
  -H "Content-Type: application/json" \
  -d '{"message": ""message": "can you tell me a nice fact Kings Gambit?"", "first_interaction": true}'
```
**Expected Response**
```
{
  "sessionId": "08ab8512-7e99-472d-a521-d8507f7c2728",
  "reply": "The \"most favorite\" chess opening can vary depending on the player's style, level of experience, and even trends in the chess world. However, some openings are consistently popular across different levels of play due to their strategic richness, flexibility, and proven effectiveness. Below are some of the most commonly favored openings:\n\n---\n\n### **For White:**\n1. **Ruy-Lopez (Spanish Opening)**:  \n   - Moves: 1.e4 e5 2.Nf3 Nc6 3.Bb5  \n   - Why it's popular: The Ruy-Lopez is one of the oldest and most respected openings in chess. It focuses on rapid development and central control while applying early pressure on Black's position. It offers both sharp and strategic lines, making it appealing to players of all styles.\n\n2. **Italian Game**:  \n   - Moves: 1.e4 e5 2.Nf3 Nc6 3.Bc4  \n   - Why it's popular: Known for its straightforward development and early focus on the center, the Italian Game is ideal for beginners and intermediate players. It can lead to both aggressive attacks and slower, maneuvering battles.\n\n3. **Queen's Gambit**:  \n   - Moves: 1.d4 d5 2.c4  \n   - Why it's popular: The Queen's Gambit is a classical opening that emphasizes central control and long-term positional play. It remains a favorite at all levels, including world championship matches, due to its strategic depth and flexibility.\n\n4. **London System**:  \n   - Moves: 1.d4 followed by 2.Nf3 and 3.Bf4  \n   - Why it's popular: The London System is easy to learn and avoids heavy theoretical preparation. It offers a solid pawn structure and straightforward development, making it a favorite among club players.\n\n5. **English Opening**:  \n   - Moves: 1.c4  \n   - Why it's popular: The English Opening allows\n\nReferences:\nhttps://en.wikipedia.org/wiki/Chess_opening?utm_source=chatgpt.com"
}
```
### 8. Screenshots
- AI response
![AI response](/Assets/ChessOpenings.JPG)
- User Input Irrelivant information
![Irrelivant Information](/Assets/Speciality.JPG)
- User Input Error
![User Error](/Assets/UserError.JPG)
- System Error
![System Error](/Assets/SystemError.JPG)

