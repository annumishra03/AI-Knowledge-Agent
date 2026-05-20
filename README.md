# AI Knowledge Agent

Production-style conversational AI system built using:

- LangGraph
- FastAPI
- ChromaDB
- Groq LLM
- Tavily Search
- Redis Memory

---

# Features

## Conversational AI
- Multi-turn chat memory
- Context-aware conversations

## RAG Pipeline
- PDF upload
- Chunking
- Embedding generation
- ChromaDB vector search

## Agentic AI Workflow
- Dynamic routing
- Tool orchestration
- Conditional graph execution

## Tools
- Web Search Tool
- Direct LLM Response
- Retrieval-Augmented Generation (RAG)

## Memory
- Session-based conversation memory
- Redis-style architecture

---

# Architecture

User Question
↓
Query Rewriter
↓
Router
↓
┌──────────────┬──────────────┬──────────────┐
↓              ↓              ↓              ↓
RAG         Direct         Web         Calculator
↓              ↓              ↓              ↓
Answer Generation
↓
Memory Update

---

# Tech Stack

| Component | Technology |
|---|---|
| API | FastAPI |
| Orchestration | LangGraph |
| LLM | Groq |
| Vector DB | ChromaDB |
| Embeddings | HuggingFace |
| Web Search | Tavily |
| Memory | Redis-style Session Store |

---

# Installation

## Clone Repository

```bash
git clone <repo-url>
cd AI-knowledge-agent
