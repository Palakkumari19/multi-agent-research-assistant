# Multi-Agent Research Assistant

An AI-powered autonomous research system that uses multiple collaborating AI agents to perform structured research, critique findings, and generate professional research reports.

Built using LangGraph, Groq, Tavily, MongoDB Atlas, FAISS, and Streamlit.

---

# Live Demo

🚀 Deployed Application:  
https://YOUR-STREAMLIT-APP.streamlit.app

---

# Overview

This project simulates a real-world multi-agent AI workflow where specialized agents collaborate to:

- break down complex research queries
- retrieve relevant web information
- critique research quality
- generate structured reports
- maintain persistent research history

The system demonstrates concepts used in modern AI engineering systems such as:
- autonomous agents
- orchestration pipelines
- retrieval-augmented generation (RAG)
- semantic memory
- persistent AI workflows

---

# Multi-Agent Workflow

```text
User Query
    │
    ▼
┌─────────────┐
│ Planner     │
│ Agent       │
│ Breaks the  │
│ query into  │
│ research    │
│ subtopics   │
└──────┬──────┘
       ▼
┌─────────────┐
│ Researcher  │
│ Agent       │
│ Performs    │
│ Tavily web  │
│ search and  │
│ retrieval   │
└──────┬──────┘
       ▼
┌─────────────┐
│ Critic      │
│ Agent       │
│ Evaluates   │
│ completeness│
│ and quality │
└──────┬──────┘
       ▼
┌─────────────┐
│ Writer      │
│ Agent       │
│ Generates   │
│ final       │
│ report      │
└─────────────┘
```

---

# Key Features

## Multi-Agent Orchestration
Uses LangGraph to coordinate specialized AI agents in a sequential workflow.

## Autonomous Research Planning
Planner Agent automatically decomposes research topics into focused subquestions.

## Web-Augmented Research
Researcher Agent uses Tavily API for real-time web retrieval.

## AI Critique System
Critic Agent evaluates research quality and identifies missing areas.

## Persistent Cloud Memory
MongoDB Atlas stores:
- previous research sessions
- reports
- findings
- critiques

## Semantic Memory Retrieval
FAISS vector search retrieves semantically similar past research.

## Professional Report Generation
Writer Agent generates:
- structured markdown reports
- technical summaries
- formatted research outputs

## PDF Export
Users can download generated reports as PDFs.

## Streamlit UI
Interactive frontend with:
- research history sidebar
- delete chat functionality
- new chat creation
- expandable findings
- clean minimal interface

---

# Tech Stack

| Technology | Purpose |
|---|---|
| LangGraph | Multi-agent orchestration |
| LangChain | LLM workflow integration |
| Groq API | Fast LLM inference |
| Tavily API | AI-powered web search |
| MongoDB Atlas | Persistent cloud memory |
| FAISS | Semantic vector retrieval |
| Streamlit | Frontend interface |
| ReportLab | PDF generation |

---

# Example Workflow

### User Query

```text
Summarize recent research trends in RAG systems for enterprise AI applications.
```

### System Output

- Research Plan
- Web Research Findings
- Critic Analysis
- Final Research Report
- PDF Export

---

# Screenshots

## Research Workflow

_Add screenshot here_

---

## Final Research Report

_Add screenshot here_

---

## Sidebar Research Memory

_Add screenshot here_

---

# Engineering Highlights

- Implemented stateful multi-agent orchestration using LangGraph
- Designed modular AI agent architecture
- Built persistent AI memory using MongoDB Atlas
- Integrated semantic retrieval using FAISS
- Developed autonomous research refinement workflow
- Optimized prompt engineering for multi-step reasoning
- Deployed full-stack AI application using Streamlit Cloud

---

# Challenges Solved

- Managing multi-agent state transitions
- Handling LLM token limitations
- Persistent research memory design
- Research result structuring and formatting
- Cloud deployment and API management
- Prompt optimization for autonomous workflows

---

# Future Improvements

- Citation-aware report generation
- Streaming agent responses
- Multi-user authentication
- Agent reasoning visualization
- Research report versioning
- Advanced semantic memory ranking
- Real-time collaborative research

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/Palakkumari19/multi-agent-research-assistant.git

cd multi-agent-research-assistant
```

---

## Create Virtual Environment

### macOS / Linux

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

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Secrets

Create `.streamlit/secrets.toml`

```toml
GROQ_API_KEY="your_groq_api_key"

TAVILY_API_KEY="your_tavily_api_key"

MONGO_URI="your_mongodb_connection_string"
```

---

## Run Application

```bash
streamlit run app.py
```

---

# Author

Palak Kumari

GitHub:  
https://github.com/Palakkumari19

LinkedIn:  
https://www.linkedin.com/in/palak-kumari-828779200/