# 🛡️ CyberSentinel — Autonomous SOC Analyst

> An AI-powered Security Operations Center (SOC) analyst that uses **RAG pipelines** and **multi-agent AI** to autonomously triage threats, correlate CVEs, and surface actionable intelligence from real-world threat data.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.16-green)](https://langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange)](https://www.trychroma.com/)
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK-red)](https://attack.mitre.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🔍 What Is CyberSentinel?

CyberSentinel is an autonomous threat analysis system designed to simulate how a SOC analyst reasons about security alerts. Instead of relying on manual investigation, it:

- **Ingests** live threat intelligence from MITRE ATT&CK, NVD CVE, and AlienVault OTX
- **Embeds** 3,500+ threat knowledge chunks into a vector database using semantic embeddings
- **Retrieves** relevant context using RAG (Retrieval-Augmented Generation) when an alert fires
- **Reasons** through multi-agent pipelines to classify, correlate, and recommend responses

This project demonstrates real-world application of agentic AI in cybersecurity — an area increasingly adopted by enterprise SOC teams.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       CyberSentinel                         │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  MITRE       │    │  NVD CVE     │    │  AlienVault  │  │
│  │  ATT&CK      │    │  Database    │    │  OTX         │  │
│  │  3,304 chunks│    │  156 chunks  │    │  28 chunks   │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         └──────────────────┬┘──────────────────┘           │
│                            ▼                                │
│                ┌───────────────────────┐                    │
│                │   Data Ingestion      │                    │
│                │   Pipeline            │                    │
│                │   (Phase 1)           │                    │
│                └───────────┬───────────┘                    │
│                            ▼                                │
│                ┌───────────────────────┐                    │
│                │   RAG Pipeline        │                    │
│                │   sentence-transformers│                   │
│                │   + ChromaDB / FAISS  │                    │
│                │   (Phase 2)           │                    │
│                └───────────┬───────────┘                    │
│                            ▼                                │
│                ┌───────────────────────┐                    │
│                │   Multi-Agent System  │                    │
│                │   Triage → Correlate  │                    │
│                │   → Recommend         │                    │
│                │   (Phase 3)           │                    │
│                └───────────┬───────────┘                    │
│                            ▼                                │
│                ┌───────────────────────┐                    │
│                │   FastAPI + Streamlit │                    │
│                │   SOC Dashboard       │                    │
│                │   (Phase 4)           │                    │
│                └───────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
cybersentinel/
├── agents/               # Multi-agent reasoning pipeline (Phase 3)
├── data_loaders/
│   ├── mitre_loader.py   # MITRE ATT&CK STIX ingestion
│   ├── nvd_loader.py     # NVD CVE API ingestion
│   ├── otx_loader.py     # AlienVault OTX threat pulses
│   └── run_all_loaders.py
├── rag/                  # RAG pipeline: embeddings + vector retrieval (Phase 2)
├── requirements.txt
├── env.example           # Environment variable template
├── PHASE1_README.md      # Phase 1 detailed docs
├── SETUP_GUIDE.md        # Full setup walkthrough
└── COMPLETE_BEGINNER_GUIDE.md
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/Poojitha-hub456/Cybersentinal.git
cd Cybersentinal
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp env.example .env
# Add your AlienVault OTX API key to .env
```

Get a free OTX API key at: https://otx.alienvault.com → Settings → API

### 5. Run the data pipeline

```bash
cd data_loaders
python3 run_all_loaders.py
```

Expected output:
```
✓ Loaded 3304 MITRE chunks
✓ Loaded 156 NVD chunks
✓ Loaded 28 OTX chunks
TOTAL: 3,488 chunks → data/chunks/all_chunks_combined.json
```

---

## 📊 Data Sources

| Source | What It Provides | Chunks |
|---|---|---|
| [MITRE ATT&CK](https://attack.mitre.org/) | Techniques, mitigations, threat actor groups (APT28, Lazarus, etc.) | 3,304 |
| [NVD CVE](https://nvd.nist.gov/) | Vulnerability database with CVSS scores and severity ratings | ~156 |
| [AlienVault OTX](https://otx.alienvault.com/) | Community threat pulses, IOCs, active campaigns | ~28 |

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Data Ingestion | `requests`, `langchain`, `pandas` |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector Database | `ChromaDB`, `FAISS` |
| Agent Framework | `LangChain` multi-agent |
| LLM Backend | OpenAI / Anthropic (Phase 3) |
| API Layer | `FastAPI`, `uvicorn` |
| UI | `Streamlit` |

---

## 🗺️ Roadmap

- [x] **Phase 1** — Data ingestion pipeline (MITRE + NVD + OTX)
- [ ] **Phase 2** — RAG pipeline with semantic embeddings + ChromaDB
- [ ] **Phase 3** — Multi-agent threat analysis (Triage → Correlate → Recommend)
- [ ] **Phase 4** — FastAPI backend + Streamlit SOC dashboard

---

## 💡 Why This Project?

Modern SOC teams are overwhelmed — analysts manually cross-reference MITRE techniques, CVE databases, and threat feeds for every alert. CyberSentinel automates that first-pass reasoning layer, the same way real-world AI-powered SIEM tools like CrowdStrike Falcon and Microsoft Sentinel are evolving to do.

This project is built to demonstrate:
- Practical application of RAG in a domain-specific (cybersecurity) context
- Multi-agent coordination for sequential reasoning tasks
- Real API integrations with production threat intelligence sources
- End-to-end pipeline from raw data → deployed intelligent system

---

## 👤 Author

**Poojitha Reddy**
B.Tech Computer Science — Malla Reddy College of Engineering, Hyderabad (2026)

- GitHub: [@Poojitha-hub456](https://github.com/Poojitha-hub456)
- LinkedIn: [linkedin.com/in/poojitha-reddy-6b065a314](https://linkedin.com/in/poojitha-reddy-6b065a314)
- Email: poojithareddy465@gmail.com

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
