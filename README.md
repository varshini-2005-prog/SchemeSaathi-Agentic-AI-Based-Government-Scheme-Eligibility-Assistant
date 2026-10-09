# SchemeSaathi — Agentic Government Scheme Eligibility Assistant 🏛️✨

**SchemeSaathi (திட்டம் சாதி)** is an Agentic AI civic‑technology platform that helps citizens discover Tamil Nadu & Central Government welfare schemes they are eligible for—in Tamil, English, and Tanglish.

## 🌟 Why SchemeSaathi is Different
- **Deterministic rule evaluation** (`PASS / FAIL / UNKNOWN`) – no hallucinations.
- **Adaptive interviewer** – asks only the minimal follow‑up questions required.
- **Source claim verification** – cross‑checks official Government Orders (G.O.).
- **What‑If simulator** – lets users tweak profile data and instantly see eligibility changes.
- **Multi‑language NLU** – supports Tamil, English, and Tanglish inputs.

## 📁 Repository Layout
```
SchemeSaathi/
│
├─ app/                # FastAPI backend + LangGraph agents
│   ├─ main.py
│   ├─ config.py
│   ├─ agents/ …
│   └─ …
│
├─ frontend/           # React + TypeScript + Tailwind UI
│   ├─ src/
│   │   ├─ App.tsx
│   │   ├─ components/ (Navbar, Hero, Catalog, Checker, Results, Simulator, Footer)
│   │   └─ services/api.ts
│   └─ vite.config.ts
│
├─ data/               # Raw scheme data & evaluation benchmark
├─ tests/              # Pytest suite
├─ Dockerfile
├─ requirements.txt
└─ run.py
```

## 🛠️ Installation & Development
### Backend (FastAPI)
```powershell
# Clone the repo
git clone https://github.com/varshini-2005-prog/SchemeSaathi-Agentic-AI-Based-Government-Scheme-Eligibility-Assistant.git
cd SchemeSaathi-Agentic-AI-Based-Government-Scheme-Eligibility-Assistant

# Python virtual environment
python -m venv venv
.\\venv\\Scripts\\Activate.ps1   # Windows

# Install dependencies
pip install -r requirements.txt

# Run dev server
python -m uvicorn app.main:app --reload --port 8000
```
Visit **http://localhost:8000** (Swagger at `/docs`).

### Frontend (React)
```powershell
cd frontend
npm install
npm run dev   # → http://localhost:3000
```
The UI talks to the backend via `services/api.ts` (base URL `http://localhost:8000`).

### Test Suite
```powershell
cd ..
python -m pytest tests/
```

## 📦 Production Docker Image
The repository includes a multi‑stage Dockerfile that builds the React UI and serves it together with FastAPI.
```bash
# Build the image
docker build -t schemesaathi .
# Run the container
docker run -d -p 8000:8000 schemesaathi
```
Open **http://localhost:8000** – the React app is served as static files.

## 🚀 Deploy to Render (Docker)
1. Create a new **Web Service** on Render.
2. Connect your GitHub repository (the branch `redesign-react-ui`).
3. Choose **Docker** as the environment.
4. Render will automatically detect the Dockerfile.
5. Set the **Start Command** to:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
6. Deploy – Render will build the image and expose a public URL.

## 🛡️ Disclaimer
*SchemeSaathi provides informational guidance based on published Government Orders and official portals. It is not an official government service and does not guarantee final scheme approval. Users must verify criteria with official department authorities prior to formal submission.*
