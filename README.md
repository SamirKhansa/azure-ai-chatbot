# Chatbot Architecture Documentation

---

## 1. Overview
This document describes the architecture, data flow, and setup instructions for the Azure OpenAI chatbot implementation. The chatbot is capable of:

- Maintaining persistent conversation history in Cosmos DB.
- Retrieving information from documents using RAG (Retrieval-Augmented Generation).
- Processing and extracting content from PDFs, text files, and images using Azure Document Intelligence.
- Performing vector similarity search with Azure AI Search to retrieve the most relevant chunks.
- Accepting **voice input via the browser microphone**, processed through Azure Speech-to-Text.
- Returning **audio from AI messages**, processed through Azure Text-to-Speech.
- Supporting **real-time speech-to-speech conversations** using GPT Realtime API (low-latency streaming audio in and out).
- Operating with a specific role or prompt to guide responses.
- Allowing users to **sign up** and **login**, storing credentials in Cosmos DB.
- Supporting **Clear Chat** to reset conversation history per session.
- Uploading documents to a separate container in Cosmos DB, chunking, and storing in Azure AI Search.
- Viewing and deleting documents from both Cosmos DB and Azure AI Search.
- Retrieving all registered users from a dedicated Cosmos DB container.
- Generating images using **DALL·E 3** when a user requests an image.
- Being deployed to Azure for cloud accessibility.


---

## 2. Resources Used
| Resource | Description |
|----------|-------------|
| **Resource Group** | Container for all project resources. |
| **Function App** | Hosts Python code accessible via HTTP requests, running chatbot logic and AI integrations. |
| **CosmosDB** | Stores chat history, user data, and uploaded documents (different containers for sessions, users, documents). |
| **Azure AI Foundry Resource** | Hosts GPT-4o, GPT-Realtime, and text-embedding models, manages AI processing. |
| **GPT-4o Deployment** | Generates responses to user queries using prompts and retrieved document chunks. |
| **gpt-realtime Deployment** | Handles real-time speech-to-speech interactions via WebSocket streaming. |
| **text-embedding-3-small** | Converts text (user messages or document chunks) into embeddings for vector similarity search. |
| **Azure Document Intelligence** | Extracts text from PDFs, scanned documents, and images for chunking and embeddings. |
| **Azure AI Search** | Stores document chunks and embeddings; supports vector similarity search. |
| **Azure Speech Service** | Converts audio input to text and generates audio output from AI messages. |
| **OpenAI / DALL·E 3** | Generates images based on user prompts through Function calling. |

---

## 3. Architecture Diagram
![Chatbot Architecture](/Assets/V1.6.jpg)

---

## 4. Data Flow and Component Interactions
1. **User → Function App:** Sends a message via HTTP POST or audio in base64.
2. **Function App → Azure Speech Service:** Converts audio to text if input is audio.
3. **Function App → Cosmos DB:** Retrieves previous chat history for the session and/or user login data.
4. **Function App → Document Intelligence:** Admin uploads documents (PDF, images, text); text is extracted.
5. **Function App:** Chunks extracted text into smaller pieces.
6. **Function App → text-embedding-3-small:** Generates embeddings for document chunks and user queries.
7. **Function App → Azure AI Search:** Stores document chunks with embeddings; retrieves relevant chunks for queries.
8. **Function App → GPT-4o Deployment:** Generates responses using retrieved document chunks, user message, and system prompts.
9. **Function App → gpt-realtime Deployment:** Streams user audio to GPT-Realtime via WebSocket, receives real-time audio responses.
10. **GPT-4o / GPT-Realtime → Function App:** Returns AI-generated text/audio response.
11. **Function App → Azure Speech Service:** Converts AI text response to audio (base64) if requested.
12. **Function App → Cosmos DB:** Saves chat history.
13. **Function App → User:** Returns text/audio response.
14. **Function App → Cosmos DB / AI Search:** Handles **ViewDocument** and **DeleteDocument** requests, updating both Cosmos DB and AI Search.
15. **Function App → Cosmos DB:** Handles **user management** for signup, login, and retrieval of all users.
16. **Function App → DALL·E 3:** Generates images on user request via Function calling and returns the image URL/base64.


---

## 5. Features Implemented
- Persistent chat history stored in Cosmos DB.
- Clear chat / session reset command support.
- Prompt customization for system role.
- RAG knowledgebase for document-based answers.
- Vector similarity search for accurate retrieval.
- References to original document sources in chatbot replies.
- Speech-to-Text voice input support.
- Text-to-Speech voice output support.
- **Real-time speech-to-speech** using GPT-Realtime WebSocket streaming.
- **User authentication:** Login and Signup stored in Cosmos DB.
- **Document management:** Upload, view, and delete documents in Cosmos DB and AI Search.
- **Function calling with DALL·E 3** to generate images on user request.
- Deployed solution in Azure for live access.


---

## 6. Future Updates
- Enhanced conversational flows and multi-turn context summarization.
- Expanded knowledgebase with more documents.
- Multi-modal input and output (images, audio, text).
- Analytics dashboard for monitoring usage and user engagement.
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
1. Create a **Resource Group**.
2. Create an **Azure OpenAI** resource and deploy GPT-4o & text-embedding-3-small.
3. Create an **Azure Document Intelligence** resource.
4. Create an **Azure AI Search** resource with vector search enabled.
5. Create a **Cosmos DB** database with multiple containers:
   - `Sessions` → stores chat history per session.
   - `Users` → stores registered users and login credentials.
   - `Documents` → stores uploaded documents and embeddings.
6. Define AI Search index with fields:
   - `id` (Edm.String, key)
   - `Content` (Edm.String, retrievable)
   - `resource` (Edm.String, retrievable)
   - `Embeddings` (Collection(Edm.Single), vector field)

### Local Setup
1. Clone repository:
```bash
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

## 8. API Configuration

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
### 9. Screenshots
- AI response
![AI response](/Assets/ChessOpenings.JPG)
- User Input Irrelivant information
![Irrelivant Information](/Assets/Speciality.JPG)
- User Input Error
![User Error](/Assets/UserError.JPG)
- System Error
![System Error](/Assets/SystemError.JPG)

