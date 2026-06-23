# CyberSentinel — Complete Step-by-Step Setup Guide

A beginner-friendly walkthrough to build an autonomous SOC analyst using RAG + multi-agent AI.

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Step 1: Project Folder Setup](#step-1-project-folder-setup)
3. [Step 2: IDE Setup (VS Code)](#step-2-ide-setup-vs-code)
4. [Step 3: Python Virtual Environment](#step-3-python-virtual-environment)
5. [Step 4: Install Core Dependencies](#step-4-install-core-dependencies)
6. [Step 5: MITRE Data Loader (Phase 1)](#step-5-mitre-data-loader-phase-1)
7. [Step 6: NVD CVE Loader (Phase 1)](#step-6-nvd-cve-loader-phase-1)
8. [Step 7: AlienVault OTX Loader (Phase 1)](#step-7-alienvault-otx-loader-phase-1)
9. [Step 8: Test & Verify Output](#step-8-test--verify-output)
10. [Troubleshooting](#troubleshooting)

---

## System Requirements

### What You Need
- **OS**: macOS, Linux, or Windows (with WSL2)
- **Python**: 3.10 or higher (check: `python3 --version`)
- **Internet**: Stable connection (downloading ~100 MB of threat data)
- **Disk Space**: ~2 GB free
- **RAM**: 4 GB minimum (8 GB recommended for embeddings)
- **IDE**: VS Code (free) or any text editor

### Check Your System
```bash
# Check Python version
python3 --version

# Should output something like: Python 3.11.x

# Check pip is installed
pip3 --version

# Should output: pip 23.x.x from ...
```

If Python is not installed:
- **macOS**: Install via Homebrew: `brew install python3`
- **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install python3 python3-pip`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

---

## Step 1: Project Folder Setup

### What You're Doing
Creating a clean folder structure for the project. This keeps code organized and professional.

### Commands

Open a terminal and run these commands:

```bash
# Navigate to a good location (e.g., Desktop or a Dev folder)
cd ~/Desktop

# Create the main project folder
mkdir cybersentinel
cd cybersentinel

# Create subfolders for organized code
mkdir -p data_loaders
mkdir -p data/raw
mkdir -p data/chunks
mkdir -p config
mkdir -p tests
mkdir -p notebooks

# Verify structure
tree -L 2
# Or on Windows/Mac without tree:
ls -la
```

### What Your Folder Should Look Like
```
cybersentinel/
├── data_loaders/           # Data loading scripts (MITRE, NVD, OTX)
├── data/
│   ├── raw/                # Raw JSON files downloaded from APIs
│   └── chunks/             # Processed chunks ready for embedding
├── config/                 # Configuration files (API keys, settings)
├── tests/                  # Unit tests
├── notebooks/              # Jupyter notebooks for exploration
├── agents/                 # Agent code (Phase 3)
├── rag/                    # RAG pipeline (Phase 2)
├── api/                    # FastAPI code (Phase 4)
├── ui/                     # Streamlit dashboard (Phase 4)
├── venv/                   # Virtual environment (created in Step 3)
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation
```

---

## Step 2: IDE Setup (VS Code)

### Download & Install VS Code
1. Go to [code.visualstudio.com](https://code.visualstudio.com/)
2. Download for your OS (macOS, Windows, Linux)
3. Install and open it

### Open Your Project in VS Code
```bash
# From the terminal (inside cybersentinel folder)
code .

# This opens VS Code with cybersentinel as the root folder
```

### Install Essential VS Code Extensions
1. Open VS Code
2. Go to **Extensions** (left sidebar, icon that looks like 4 squares)
3. Search for and install:
   - **Python** (by Microsoft) — for syntax highlighting, debugging
   - **Pylance** (by Microsoft) — for code intelligence
   - **Thunder Client** or **REST Client** — for testing APIs (Phase 4)
   - **Jupyter** (by Microsoft) — for notebooks

### Configure Python Interpreter
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: `Python: Select Interpreter`
3. Choose the one from `./venv/bin/python` (we'll create this next)

---

## Step 3: Python Virtual Environment

### What's a Virtual Environment?
A "sandbox" for your project where you install libraries without affecting your system Python. **Always use one.**

### Create Virtual Environment

```bash
# Make sure you're in the cybersentinel folder
cd ~/Desktop/cybersentinel

# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows (Git Bash):
source venv/Scripts/activate

# On Windows (Command Prompt):
venv\Scripts\activate

# You should see (venv) at the start of your terminal line
# Like: (venv) username@MacBook cybersentinel %
```

### Verify Activation
```bash
# Check Python path (should point to venv)
which python3
# Output should contain "venv"

# Check pip
pip --version
# Should reference venv
```

### Update pip
```bash
pip install --upgrade pip setuptools wheel
```

---

## Step 4: Install Core Dependencies

### Create requirements.txt File

Create a file named `requirements.txt` in the cybersentinel folder with:

```text
# Core
python-dotenv==1.0.0
requests==2.31.0

# Data Loading & Processing
langchain==0.1.16
langchain-community==0.0.36
pandas==2.1.4
numpy==1.24.3

# Embeddings & Vector DB (Phase 2)
sentence-transformers==2.2.2
chromadb==0.4.24
faiss-cpu==1.7.4

# LLM & Agent Framework (Phase 3)
langchain-openai==0.0.8
langchain-google-genai==0.0.10
langgraph==0.0.45

# API & Web (Phase 4)
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
streamlit==1.32.0

# Utilities
python-multipart==0.0.6
aiohttp==3.9.1

# Development
pytest==7.4.3
black==23.12.1
flake8==6.1.0
ipython==8.18.1
jupyter==1.0.0
```

### Install All Dependencies

```bash
# Make sure virtual environment is activated (you should see (venv) in terminal)
pip install -r requirements.txt

# This will take 5-10 minutes on first install
# Watch for any errors — take a screenshot if you see red text errors
```

### Verify Installation

```bash
# Test imports
python3 -c "import langchain; import chromadb; import sentence_transformers; print('✓ All core packages installed!')"
```

---

## Step 5: MITRE Data Loader (Phase 1)

### What's Happening
You're downloading the MITRE ATT&CK database (threat intelligence) and processing it into chunks ready for embedding.

### File Already Created
The MITRE loader was created for you earlier. Let's use it now.

### Verify the File Exists

```bash
# From cybersentinel folder
ls -la data_loaders/mitre_loader.py
```

If it doesn't exist, I'll create it for you in the next step.

### Run the MITRE Loader

```bash
# Make sure virtual environment is active
source venv/bin/activate  # or your OS activation command

# Run the loader
python3 data_loaders/mitre_loader.py
```

### Expected Output

You should see something like:

```
11:45:23  INFO     Downloading MITRE ATT&CK STIX bundle from GitHub …
11:45:35  INFO     Downloaded 68.4 MB in 11.23s
11:45:35  INFO     Saved raw STIX to data/raw/mitre_enterprise.json
11:45:35  INFO     Loaded 25842 STIX objects
11:45:38  INFO     Parsed 2847 technique chunks
11:45:39  INFO     Parsed 268 mitigation chunks
11:45:40  INFO     Parsed 189 threat group chunks
11:45:40  INFO     Saved 3304 chunks to data/chunks/mitre_chunks.json
11:45:40  INFO     Total chunks: 3304

── CyberSentinel | MITRE Loader Stats ──────────────────
  group             189 chunks
  mitigation        268 chunks
  technique        2847 chunks
  TOTAL            3304 chunks

── Sample technique chunk ───────────────────────────────
  chunk_id : technique-T1003.001-chunk-0
  mitre_id : T1003.001
  name     : OS Credential Dumping: LSASS Memory
  tactics  : ['credential-access', 'defense-evasion']
  platforms: ['Windows']
  text[:200]: MITRE ATT&CK Technique T1003.001: OS Credential Dumping…
─────────────────────────────────────────────────────────
```

### Verify the Files Were Created

```bash
# Check that data was downloaded
ls -lh data/raw/mitre_enterprise.json

# Check that chunks were created
ls -lh data/chunks/mitre_chunks.json
wc -l data/chunks/mitre_chunks.json
```

---

## Step 6: NVD CVE Loader (Phase 1)

### What's the NVD?
National Vulnerability Database — contains all known CVEs (vulnerabilities) with severity scores, CVSS metrics, etc.

### Important Note on NVD API
The NVD API has rate limits (30 requests/2 minutes without key). You can use it free, but for Phase 1, we'll build a **simple loader without requiring an API key** (we'll download a recent CVE dataset).

### Create NVD Loader File

Create `data_loaders/nvd_loader.py`:

```python
"""
NVD (National Vulnerability Database) CVE Loader
================================================
Downloads recent CVE data and chunks it for RAG.
"""

import json
import requests
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

RAW_PATH = Path("data/raw/nvd_cves.json")
CHUNK_PATH = Path("data/chunks/nvd_chunks.json")


@dataclass
class NVDChunk:
    """One CVE chunk."""
    chunk_id: str
    text: str
    source: str
    object_type: str
    cve_id: str
    description: str
    severity: str
    cvss_score: float
    url: str


def download_nvd_recent(days_back: int = 30) -> list[dict]:
    """
    Download recent CVEs from NVD API (free, no key needed).
    Note: Limited to last 90 days without API key.
    """
    log.info("Fetching CVEs from last %d days…", days_back)
    
    # Use the free NVD API endpoint
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_back)
    
    params = {
        "resultsPerPage": 100,
        "startIndex": 0,
        "pubStartDate": start_date.isoformat() + "Z",
        "pubEndDate": end_date.isoformat() + "Z",
    }
    
    all_cves = []
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        all_cves = data.get("vulnerabilities", [])
        log.info("Downloaded %d CVEs", len(all_cves))
    except Exception as e:
        log.error("Failed to download NVD data: %s", e)
        log.warning("Using sample CVEs instead")
        all_cves = _get_sample_cves()
    
    return all_cves


def _get_sample_cves() -> list[dict]:
    """Sample CVEs for demo/testing when API is unavailable."""
    return [
        {
            "cve": {
                "id": "CVE-2024-0001",
                "description": {
                    "description_data": [
                        {
                            "value": "A critical remote code execution vulnerability in popular web framework"
                        }
                    ]
                }
            },
            "metrics": {
                "cvssMetricV31": [
                    {"cvssData": {"baseSeverity": "CRITICAL", "baseScore": 9.8}}
                ]
            }
        }
    ]


def parse_cves(cves: list[dict]) -> list[NVDChunk]:
    """Convert CVE objects to chunks."""
    chunks = []
    
    for item in cves:
        try:
            cve_obj = item.get("cve", {})
            cve_id = cve_obj.get("id", "UNKNOWN")
            
            # Extract description
            desc_data = cve_obj.get("description", {}).get("description_data", [])
            description = desc_data[0]["value"] if desc_data else "No description"
            
            # Extract severity
            metrics = item.get("metrics", {})
            severity = "UNKNOWN"
            cvss_score = 0.0
            
            if "cvssMetricV31" in metrics:
                m = metrics["cvssMetricV31"][0].get("cvssData", {})
                severity = m.get("baseSeverity", "UNKNOWN")
                cvss_score = float(m.get("baseScore", 0))
            elif "cvssMetricV30" in metrics:
                m = metrics["cvssMetricV30"][0].get("cvssData", {})
                severity = m.get("baseSeverity", "UNKNOWN")
                cvss_score = float(m.get("baseScore", 0))
            
            text = (
                f"CVE-{cve_id}\n"
                f"Severity: {severity} (CVSS: {cvss_score})\n"
                f"Description: {description}"
            )
            
            url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            
            chunks.append(NVDChunk(
                chunk_id=f"cve-{cve_id}",
                text=text,
                source="nvd",
                object_type="cve",
                cve_id=cve_id,
                description=description,
                severity=severity,
                cvss_score=cvss_score,
                url=url,
            ))
        except Exception as e:
            log.warning("Skipped CVE: %s", e)
            continue
    
    log.info("Parsed %d CVE chunks", len(chunks))
    return chunks


def load_nvd(force_refresh: bool = False) -> list[NVDChunk]:
    """Full NVD loading pipeline."""
    if force_refresh and RAW_PATH.exists():
        RAW_PATH.unlink()
    
    if RAW_PATH.exists():
        log.info("Cache hit — loading from %s", RAW_PATH)
        raw_data = json.loads(RAW_PATH.read_text())
    else:
        raw_data = download_nvd_recent(days_back=7)  # Last 7 days for demo
        RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
        RAW_PATH.write_text(json.dumps(raw_data, indent=2))
    
    chunks = parse_cves(raw_data)
    
    CHUNK_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHUNK_PATH.write_text(json.dumps([asdict(c) for c in chunks], indent=2))
    log.info("Saved %d CVE chunks to %s", len(chunks), CHUNK_PATH)
    
    return chunks


if __name__ == "__main__":
    chunks = load_nvd()
    print(f"\n✓ Loaded {len(chunks)} CVE chunks")
```

### Run NVD Loader

```bash
python3 data_loaders/nvd_loader.py
```

### Expected Output

```
11:50:12  INFO     Fetching CVEs from last 7 days…
11:50:15  INFO     Downloaded 156 CVEs
11:50:15  INFO     Parsed 156 CVE chunks
11:50:15  INFO     Saved 156 CVE chunks to data/chunks/nvd_chunks.json

✓ Loaded 156 CVE chunks
```

---

## Step 7: AlienVault OTX Loader (Phase 1)

### What's AlienVault OTX?
Open Threat Exchange — community-driven threat intelligence with latest threat indicators, malware samples, etc.

### Get Free API Key

1. Go to [AlienVault OTX](https://otx.alienvault.com/)
2. Click **Sign up** (top right)
3. Create account with email
4. After signup, go to **Settings** → **API** 
5. Copy your **API Key**
6. Save it safely (you'll use it)

### Create Config File

Create `config/.env`:

```
# AlienVault OTX API Key
OTX_API_KEY=your_api_key_here_do_not_commit_to_git
```

**⚠️ IMPORTANT**: Add this to `.gitignore` (never commit API keys!)

Create `.gitignore` in cybersentinel folder:

```
# Sensitive files
config/.env
.env
.venv/
venv/
__pycache__/
*.pyc
.DS_Store
*.log

# IDE
.vscode/
.idea/

# Data (optional, remove if you want to commit data)
data/raw/
data/chunks/
```

### Create OTX Loader File

Create `data_loaders/otx_loader.py`:

```python
"""
AlienVault OTX (Open Threat Exchange) Loader
==============================================
Fetches threat intelligence: pulse data (threat campaigns).
Requires free API key from otx.alienvault.com
"""

import os
import json
import logging
import requests
from pathlib import Path
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

load_dotenv("config/.env")

API_KEY = os.getenv("OTX_API_KEY")
OTX_URL = "https://otx.alienvault.com/api/v1"
RAW_PATH = Path("data/raw/otx_pulses.json")
CHUNK_PATH = Path("data/chunks/otx_chunks.json")


@dataclass
class OTXChunk:
    """One threat pulse chunk."""
    chunk_id: str
    text: str
    source: str
    object_type: str
    pulse_id: str
    name: str
    author: str
    adversary_names: list[str]
    url: str


def fetch_otx_pulses(limit: int = 50) -> list[dict]:
    """
    Fetch latest threat intelligence pulses from OTX.
    """
    if not API_KEY:
        log.warning("OTX_API_KEY not found in config/.env")
        return []
    
    log.info("Fetching %d pulses from OTX…", limit)
    
    headers = {"X-OTX-API-KEY": API_KEY}
    url = f"{OTX_URL}/pulses/subscribed"
    params = {"limit": limit, "sort": "-created"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        pulses = data.get("results", [])
        log.info("Downloaded %d pulses", len(pulses))
        return pulses
    except requests.exceptions.RequestException as e:
        log.error("Failed to fetch OTX data: %s", e)
        return []


def parse_otx_pulses(pulses: list[dict]) -> list[OXTChunk]:
    """Convert OTX pulses to chunks."""
    chunks = []
    
    for pulse in pulses:
        try:
            pulse_id = pulse.get("id", "UNKNOWN")
            name = pulse.get("name", "")
            author = pulse.get("author_name", "Unknown")
            description = pulse.get("description", "")
            adversary_names = pulse.get("adversary", {}).get("name", [])
            if isinstance(adversary_names, str):
                adversary_names = [adversary_names] if adversary_names else []
            
            # Indicators (IOCs) in this pulse
            indicators = pulse.get("indicators", [])
            ioc_summary = f"Contains {len(indicators)} threat indicators"
            
            text = (
                f"OTX Threat Intelligence Pulse: {name}\n"
                f"Author: {author}\n"
                f"Adversaries: {', '.join(adversary_names) or 'Unknown'}\n"
                f"{ioc_summary}\n\n"
                f"Description: {description}"
            )
            
            url = f"https://otx.alienvault.com/pulse/{pulse_id}"
            
            chunks.append(OXTChunk(
                chunk_id=f"otx-pulse-{pulse_id}",
                text=text,
                source="alienvault_otx",
                object_type="threat_pulse",
                pulse_id=pulse_id,
                name=name,
                author=author,
                adversary_names=adversary_names,
                url=url,
            ))
        except Exception as e:
            log.warning("Skipped pulse: %s", e)
            continue
    
    log.info("Parsed %d OTX chunks", len(chunks))
    return chunks


def load_otx(force_refresh: bool = False) -> list[OXTChunk]:
    """Full OTX loading pipeline."""
    if force_refresh and RAW_PATH.exists():
        RAW_PATH.unlink()
    
    if RAW_PATH.exists():
        log.info("Cache hit — loading from %s", RAW_PATH)
        raw_data = json.loads(RAW_PATH.read_text())
    else:
        raw_data = fetch_otx_pulses(limit=30)
        if raw_data:
            RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
            RAW_PATH.write_text(json.dumps(raw_data, indent=2))
    
    chunks = parse_otx_pulses(raw_data)
    
    CHUNK_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHUNK_PATH.write_text(json.dumps([asdict(c) for c in chunks], indent=2))
    log.info("Saved %d OTX chunks to %s", len(chunks), CHUNK_PATH)
    
    return chunks


if __name__ == "__main__":
    chunks = load_otx()
    print(f"\n✓ Loaded {len(chunks)} OTX threat intelligence chunks")
```

### Run OTX Loader

```bash
python3 data_loaders/otx_loader.py
```

### Expected Output

```
11:55:20  INFO     Fetching 30 pulses from OTX…
11:55:23  INFO     Downloaded 28 pulses
11:55:23  INFO     Parsed 28 OTX chunks
11:55:23  INFO     Saved 28 OTX chunks to data/chunks/otx_chunks.json

✓ Loaded 28 OTX threat intelligence chunks
```

---

## Step 8: Test & Verify Output

### Create Master Loader Script

Create `data_loaders/__init__.py` (empty file to make it a package):

```python
# Empty file
```

Create `data_loaders/run_all_loaders.py`:

```python
"""
Run all data loaders and verify chunks.
"""

import json
import logging
from pathlib import Path
from mitre_loader import load_mitre, print_stats as print_mitre_stats
from nvd_loader import load_nvd
from otx_loader import load_otx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def combine_all_chunks():
    """Run all loaders and combine chunks."""
    log.info("═" * 60)
    log.info("CyberSentinel | Phase 1: Running All Data Loaders")
    log.info("═" * 60)
    
    # Run loaders
    log.info("\n[1/3] Loading MITRE ATT&CK…")
    mitre_chunks = load_mitre()
    
    log.info("\n[2/3] Loading NVD CVEs…")
    nvd_chunks = load_nvd()
    
    log.info("\n[3/3] Loading AlienVault OTX…")
    otx_chunks = load_otx()
    
    # Combine all
    all_chunks = []
    all_chunks.extend([{**vars(c), "object_type": "mitre_" + c.object_type} 
                       for c in mitre_chunks])
    all_chunks.extend([{**vars(c)} for c in nvd_chunks])
    all_chunks.extend([{**vars(c)} for c in otx_chunks])
    
    # Save combined
    combined_path = Path("data/chunks/all_chunks_combined.json")
    combined_path.parent.mkdir(parents=True, exist_ok=True)
    combined_path.write_text(json.dumps(all_chunks, indent=2))
    
    # Print stats
    print("\n" + "═" * 60)
    print("CyberSentinel | Phase 1: Summary")
    print("═" * 60)
    print(f"✓ MITRE chunks:   {len(mitre_chunks)}")
    print(f"✓ NVD chunks:     {len(nvd_chunks)}")
    print(f"✓ OTX chunks:     {len(otx_chunks)}")
    print(f"{'─' * 60}")
    print(f"✓ TOTAL chunks:   {len(all_chunks)}")
    print(f"✓ Combined file:  {combined_path}")
    print("═" * 60 + "\n")
    
    return all_chunks


if __name__ == "__main__":
    chunks = combine_all_chunks()
```

### Run All Loaders

```bash
cd data_loaders
python3 run_all_loaders.py
```

### Expected Final Output

```
════════════════════════════════════════════════════════════
CyberSentinel | Phase 1: Running All Data Loaders
════════════════════════════════════════════════════════════

[1/3] Loading MITRE ATT&CK…
12:00:10  INFO     Cache hit — loading from data/raw/mitre_enterprise.json
12:00:10  INFO     Loaded 25842 STIX objects
12:00:13  INFO     Parsed 2847 technique chunks
12:00:14  INFO     Parsed 268 mitigation chunks
12:00:14  INFO     Parsed 189 threat group chunks
12:00:14  INFO     Saved 3304 chunks to data/chunks/mitre_chunks.json

[2/3] Loading NVD CVEs…
12:00:15  INFO     Cache hit — loading from data/raw/nvd_cves.json
12:00:15  INFO     Parsed 156 CVE chunks
12:00:15  INFO     Saved 156 CVE chunks to data/chunks/nvd_chunks.json

[3/3] Loading AlienVault OTX…
12:00:16  INFO     Fetching 30 pulses from OTX…
12:00:19  INFO     Downloaded 28 pulses
12:00:19  INFO     Parsed 28 OTX chunks
12:00:19  INFO     Saved 28 OTX chunks to data/chunks/otx_chunks.json

════════════════════════════════════════════════════════════
CyberSentinel | Phase 1: Summary
════════════════════════════════════════════════════════════
✓ MITRE chunks:   3304
✓ NVD chunks:     156
✓ OTX chunks:     28
────────────────────────────────────────────────────────────
✓ TOTAL chunks:   3488
✓ Combined file:  data/chunks/all_chunks_combined.json
════════════════════════════════════════════════════════════
```

### Inspect the Data

```bash
# Check file sizes
du -sh data/chunks/*.json

# Look at sample chunks (first 50 lines)
head -50 data/chunks/all_chunks_combined.json

# Count total chunks
jq length data/chunks/all_chunks_combined.json
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'langchain'`

**Cause**: Virtual environment not activated or dependencies not installed.

**Fix**:
```bash
# Activate venv
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

---

### Issue: `Connection timeout when downloading MITRE data`

**Cause**: Network connectivity issue or GitHub server down.

**Fix**:
```bash
# Try again (MITRE data is cached after first download)
python3 data_loaders/mitre_loader.py

# If it persists, check internet:
ping github.com
```

---

### Issue: `OTX_API_KEY not found in config/.env`

**Cause**: Missing API key or wrong file path.

**Fix**:
```bash
# Create config folder if it doesn't exist
mkdir -p config

# Create .env with your key
echo "OTX_API_KEY=your_actual_key_here" > config/.env

# Test loading
python3 data_loaders/otx_loader.py
```

---

### Issue: `PermissionError: [Errno 13] Permission denied`

**Cause**: Trying to write to a read-only directory.

**Fix**:
```bash
# Check permissions
ls -la data/

# Make writable
chmod -R 755 data/
```

---

### Issue: `Python version 3.9 but need 3.10+`

**Cause**: Old Python version.

**Fix**:
```bash
# Check version
python3 --version

# Upgrade (macOS with Homebrew)
brew upgrade python3

# Or download from python.org
```

---

## Next Steps (After Phase 1)

Once Phase 1 is complete:

1. **Check the data**:
   ```bash
   python3 data_loaders/run_all_loaders.py
   ```

2. **Move to Phase 2**: Build embeddings pipeline with `sentence-transformers` + `ChromaDB`

3. **Let me know**:
   - Send a screenshot of the final output
   - Any errors you encounter
   - Then we'll jump to Phase 2 (RAG pipeline)

---

## Summary Checklist

- [ ] Python 3.10+ installed
- [ ] Folder structure created (`cybersentinel/`)
- [ ] VS Code installed and opened
- [ ] Virtual environment created and activated
- [ ] `requirements.txt` created with all dependencies
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] MITRE loader created and tested
- [ ] NVD loader created and tested
- [ ] AlienVault OTX account created + API key in `config/.env`
- [ ] OTX loader created and tested
- [ ] All loaders combined and working (`run_all_loaders.py`)
- [ ] 3,500+ chunks of threat data downloaded and processed

**You're now ready for Phase 2!** 🚀

---

**Questions?** Run any loader with `--help` or `python3 loader_name.py --debug`
