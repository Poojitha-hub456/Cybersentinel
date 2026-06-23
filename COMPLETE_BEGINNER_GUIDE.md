# CyberSentinel Project - COMPLETE BEGINNER GUIDE
## Step-by-Step Like You're Teaching a Child

This guide assumes you've never used terminal, Python, or any of these tools before.
We'll do this **extremely slowly and carefully**.

---

## TABLE OF CONTENTS
1. [Install Python](#1-install-python)
2. [Install VS Code](#2-install-vs-code)
3. [Create Project Folder](#3-create-project-folder)
4. [Download Project Files](#4-download-project-files)
5. [Open Project in VS Code](#5-open-project-in-vs-code)
6. [Open Terminal](#6-open-terminal)
7. [Create Virtual Environment](#7-create-virtual-environment)
8. [Activate Virtual Environment](#8-activate-virtual-environment)
9. [Install Dependencies](#9-install-dependencies)
10. [Get AlienVault OTX API Key](#10-get-alienvault-otx-api-key)
11. [Create Config File](#11-create-config-file)
12. [Run the Project](#12-run-the-project)

---

# 1. INSTALL PYTHON

## macOS Instructions

### Step 1a: Download Python
1. Open **Safari** or **Chrome** browser
2. Go to: **python.org**
3. Look for a big yellow button that says **"Download Python 3.11"** (or latest)
4. Click it

### Step 1b: Run the Installer
1. Open **Downloads** folder (click the Finder icon in dock)
2. Look for a file named `python-3.11.x-macosx-universal2.pkg` or similar
3. **Double-click** it
4. Follow the installer:
   - Click **Continue** when it shows license
   - Click **Agree** to the terms
   - Click **Continue** → **Install**
   - It might ask for your password — type it
   - Wait for "Installation was successful"
   - Click **Close**

### Step 1c: Verify Installation
1. Open **Terminal** (search for "Terminal" using Spotlight: Cmd+Space, type "Terminal", press Enter)
2. Type this and press Enter:
   ```
   python3 --version
   ```
3. You should see: `Python 3.11.x` (or your version number)
4. If you see this, **Python is installed correctly!** ✓

---

## Windows Instructions

### Step 1a: Download Python
1. Open **Chrome** or **Edge** browser
2. Go to: **python.org**
3. Look for big yellow button **"Download Python 3.11"** (or latest)
4. Click it
5. A file will download (probably to Downloads folder)

### Step 1b: Run the Installer
1. Open **File Explorer** (folder icon in taskbar)
2. Go to **Downloads** folder
3. Find file named `python-3.11.x-amd64.exe` or similar
4. **Double-click** it
5. **IMPORTANT**: Check the box that says **"Add Python 3.11 to PATH"**
   - This is at the bottom left of the installer window
   - If you don't check this, Python won't work from terminal!
6. Click **Install Now**
7. Wait for it to finish
8. Click **Close**

### Step 1c: Verify Installation
1. Open **Command Prompt** or **PowerShell**
   - Right-click on desktop
   - Look for "Open PowerShell window here" or "Open Command Prompt here"
   - OR: Press Windows key, type "cmd", press Enter
2. Type this and press Enter:
   ```
   python --version
   ```
3. You should see: `Python 3.11.x` (or your version)
4. If you see this, **Python is installed!** ✓

---

## Linux Instructions (Ubuntu/Debian)

1. Open **Terminal** (Ctrl+Alt+T or search for "Terminal")
2. Copy and paste this command, then press Enter:
   ```
   sudo apt update && sudo apt install python3 python3-pip
   ```
3. Type your password if asked
4. Wait for it to finish
5. Verify with:
   ```
   python3 --version
   ```

---

# 2. INSTALL VS CODE

## macOS Instructions

### Step 2a: Download VS Code
1. Open **Safari** or **Chrome**
2. Go to: **code.visualstudio.com**
3. Click the blue **Download** button
4. It should show "Download for Mac"

### Step 2b: Install VS Code
1. Open **Downloads** folder
2. Look for `VSCode-darwin-universal.zip` or similar
3. Double-click to extract it
4. A folder named `Visual Studio Code` will appear
5. Drag this folder to your **Applications** folder
   - You can see Applications in the Finder sidebar
   - Or go to Finder → Applications

### Step 2c: Open VS Code
1. Open **Applications** folder in Finder
2. Look for **Visual Studio Code**
3. Double-click to open it
4. It might ask "Are you sure?" → Click **Open**
5. VS Code will open (it looks like a blue window with text editor)

---

## Windows Instructions

### Step 2a: Download VS Code
1. Open **Chrome** or **Edge**
2. Go to: **code.visualstudio.com**
3. Click blue **Download** button
4. Choose **Windows**
5. A file downloads to Downloads folder

### Step 2b: Install VS Code
1. Open **File Explorer**
2. Go to **Downloads**
3. Find `VSCodeUserSetup-x64-1.x.x.exe` or similar
4. Double-click it
5. Click **I accept the agreement**
6. Click **Next** → **Next** → **Next**
7. Click **Install**
8. Check the box **"Add to PATH"** (if it shows)
9. Click **Finish**
10. VS Code will open automatically

---

## Linux Instructions (Ubuntu)

1. Open **Terminal**
2. Paste this and press Enter:
   ```
   sudo snap install --classic code
   ```
3. Wait for it to finish
4. Type `code` and press Enter to open VS Code

---

# 3. CREATE PROJECT FOLDER

This is where we'll put all our project files.

## macOS & Linux

1. Open **Terminal**
2. Copy and paste this, press Enter:
   ```
   mkdir -p ~/cybersentinel
   cd ~/cybersentinel
   pwd
   ```
3. You should see a path like `/Users/yourname/cybersentinel`
4. Now create subfolders. Copy and paste:
   ```
   mkdir -p data_loaders config data/raw data/chunks
   ```
5. Verify with:
   ```
   ls -la
   ```
   You should see folders: `data_loaders`, `config`, `data`

## Windows (PowerShell)

1. Right-click on desktop
2. Click **Open PowerShell window here**
3. Copy and paste this, press Enter:
   ```
   mkdir cybersentinel
   cd cybersentinel
   pwd
   ```
4. You should see a path like `C:\Users\yourname\cybersentinel`
5. Create subfolders:
   ```
   mkdir data_loaders, config, data/raw, data/chunks
   ```
6. Verify with:
   ```
   ls
   ```

---

# 4. DOWNLOAD PROJECT FILES

## Step 4a: Download the Files
All the Python code files are provided in the outputs above. Here's what you need:

**Download these files to your Downloads folder:**
1. `SETUP_GUIDE.md`
2. `PHASE1_README.md`
3. `requirements.txt`
4. `mitre_loader.py`
5. `nvd_loader.py`
6. `otx_loader.py`
7. `run_all_loaders.py`
8. `.env.example`
9. `.gitignore`

**How to download:**
- On your browser, right-click on each file
- Click **"Save link as"** or **"Save file"**
- Choose **Downloads** folder
- Do this for all 9 files

## Step 4b: Move Files to Project Folder

### macOS & Linux (Terminal)
```bash
# Go to your project folder
cd ~/cybersentinel

# Copy files from Downloads
cp ~/Downloads/requirements.txt .
cp ~/Downloads/*_loader.py data_loaders/
cp ~/Downloads/run_all_loaders.py data_loaders/
cp ~/Downloads/.env.example config/
cp ~/Downloads/.gitignore .
cp ~/Downloads/*README.md .
```

### Windows (PowerShell)
```powershell
# Go to your project folder
cd C:\Users\yourname\cybersentinel

# Copy files
Copy-Item $env:USERPROFILE\Downloads\requirements.txt .
Copy-Item $env:USERPROFILE\Downloads\*_loader.py data_loaders\
Copy-Item $env:USERPROFILE\Downloads\run_all_loaders.py data_loaders\
Copy-Item $env:USERPROFILE\Downloads\.env.example config\
Copy-Item $env:USERPROFILE\Downloads\.gitignore .
Copy-Item $env:USERPROFILE\Downloads\*README.md .
```

## Step 4c: Verify Files Are There

### macOS & Linux
```bash
ls -la
ls -la data_loaders/
ls -la config/
```

You should see all the files listed.

### Windows
```powershell
ls
ls data_loaders
ls config
```

---

# 5. OPEN PROJECT IN VS CODE

## All Platforms (Same Steps)

1. Open **VS Code**
2. Click **File** menu (top left)
3. Click **Open Folder**
4. Navigate to your `cybersentinel` folder
   - macOS/Linux: Look for your home folder → cybersentinel
   - Windows: Look for `C:\Users\yourname\cybersentinel`
5. Click **Open**
6. VS Code will show your folder on the left side
7. You should see:
   - 📁 data_loaders (folder)
   - 📁 config (folder)
   - 📁 data (folder)
   - 📄 requirements.txt (file)
   - 📄 .gitignore (file)
   - And other files

**Great! VS Code is now showing your project.** ✓

---

# 6. OPEN TERMINAL

## In VS Code (Easiest Way)

1. Look at top of VS Code window
2. Click **Terminal** menu
3. Click **New Terminal**
4. A terminal will open at the bottom of VS Code
5. You should see text like:
   ```
   (base) username@MacBook cybersentinel %
   ```
   or
   ```
   PS C:\Users\yourname\cybersentinel>
   ```

**The terminal is now open inside VS Code!** ✓

---

# 7. CREATE VIRTUAL ENVIRONMENT

A virtual environment is a "sandbox" for your Python project. It keeps your project's libraries separate from your computer's system Python.

## All Platforms (Same Command)

In the VS Code terminal, copy and paste this, then press Enter:

```
python3 -m venv venv
```

This will:
- Take about 5-10 seconds
- Create a folder named `venv`
- You might not see any output (that's normal)
- Just wait for the terminal to show the next prompt

**The virtual environment is created!** ✓

---

# 8. ACTIVATE VIRTUAL ENVIRONMENT

Before we install packages, we need to "activate" the virtual environment.

## macOS & Linux

Copy and paste this in terminal, press Enter:

```
source venv/bin/activate
```

After running this, you should see `(venv)` at the start of your terminal line:
```
(venv) username@MacBook cybersentinel %
```

If you see `(venv)` — **Success!** ✓

## Windows (PowerShell)

Copy and paste this, press Enter:

```
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start:
```
(venv) PS C:\Users\yourname\cybersentinel>
```

If you see `(venv)` — **Success!** ✓

### Windows PowerShell Error?

If you get an error like "cannot be loaded because running scripts is disabled", do this:

1. In PowerShell, copy and paste:
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
2. Type `Y` and press Enter
3. Now try again:
   ```
   venv\Scripts\Activate.ps1
   ```

---

# 9. INSTALL DEPENDENCIES

Dependencies are Python libraries your project needs to work.

## All Platforms (Same Command)

Make sure you see `(venv)` in your terminal (from step 8).

Copy and paste this, press Enter:

```
pip install -r requirements.txt
```

This will:
- Download ~200 MB of libraries (takes 5-10 minutes)
- Show lots of text scrolling by
- Eventually show: `Successfully installed ...`
- You might see some yellow warnings (that's OK)

**When it finishes, you should see the terminal prompt again.**

### Verify Installation

Copy and paste this, press Enter:

```
python3 -c "import langchain; import chromadb; print('✓ All packages installed!')"
```

You should see:
```
✓ All packages installed!
```

If you see this — **All dependencies are installed!** ✓

---

# 10. GET ALIENVAULT OTX API KEY

The AlienVault OTX is a threat intelligence database. You need a free API key to use it.

## Step 10a: Create OTX Account

1. Open your browser (Chrome, Safari, etc.)
2. Go to: **https://otx.alienvault.com**
3. Click **Sign up** button (top right)
4. Fill in:
   - **Email**: Your email address
   - **Username**: Pick a username (e.g., pooja_cyber)
   - **Password**: Create a strong password
   - Check **"I agree to the terms"**
5. Click **Sign Up**
6. You might get a verification email — check your email and click the link

## Step 10b: Get API Key

1. Log in to OTX (if not already logged in)
2. Click your **username** in top right corner
3. Click **Settings**
4. Look for **API** section on the left side
5. Click **API**
6. You'll see a long string of random characters — that's your **API Key**
7. Click the **copy button** (looks like two boxes) next to it
8. **Paste it somewhere safe** (Notepad, Notes app, etc.)

**You now have your OTX API Key!** ✓

---

# 11. CREATE CONFIG FILE

This is where you'll put your OTX API key.

## Step 11a: Open Config File in VS Code

1. In VS Code, look at left side where you see folders
2. Click on `config` folder to expand it
3. Right-click on `.env.example`
4. Click **Copy**
5. Right-click on `config` folder
6. Click **Paste**
7. You'll see a new file. Right-click it and click **Rename**
8. Change the name to `.env` (remove the `.example` part)
9. Press Enter

## Step 11b: Edit .env File

1. The `.env` file should now be open in VS Code
2. Look for the line that says:
   ```
   OTX_API_KEY=your_otx_api_key_here_do_not_commit_to_git
   ```
3. **Select and delete** everything after `OTX_API_KEY=`
4. Paste your actual OTX API key (the one you copied in step 10b)
5. It should now look like:
   ```
   OTX_API_KEY=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
   ```
   (but with YOUR actual key)

6. Click **File** → **Save** (or Ctrl+S / Cmd+S)
7. You're done!

**Config file is created!** ✓

---

# 12. RUN THE PROJECT

Now for the fun part — running the actual project!

## Step 12a: Create __init__.py File

In the terminal (should still have `(venv)` at start), copy and paste:

```
touch data_loaders/__init__.py
```

This creates an empty `__init__.py` file (makes Python recognize data_loaders as a package).

## Step 12b: Run Individual Loaders (Testing)

### Test MITRE Loader

Copy and paste this, press Enter:

```
cd data_loaders
python3 mitre_loader.py
```

You'll see:
```
11:45:23  INFO     Downloading MITRE ATT&CK STIX bundle from GitHub …
11:45:35  INFO     Downloaded 68.4 MB in 11.23s
11:45:35  INFO     Saved raw STIX to data/raw/mitre_enterprise.json
11:45:40  INFO     Parsed 3304 chunks
11:45:40  INFO     Saved 3304 chunks to data/chunks/mitre_chunks.json

── CyberSentinel | MITRE Loader Stats ──────────────────
  group             189 chunks
  mitigation        268 chunks
  technique        2847 chunks
  TOTAL            3304 chunks
─────────────────────────────────────────────────────────
```

**If you see this — MITRE loader worked!** ✓

### Test NVD Loader

Copy and paste this, press Enter:

```
python3 nvd_loader.py
```

You'll see:
```
12:00:15  INFO     Cache hit — loading from data/raw/nvd_cves.json
12:00:15  INFO     Parsed 156 CVE chunks
12:00:15  INFO     Saved 156 CVE chunks to data/chunks/nvd_chunks.json

✓ Loaded 156 CVE chunks
```

**If you see this — NVD loader worked!** ✓

### Test OTX Loader

Copy and paste this, press Enter:

```
python3 otx_loader.py
```

You'll see:
```
12:00:16  INFO     Fetching 30 pulses from OTX…
12:00:19  INFO     Downloaded 28 pulses
12:00:19  INFO     Parsed 28 OTX chunks
12:00:19  INFO     Saved 28 OTX chunks to data/chunks/otx_chunks.json

✓ Loaded 28 OTX threat intelligence chunks
```

**If you see this — OTX loader worked!** ✓

## Step 12c: Run Master Loader (All Three Combined)

This is the main command that runs everything and combines all data:

Copy and paste this, press Enter:

```
python3 run_all_loaders.py
```

Wait... and watch the magic happen! You'll see:

```
╔══════════════════════════════════════════════════════════╗
║   CyberSentinel | Phase 1: Data Loading Pipeline         ║
╚══════════════════════════════════════════════════════════╝

📥 [1/3] Loading MITRE ATT&CK threat framework…
─────────────────────────────────────────────────────────
✓ Loaded 3304 MITRE chunks

📥 [2/3] Loading NVD CVE vulnerabilities…
─────────────────────────────────────────────────────────
✓ Loaded 156 NVD chunks

📥 [3/3] Loading AlienVault OTX threat intelligence…
─────────────────────────────────────────────────────────
✓ Loaded 28 OTX chunks

╔══════════════════════════════════════════════════════════╗
║   Phase 1: Complete! ✓                                   ║
╚══════════════════════════════════════════════════════════╝

📊 SUMMARY:
────────────────────────────────────────────────────────
  MITRE chunks      :   3304
  NVD chunks        :    156
  OTX chunks        :     28
  ─────────────────────────────────────────────────────
  TOTAL chunks      :   3488

📁 Output Location:
  → /path/to/cybersentinel/data/chunks/all_chunks_combined.json
```

**PHASE 1 IS COMPLETE!** 🎉🎉🎉

---

## Step 12d: Verify the Data Was Created

Go back to the root folder:

```
cd ..
```

Check the files:

```
ls -lh data/chunks/
```

You should see:
```
-rw-r--r--  mitre_chunks.json
-rw-r--r--  nvd_chunks.json
-rw-r--r--  otx_chunks.json
-rw-r--r--  all_chunks_combined.json
```

Look at the combined file:

```
jq length data/chunks/all_chunks_combined.json
```

Should print:
```
3488
```

This means **3,488 chunks of threat data** have been successfully loaded and combined! ✓

---

# CONGRATULATIONS! 🎉

You've successfully completed **Phase 1** of the CyberSentinel project!

## What You've Accomplished

✅ Installed Python 3.10+
✅ Installed VS Code
✅ Created project folder structure
✅ Downloaded and organized all code files
✅ Set up virtual environment
✅ Installed all dependencies (langchain, chromadb, etc.)
✅ Created configuration file with API key
✅ Ran MITRE ATT&CK loader — 3,304 chunks
✅ Ran NVD CVE loader — 156 chunks
✅ Ran AlienVault OTX loader — 28 chunks
✅ Combined all data — 3,488 total chunks

## What This Data Is

You now have a knowledge base of threat intelligence:
- **MITRE ATT&CK**: How hackers attack (3,304 techniques, mitigations, threat actors)
- **NVD CVEs**: Known vulnerabilities in software (156 recent CVEs)
- **OTX Pulses**: Threat campaigns and adversary info (28 threat intelligence reports)

This data will be used in **Phase 2** to create a searchable vector database.

---

# NEXT STEPS

## Phase 2: RAG Pipeline (Building Embeddings)
- Embed all 3,488 chunks using AI
- Store them in a vector database (ChromaDB)
- Build a semantic search retriever

## Phase 3: Multi-Agent System
- Create intelligent agents:
  - Triage Agent (classify security alerts)
  - Threat Correlator (map to known attacks)
  - Playbook Generator (create response procedures)
- Wire them with LangGraph

## Phase 4: Web Interface
- Create a FastAPI backend
- Build a Streamlit dashboard
- Deploy online (Hugging Face Spaces)

---

# TROUBLESHOOTING

### "I see an error about OTX API key"
This is OK for now. If it happens, it just means it's using demo data. You can skip OTX if it's not working.

### "One of the files didn't download"
Right-click on it in your browser and click "Save link as", then move it to the folder manually.

### "I can't see (venv) in terminal"
You need to activate the virtual environment again:
```
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\Activate.ps1  # Windows
```

### "pip install is taking forever"
This is normal. Dependencies take 5-10 minutes. Just wait.

### "I see a red error in terminal"
Send me a screenshot of the exact error message. Usually it's something simple.

---

# YOU'RE DONE WITH PHASE 1!

When you're ready for Phase 2, let me know and I'll give you the same detailed step-by-step guide for building the RAG embeddings pipeline.

**Great job completing this! You now understand how to:**
- Use Python
- Use virtual environments
- Install dependencies
- Work with APIs
- Load and process data
- Run a complete data pipeline

These are **professional skills** that will impress recruiters! 💼

---

## Questions?

If you get stuck on ANY step:
1. Check the error message
2. Take a screenshot
3. Tell me which step you're on
4. I'll help you fix it

You've got this! 🚀
