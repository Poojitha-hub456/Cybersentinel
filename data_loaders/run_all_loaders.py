"""
CyberSentinel | Phase 1: Master Data Loader
============================================
Runs all data loaders (MITRE, NVD, OTX) and combines chunks.

This is your main entry point for Phase 1.

Usage:
    python3 run_all_loaders.py
"""

import json
import logging
from pathlib import Path
from mitre_loader import load_mitre
from nvd_loader import load_nvd, print_stats as print_nvd_stats
from otx_loader import load_otx, print_stats as print_otx_stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def combine_all_chunks():
    """
    Run all loaders and combine chunks into a single dataset.
    
    Returns:
        List of all chunks combined, ready for embedding in Phase 2
    """
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  CyberSentinel | Phase 1: Data Loading Pipeline  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # ── Run all loaders ──────────────────────────────────────────────────────
    print("📥 [1/3] Loading MITRE ATT&CK threat framework…")
    print("─" * 60)
    mitre_chunks = load_mitre()
    print(f"✓ Loaded {len(mitre_chunks)} MITRE chunks\n")
    
    print("📥 [2/3] Loading NVD CVE vulnerabilities…")
    print("─" * 60)
    nvd_chunks = load_nvd()
    print_nvd_stats(nvd_chunks)
    
    print("📥 [3/3] Loading AlienVault OTX threat intelligence…")
    print("─" * 60)
    otx_chunks = load_otx()
    print_otx_stats(otx_chunks)
    
    # ── Combine all chunks ───────────────────────────────────────────────────
    log.info("Combining all chunks…")
    
    all_chunks = []
    
    # Add MITRE chunks (already as dicts or dataclasses)
    for c in mitre_chunks:
        if hasattr(c, '__dict__'):
            chunk_dict = c.__dict__
        else:
            chunk_dict = dict(c)
        all_chunks.append(chunk_dict)
    
    # Add NVD chunks
    for c in nvd_chunks:
        if hasattr(c, '__dict__'):
            chunk_dict = c.__dict__
        else:
            chunk_dict = dict(c)
        all_chunks.append(chunk_dict)
    
    # Add OTX chunks
    for c in otx_chunks:
        if hasattr(c, '__dict__'):
            chunk_dict = c.__dict__
        else:
            chunk_dict = dict(c)
        all_chunks.append(chunk_dict)
    
    # ── Save combined dataset ────────────────────────────────────────────────
    combined_path = Path("data/chunks/all_chunks_combined.json")
    combined_path.parent.mkdir(parents=True, exist_ok=True)
    combined_path.write_text(json.dumps(all_chunks, indent=2))
    log.info("Saved combined chunks to %s", combined_path)
    
    # ── Print summary ────────────────────────────────────────────────────────
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Phase 1: Complete! ✓  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    print("📊 SUMMARY:")
    print("─" * 60)
    print(f"  MITRE chunks      : {len(mitre_chunks):>6}")
    print(f"  NVD chunks        : {len(nvd_chunks):>6}")
    print(f"  OTX chunks        : {len(otx_chunks):>6}")
    print("  " + "─" * 55)
    print(f"  TOTAL chunks      : {len(all_chunks):>6}")
    print("─" * 60)
    
    print(f"\n📁 Output Location:")
    print(f"  → {combined_path.resolve()}\n")
    
    print("✨ What's Next?")
    print("─" * 60)
    print("  Phase 2: Build the RAG pipeline")
    print("    - Embed chunks with sentence-transformers")
    print("    - Store in ChromaDB vector database")
    print("    - Build a retriever for semantic search\n")
    
    print("  Next command: Check out Phase 2 notebook")
    print("  cd .. && jupyter notebook phase2_rag_pipeline.ipynb\n")
    
    return all_chunks


def verify_output():
    """Verify that all output files were created correctly."""
    print("\n🔍 Verifying output files…\n")
    
    files_to_check = [
        "data/chunks/mitre_chunks.json",
        "data/chunks/nvd_chunks.json",
        "data/chunks/otx_chunks.json",
        "data/chunks/all_chunks_combined.json",
    ]
    
    all_exist = True
    for file_path in files_to_check:
        p = Path(file_path)
        if p.exists():
            size = p.stat().st_size / 1024  # KB
            lines = len(p.read_text().split('\n'))
            print(f"  ✓ {file_path:<40} ({size:.1f} KB)")
        else:
            print(f"  ✗ {file_path:<40} (MISSING)")
            all_exist = False
    
    if all_exist:
        print("\n✓ All files created successfully!")
    else:
        print("\n⚠ Some files are missing. Check logs above.")
    
    return all_exist


if __name__ == "__main__":
    try:
        chunks = combine_all_chunks()
        verify_output()
    except Exception as e:
        log.error("Pipeline failed: %s", e, exc_info=True)
        print("\n❌ Error running pipeline. Check logs above.")
        exit(1)
