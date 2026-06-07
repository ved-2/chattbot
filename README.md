# LangGraph Persistent Chatbot

A production-ready AI chatbot built using **LangGraph**, **Groq LLM**, **SQLite Persistence**, and **Streamlit**. This chatbot supports conversation memory, resume chat functionality, streaming responses, and a ChatGPT-style sidebar for managing multiple conversations.

---

## 🚀 Features

### 💬 Multi-Chat Support

* Create unlimited chat sessions.
* Each conversation gets a unique LangGraph `thread_id`.
* Switch between chats from the sidebar.

### 🔄 Resume Chat

* Continue any previous conversation.
* Chat history is automatically loaded from LangGraph persistence.
* Conversations remain available even after restarting the application.

### 🧠 Persistent Memory

* Powered by LangGraph's `SqliteSaver`.
* Messages are stored in SQLite.
* AI remembers previous messages within the same thread.

### ⚡ Streaming Responses

* Token-by-token response generation.
* ChatGPT-like typing experience using `st.write_stream()`.

### 📂 Chat Management

* Sidebar displays all conversations.
* Automatically generates titles from the first user message.
* Start a new chat with a single click.

### 💾 SQLite Storage

* Chat messages stored using LangGraph persistence.
* Chat metadata (thread IDs and titles) stored separately.
* No external database required.

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### AI Framework

* LangGraph
* LangChain

### LLM

* Groq
* Llama 3.3 70B Versatile

### Database

* SQLite

### Persistence

* LangGraph SqliteSaver

---

## 📁 Project Structure

```bash
project/
│
├── streamlit_app.py
├── langgraph_backend.py
├── chatbot.db
├── threads.db
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Get your API key from:

https://console.groq.com

---

## ▶️ Run Application

```bash
streamlit run streamlit_app.py
```

---

## 🏗️ How It Works

### Step 1: User Sends Message

```text
User → Streamlit UI
```

### Step 2: LangGraph Workflow Executes

```text
Human Message
       ↓
LangGraph Node
       ↓
Groq LLM
       ↓
AI Response
```

### Step 3: State Saved

LangGraph stores:

```text
Messages
Checkpoints
Thread State
```

inside:

```text
chatbot.db
```

### Step 4: Sidebar Stores Metadata

```text
Thread ID
Chat Title
```

inside:

```text
threads.db
```

### Step 5: Resume Chat

When a user selects a previous conversation:

```text
Sidebar
   ↓
Thread ID
   ↓
LangGraph get_state()
   ↓
Messages Restored
```

---

## 🧩 LangGraph Architecture

```text
START
  │
  ▼
Chatbot Node
  │
  ▼
END
```

### State Definition

```python
class ChatState(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]
```

### Persistence

```python
checkpointer = SqliteSaver(conn)
```

### Compilation

```python
chatbot = builder.compile(
    checkpointer=checkpointer
)
```

---

## 🎯 Benefits of LangGraph Persistence

### Conversation Memory

AI remembers previous messages.

### Resume Chat

Users can continue old conversations.

### Checkpointing

Workflow state is automatically saved.

### Fault Tolerance

Workflows can resume after failures.

### Scalable Architecture

Easy to extend with:

* Tools
* Agents
* RAG
* Multi-Agent Systems
* Human-in-the-Loop

---

## 🔮 Future Improvements

* User Authentication
* Dark/Light Theme Toggle
* Chat Deletion
* Chat Renaming
* Export Chat as PDF
* File Upload Support
* RAG Integration
* Voice Input
* Image Generation
* Multi-Agent Workflows

---

## 📸 Demo Features

✅ New Chat

✅ Resume Chat

✅ Sidebar Navigation

✅ Persistent Memory

✅ Streaming Responses

✅ SQLite Storage

✅ LangGraph Integration

✅ Groq LLM

---

## 👨‍💻 Author

Vedant

Built while learning and exploring LangGraph, Agentic AI, and production-grade conversational AI systems.
