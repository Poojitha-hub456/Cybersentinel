# CyberSentinel — Phase 1: Data Ingestion Pipeline

Build an autonomous SOC analyst using RAG + multi-agent AI.

## 📋 What Is Phase 1?

Phase 1 downloads and processes threat intelligence from three sources:

1. **MITRE ATT&CK** — Techniques, mitigations, threat groups (3,300+ chunks)
2. **NVD CVEs** — Vulnerability database (150+ chunks)
3. **AlienVault OTX** — Threat pulses & campaigns (30+ chunks)

These chunks become the knowledge base for your RAG system in Phase 2.

---

## 🚀 Quick Start (5 minutes)

### Step 1: Clone/Create Project
```bash
# You should already have the project folder
cd cybersentinel
```

### Step 2: Activate Virtual Environment
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Should see `(venv)` in your terminal.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Takes 5-10 minutes on first install.

### Step 4: Create Config File
```bash
# Copy the example
cp config/.env.example config/.env

# Edit it with your OTX API key
nano config/.env
# or
code config/.env
```

### Step 5: Run All Loaders
```bash
cd data_loaders
python3 run_all_loaders.py
```

Watch it download ~100 MB of threat data and process 3,500+ chunks.

---

## 📁 File Structure

```
cybersentinel/
├── data_loaders/
│   ├── mitre_loader.py       # MITRE ATT&CK loader
│   ├── nvd_loader.py         # NVD CVE loader
│   ├── otx_loader.py         # AlienVault OTX loader
│   ├── run_all_loaders.py    # Master loader (run this!)
│   └── __init__.py           # Package marker
├── data/
│   ├── raw/                  # Raw JSON from APIs
│   │   ├── mitre_enterprise.json
│   │   ├── nvd_cves.json
│   │   └── otx_pulses.json
│   └── chunks/               # Processed chunks ready for embedding
│       ├── mitre_chunks.json
│       ├── nvd_chunks.json
│       ├── otx_chunks.json
│       └── all_chunks_combined.json
├── config/
│   ├── .env.example          # Template (copy to .env)
│   └── .env                  # Your actual config (DON'T COMMIT!)
├── requirements.txt          # Python dependencies
├── SETUP_GUIDE.md           # Detailed step-by-step guide
└── README.md                # This file
```

---

## 🔧 What Each Loader Does

### MITRE ATT&CK Loader
Downloads the STIX bundle from GitHub and extracts:
- **Techniques**: T1234, T1055.011 (attack methods)
- **Mitigations**: M1001, M1050 (defensive strategies)
- **Groups**: G0001, G0119 (threat actors like APT28)

```bash
python3 data_loaders/mitre_loader.py
# Output: 3,304 chunks
```

### NVD CVE Loader
Fetches vulnerabilities from National Vulnerability Database:
- CVE-2024-1234 with CVSS scores
- Severity levels (Critical, High, Medium, Low)
- Descriptions and links

```bash
python3 data_loaders/nvd_loader.py
# Output: ~150 chunks (last 7 days)
```

### AlienVault OTX Loader
Grabs threat intelligence from the community:
- Threat campaign pulses
- Adversary mapping (Emotet, APT28, etc.)
- Indicators of compromise (IOCs)

```bash
python3 data_loaders/otx_loader.py
# Output: 28 chunks
```

---

## 🔑 API Keys Required

### ✓ Free (Required for full functionality)
- **AlienVault OTX**: https://otx.alienvault.com
  - Click "Sign up" → Create account → Settings → API
  - Copy key to `config/.env`

### ✗ Not Required (Phase 1 works without these)
- NVD: Uses free API without key
- MITRE: Uses public GitHub (no auth needed)
- OpenAI/Google/Anthropic: Needed for Phase 3+ only

---

## 📊 Expected Output

Running `python3 data_loaders/run_all_loaders.py` should output:

```
╔══════════════════════════════════════════════════════════╗
║   CyberSentinel | Phase 1: Data Loading Pipeline         ║
╚══════════════════════════════════════════════════════════╝

📥 [1/3] Loading MITRE ATT&CK threat framework…
─────────────────────────────────────────────
✓ Loaded 3304 MITRE chunks

📥 [2/3] Loading NVD CVE vulnerabilities…
─────────────────────────────────────────────
✓ Loaded 156 NVD chunks

📥 [3/3] Loading AlienVault OTX threat intelligence…
─────────────────────────────────────────────
✓ Loaded 28 OTX chunks

╔══════════════════════════════════════════════════════════╗
║   Phase 1: Complete! ✓                                   ║
╚══════════════════════════════════════════════════════════╝

📊 SUMMARY:
─────────────────────────────────────────────
  MITRE chunks      :   3304
  NVD chunks        :    156
  OTX chunks        :     28
  ─────────────────────────────────────────
  TOTAL chunks      :   3488

📁 Output Location:
  → /path/to/cybersentinel/data/chunks/all_chunks_combined.json
```

---

## 🔍 Verify Output

After running, check the data:

```bash
# See file sizes
ls -lh data/chunks/

# Count chunks
jq length data/chunks/all_chunks_combined.json

# Look at a sample chunk
jq '.[0]' data/chunks/all_chunks_combined.json | head -30
```

---

## ❌ Troubleshooting

### "ModuleNotFoundError: No module named 'langchain'"
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "OTX_API_KEY not found"
```bash
# Create config/.env
mkdir -p config
cp config/.env.example config/.env

# Edit with your OTX key
nano config/.env
```

### "Connection timeout when downloading MITRE"
```bash
# Just try again (MITRE data is cached after first download)
python3 data_loaders/mitre_loader.py

# It will use the cached version on retry
```

### "PermissionError when writing to data/"
```bash
# Make data folder writable
chmod -R 755 data/
mkdir -p data/raw data/chunks
```

---

## 📚 What's a "Chunk"?

A chunk is one passage of text that will be embedded (converted to a vector) in Phase 2.

Example chunk:

```json
{
  "chunk_id": "technique-T1055.011-chunk-0",
  "text": "MITRE ATT&CK Technique T1055.011: Process Injection...",
  "source": "mitre_attack",
  "object_type": "technique",
  "mitre_id": "T1055.011",
  "tactics": ["defense-evasion", "privilege-escalation"],
  "platforms": ["Windows"],
  "url": "https://attack.mitre.org/techniques/T1055/011/"
}
```

These chunks are your knowledge base. In Phase 2, you'll:
1. Embed each chunk (convert to vector: ~384 dimensions)
2. Store in ChromaDB vector database
3. Build a retriever for semantic search

When an alert comes in later (Phase 3), you'll search these chunks to find relevant threat context.

---

## 🎯 Next Steps (Phase 2)

Once Phase 1 is working:

1. **Run Phase 1 again** to generate all chunks:
   ```bash
   cd data_loaders
   python3 run_all_loaders.py
   ```

2. **Check output file**:
   ```bash
   ls -lh data/chunks/all_chunks_combined.json
   ```

3. **Move to Phase 2**: Build the RAG pipeline
   - Install `sentence-transformers` and `chromadb`
   - Embed all chunks
   - Create a vector database
   - Build retriever with semantic search

---

## 📖 Files Reference

| File | Purpose |
|------|---------|
| `mitre_loader.py` | Download & parse MITRE ATT&CK STIX |
| `nvd_loader.py` | Download & parse NVD CVE data |
| `otx_loader.py` | Fetch & parse AlienVault OTX pulses |
| `run_all_loaders.py` | Master script — run this! |
| `requirements.txt` | All Python dependencies |
| `config/.env.example` | Template for config |
| `SETUP_GUIDE.md` | Detailed step-by-step setup |

---

## 💡 Pro Tips

1. **First run takes time**: MITRE download is ~70 MB. Subsequent runs use cache.

2. **Check caching**: Look in `data/raw/` — if files exist, they won't re-download.

3. **Force refresh** if you want fresh data:
   ```python
   # In your Python script
   from data_loaders import load_mitre
   load_mitre(force_refresh=True)  # Re-download
   ```

4. **Use the right chunks**: `all_chunks_combined.json` has everything ready for Phase 2.

---

## 🎓 Learning Goals (Phase 1)

By the end of Phase 1, you should understand:

- ✓ How to load data from multiple APIs
- ✓ How to parse and normalize threat intelligence
- ✓ What a "chunk" is (passage for embedding)
- ✓ How to combine datasets
- ✓ The structure of MITRE ATT&CK, CVEs, and OTX

You're building the **data foundation** for an intelligent security system. In Phase 2, these chunks become a **searchable knowledge base**. In Phase 3, agents will **use that knowledge** to analyze threats.

---

## 📞 Questions?

- Check `SETUP_GUIDE.md` for detailed setup
- Re-run `python3 data_loaders/run_all_loaders.py` to verify everything works
- Check logs for specific errors
- All loaders have helpful error messages

---

**Ready to move to Phase 2?** 🚀

Next: Build embeddings & RAG retriever
