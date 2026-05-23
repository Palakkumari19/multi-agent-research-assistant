# 🤖 Multi-Agent Research Assistant

An autonomous AI-powered research assistant built using LangGraph, Groq, Tavily, MongoDB Atlas, and FAISS.

This system uses multiple specialized AI agents that collaborate together to:
- plan research
- perform web retrieval
- critique findings
- generate structured reports
- store long-term memory
- retrieve semantically similar past research

---

# 🚀 Features

## 🧠 Multi-Agent Architecture
The system consists of multiple autonomous agents:

- Planner Agent
- Researcher Agent
- Critic Agent
- Writer Agent

Each agent has a specialized responsibility and collaborates through a shared LangGraph state.

---

## 🌐 Web Research
Uses Tavily Search API for:
- AI-optimized web search
- retrieval of recent information
- structured search results

---

## 🧠 Persistent Memory
MongoDB Atlas stores:
- past research reports
- research history
- timestamps
- session memory

---

## 🔍 Semantic Memory Retrieval
FAISS + Sentence Transformers provide:
- semantic similarity search
- retrieval of related past research
- memory augmentation

---

## ⚡ Fast LLM Inference
Powered by Groq using:
- Llama 3.3 70B Versatile

---

# 🏗️ System Architecture

```text
User Query
   ↓
Memory Retrieval
   ↓
Planner Agent
   ↓
Researcher Agent
   ↓
Critic Agent
   ↓
Writer Agent
   ↓
Final Research Report
   ↓
MongoDB + FAISS Memory Storage
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| LangGraph | Multi-agent orchestration |
| LangChain | LLM application framework |
| Groq API | LLM inference |
| Tavily API | Web search |
| MongoDB Atlas | Persistent memory |
| FAISS | Vector similarity search |
| Sentence Transformers | Embeddings |
| Streamlit | Frontend |

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-research-assistant.git

cd multi-agent-research-assistant
```

---

## 2. Create Virtual Environment

### Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_key

TAVILY_API_KEY=your_key

MONGO_URI=your_mongodb_connection
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 🧪 Example Queries

- Summarize recent AI research on RAG systems
- Compare modern AI agent frameworks
- Explain recent advancements in multimodal AI
- Analyze latest developments in open-source LLMs

---

# 📌 Future Improvements

- Real-time streaming responses
- Multi-user sessions
- PDF export
- Citation support
- Agent execution visualization
- LangSmith observability integration

---

# 👩‍💻 Author

Palak Kumari