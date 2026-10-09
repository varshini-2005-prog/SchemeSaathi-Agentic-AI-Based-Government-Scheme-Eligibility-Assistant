# SchemeSaathi — Agentic Government Scheme Eligibility Assistant 🏛️✨

**SchemeSaathi (திட்டம் சாதி)** is an Agentic AI civic technology platform designed to help citizens discover Tamil Nadu and Central Government welfare schemes they qualify for.

Unlike generic chatbot wrappers that rely on LLM text generation to guess eligibility, SchemeSaathi enforces **deterministic rule evaluation (`PASS`, `FAIL`, `UNKNOWN`)**, **adaptive information collection**, **source claim verification against official Government Orders (G.O.)**, and **counterfactual "What-If" eligibility simulations** in **Tamil (தமிழ்), English, and Tanglish**.

---

## 🌟 Key Differentiating Features

- **🤖 Stateful LangGraph Agent Workflow:** Connects specialized nodes (Input NLU Processor, Adaptive Interviewer, Deterministic Rule Evaluator, Source Verifier, Document Agent, What-If Simulator, and Response Generator).
- **🎯 Adaptive Interviewer:** Asks *only* the minimum follow-up questions required by active candidate schemes. Skips irrelevant questions (e.g., skips agricultural land questions for student candidates).
- **📐 Zero-Hallucination 3-Way Decision Engine:** Every condition is evaluated deterministically against numerical and boolean constraints yielding:
  - 🟢 **ELIGIBLE:** All mandatory rules PASS.
  - 🔴 **NOT ELIGIBLE:** At least one mandatory rule FAILS.
  - 🟡 **NEED MORE INFORMATION:** No rules fail, but required parameters are missing.
- **🛡️ Source Claim Verification:** Cross-references retrieved vector chunks from official Government Orders to verify claims (`VERIFIED` vs `UNVERIFIED`).
- **💡 Counterfactual "What-If" Simulator:** Allows users to simulate profile changes (e.g. *"What if my annual income was ₹2 Lakh?"*) and compare side-by-side eligibility without overwriting their primary stored profile.
- **📄 Document Guidance:** Aggregates required documents and provides step-by-step instructions on procurement channels (e.g., e-Sevai portal, Tahsildar office).

---

## 🏗️ System Architecture & Workflow

```text
                           USER INPUT
            ("Enakku 24 age. Family income 1.8 lakh. 
              Coimbatore-la irukken. Schemes?")
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Input Processor   │ ➔ Detects language ('ta-en')
                     └──────────┬──────────┘   Extracts: age=24, income=180000, district=Coimbatore
                                │
                                ▼
                     ┌─────────────────────┐
                     │Adaptive Interviewer │ ➔ Filters candidates; identifies missing
                     └──────────┬──────────┘   attributes; skips irrelevant questions
                                │
                                ▼
                     ┌─────────────────────┐
                     │Eligibility Reasoner │ ➔ Evaluates PASS/FAIL/UNKNOWN per rule
                     └──────────┬──────────┘   Yields 3-way status: ELIGIBLE / NOT ELIGIBLE / NEED INFO
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Source Verifier   │ ➔ Cross-checks FAISS snippets against official
                     └──────────┬──────────┘   G.O. source (VERIFIED / UNVERIFIED)
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Document & Step Agt │ ➔ Compiles required documents & e-Sevai portal links
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  What-if Simulator  │ ➔ Evaluates counterfactual scenario without modifying
                     └──────────┬──────────┘   permanent profile stored in SQLite
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Response Generator  │ ➔ Formats markdown response with citations & badges
                     └─────────────────────┘
```

---

## 🏛️ Supported Official Government Schemes

| Scheme ID | Scheme Name | Level | Category | Target Audience & Benefits | Key Source Citation |
|---|---|---|---|---|---|
| `TN_SCH_001` | **Pudhumai Penn Scheme** | State (TN) | Women Welfare / Student | Female students from TN Govt Schools | G.O. (Ms) No. 18 (`penkalvi.tn.gov.in`) |
| `TN_SCH_002` | **Tamizh Pudhalvan Scheme** | State (TN) | Student Scholarship | Male students from TN Govt Schools | TN Higher Ed Dept (`tn.gov.in`) |
| `TN_SCH_003` | **Kalaignar Magalir Urimai Thittam (KMUT)** | State (TN) | Women Welfare | Female heads of eligible families (₹1,000/mo) | G.O. (Ms) No. 49 (`kmut.tn.gov.in`) |
| `TN_SCH_004` | **CM Health Insurance (CMCHIS)** | State (TN) | Health Insurance | Families with income ≤ ₹1,20,000/yr (₹5 Lakh cover) | TN Health Dept (`cmchistn.com`) |
| `CENT_SCH_001`| **PM-KISAN** | Central | Farmer Support | Landholding farmer families (₹6,000/yr) | Ministry of Agriculture (`pmkisan.gov.in`) |
| `CENT_SCH_002`| **Indira Gandhi Old Age Pension (IGNOAPS)** | Central-State | Pension | BPL Senior Citizens age ≥ 60 (₹1,000/mo) | NSAP Guidelines (`nsap.nic.in`) |

---

## 📁 Repository Directory Structure

```text
SchemeSaathi/
│
├── app/                        # Python Backend & Agent Modules
│   ├── main.py                 # FastAPI REST server & SPA static mount
│   ├── config.py               # Pydantic configuration loader
│   ├── agents/                 # Specialized Agent Modules
│   │   ├── input_processor.py  # Multi-language NLU parser
│   │   ├── interviewer.py      # Adaptive Interviewer agent
│   │   ├── eligibility.py      # Rule-by-rule Eligibility Reasoner
│   │   ├── verifier.py         # Source Claim Verifier agent
│   │   ├── documents.py        # Required Documents & Steps agent
│   │   ├── what_if.py          # Counterfactual What-if Simulator agent
│   │   └── response_generator.py # Output formatter
│   ├── graph/                  # LangGraph State & Workflow Graph
│   │   ├── state.py            # TypedDict SchemeState
│   │   └── workflow.py         # Compiled StateGraph workflow
│   ├── rag/                    # Ingestion, Embeddings & FAISS Vector Index
│   ├── rules/                  # Rule Evaluator, Parser & Scheme Repository
│   ├── database/               # SQLite connection & session persistence
│   └── utils/                  # Benchmark evaluator & Logger
│
├── frontend/                   # React + TypeScript + Tailwind CSS Frontend
│   ├── src/
│   │   ├── App.tsx             # Main App layout & state router
│   │   ├── components/         # Navbar, Hero, HowItWorks, Catalog, Checker, Results, Simulator, Footer
│   │   ├── services/api.ts     # Type-safe API client
│   │   └── types/scheme.ts     # TypeScript interfaces
│   ├── index.html
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── data/                       # Official Scheme Data & Evaluation Benchmark
│   ├── raw/                    # Official scheme JSON documents
│   └── evaluation/             # 35 benchmark test profiles
│
├── tests/                      # Automated Pytest Test Suite
├── Dockerfile                  # Production container setup
├── requirements.txt            # Python dependencies
└── run.py                      # System startup check launcher
```

---

## 🛠️ Step-by-Step Installation & Usage

### 1. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/varshini-2005-prog/SchemeSaathi-Agentic-AI-Based-Government-Scheme-Eligibility-Assistant.git
cd SchemeSaathi-Agentic-AI-Based-Government-Scheme-Eligibility-Assistant

# Create & activate Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows
source venv/bin/activate      # On Mac/Linux

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Run Production Web Application (FastAPI + React UI)
```powershell
python -m uvicorn app.main:app --reload --port 8000
```
> 🌐 **Web Portal:** [http://localhost:8000](http://localhost:8000)  
> 🌐 **Swagger REST API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Run React Development Server (Optional for Dev Hot Reload)
```powershell
cd frontend
npm install
npm run dev
```
> 🌐 **Vite Dev Server:** [http://localhost:3000](http://localhost:3000)

### 4. Run Automated Test Suite (18 Unit Tests)
```powershell
python -m pytest tests/
```

### 5. Run Docker Container
```powershell
docker build -t schemesaathi .
docker run -p 8000:8000 schemesaathi
```

---

## 📊 Evaluation Metrics Benchmark

| Metric | Measured Score | Target | Status |
|---|---|---|---|
| **Scheme Matching Precision** | **100% (1.00)** | ≥ 90% | ✅ Exceeded |
| **False Eligibility Rate** | **0.0% (0.00)** | ≤ 5% | ✅ Exceeded |
| **Eligibility Accuracy** | **88.0% (0.88)** | ≥ 85% | ✅ Passed |
| **Source Verification Rate** | **100% (1.00)** | 100% | ✅ Passed |
| **Test Execution Speed** | **1.76 seconds (18 tests)** | < 10s | ✅ Passed |

---

## 🛡️ Official Disclaimer

*SchemeSaathi provides informational guidance based on published Government Orders (G.O.) and official portals. It is not an official government service and does not guarantee final scheme approval. Users must verify criteria with official department authorities prior to formal submission.*
