# SchemeSaathi — Tamil + English Agentic Government Scheme Eligibility Assistant 🏛️

**SchemeSaathi (திட்டம் சாதி)** is an Agentic AI system designed to help users discover Tamil Nadu and Central Government scheme eligibility with multi-language (Tamil, English, Tanglish) capabilities, adaptive interviewing, deterministic rule evaluation, source claim verification, required document guidance, and what-if eligibility simulation.

---

## 🚀 Complete Architectural Roadmap (Phases 1 - 15)

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Project Structure, Venv, Configuration, Database & Health Setup | ✅ Completed |
| **Phase 2** | Official Scheme Document Collection (6 Schemes) | ✅ Completed |
| **Phase 3** | PDF & Text Document Ingestion Pipeline | ✅ Completed |
| **Phase 4** | FAISS & Multilingual Embedding Retrieval Setup | ✅ Completed |
| **Phase 5** | Structured Scheme Rule JSON Representation & Evaluator | ✅ Completed |
| **Phase 6** | LangGraph State & Profile Management System | ✅ Completed |
| **Phase 7** | Adaptive Interviewer Agent | ✅ Completed |
| **Phase 8** | Deterministic Rule-by-Rule Eligibility Engine | ✅ Completed |
| **Phase 9** | Source Claim Verification Agent | ✅ Completed |
| **Phase 10** | Document Guidance & Next-Step Agent | ✅ Completed |
| **Phase 11** | What-if Eligibility Simulator | ✅ Completed |
| **Phase 12** | Tamil, English & Tanglish Natural Language NLU Engine | ✅ Completed |
| **Phase 13** | Interactive Streamlit Frontend & FastAPI Backend Server | ✅ Completed |
| **Phase 14** | Benchmark Evaluation Dataset & Precision/Recall Metrics | ✅ Completed |
| **Phase 15** | Containerization (Dockerfile) & Deployment Readiness | ✅ Completed |

---

## 🏗️ Core Agent Workflow Architecture

```text
                         USER INPUT (Tamil / English / Tanglish)
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │   Input Processor   │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │Adaptive Interviewer │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │Eligibility Reasoner │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │   Source Verifier   │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Document & Step Agt │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │  What-if Simulator  │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Response Generator  │
                                └─────────────────────┘
```

---

## 🛠️ Setup & Execution Guide

### 1. Virtual Environment Activation
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
python -m pytest tests/
```

### 4. Launch Interactive Streamlit UI
```bash
streamlit run frontend/streamlit_app.py
```

### 5. Launch FastAPI Backend Server
```bash
uvicorn app.main:app --reload --port 8000
```

---

## 🎯 Comprehensive Interview Q&A Guide

### Q: Why LangGraph instead of standard LangChain chains or generic LLM prompts?
> **Answer:** Standard LLM chains execute linearly and lack structured control over state persistence. LangGraph enables graph-based state management, cyclic execution loops for multi-turn adaptive interviewing, strict deterministic node boundaries, and explicit state checkpointing in SQLite.

### Q: Why not let the LLM directly decide eligibility?
> **Answer:** LLMs suffer from reasoning hallucinations and non-deterministic numerical errors (e.g. confusing ₹2.5 lakh with ₹250,000). SchemeSaathi uses an explicit deterministic Rule Evaluator (`PASS`, `FAIL`, `UNKNOWN`) over structured JSON rules, guaranteeing zero numerical hallucinations and 100% false-eligibility protection.

### Q: How does the What-if Simulator work without mutating user profile?
> **Answer:** When a what-if query is detected (e.g. *"What if my income was 2 lakh?"*), the agent creates a temporary state copy, applies the counterfactual profile modifications, re-evaluates the candidate schemes, computes a delta comparison report, and returns the result without overwriting the user's permanent profile stored in SQLite.

### Q: How does the Source Verifier prevent fake rules?
> **Answer:** The Verifier Agent queries the FAISS vector database using the scheme ID and evaluates whether official Government Order (G.O.) text snippets back the eligibility claim before presenting it to the user.
