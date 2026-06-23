"""
NVD (National Vulnerability Database) CVE Loader
================================================
Downloads recent CVE data and chunks it for RAG.

Usage:
    python3 nvd_loader.py
"""

import json
import requests
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Config ───────────────────────────────────────────────────────────────────
RAW_PATH = Path("data/raw/nvd_cves.json")
CHUNK_PATH = Path("data/chunks/nvd_chunks.json")


# ── Data model ────────────────────────────────────────────────────────────────
@dataclass
class NVDChunk:
    """One CVE chunk ready for embedding."""
    chunk_id: str
    text: str
    source: str
    object_type: str
    cve_id: str
    description: str
    severity: str
    cvss_score: float
    url: str


# ── Downloader ────────────────────────────────────────────────────────────────
def download_nvd_recent(days_back: int = 7) -> list[dict]:
    """
    Download recent CVEs from NVD API (free, no key needed).
    
    Note: Without API key, limited to last 90 days.
    
    Args:
        days_back: Number of days to fetch (default: 7)
        
    Returns:
        List of CVE objects from NVD
    """
    log.info("Fetching CVEs from last %d days…", days_back)
    
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
        log.info("Downloaded %d CVEs from %s to %s", 
                 len(all_cves), start_date.date(), end_date.date())
    except requests.exceptions.RequestException as e:
        log.error("Failed to download NVD data: %s", e)
        log.warning("Using sample CVEs instead")
        all_cves = _get_sample_cves()
    
    return all_cves


def _get_sample_cves() -> list[dict]:
    """
    Sample CVEs for demo/testing when API is unavailable.
    These are realistic examples.
    """
    return [
        {
            "cve": {
                "id": "CVE-2024-3156",
                "description": {
                    "description_data": [
                        {
                            "value": "Remote Code Execution in Apache Struts allows unauthenticated attackers "
                                    "to execute arbitrary code via specially crafted HTTP requests."
                        }
                    ]
                }
            },
            "metrics": {
                "cvssMetricV31": [
                    {
                        "cvssData": {
                            "baseSeverity": "CRITICAL",
                            "baseScore": 9.8,
                            "version": "3.1"
                        }
                    }
                ]
            }
        },
        {
            "cve": {
                "id": "CVE-2024-2891",
                "description": {
                    "description_data": [
                        {
                            "value": "SQL Injection in MySQL allows authenticated users to execute "
                                    "arbitrary SQL code through improper input validation."
                        }
                    ]
                }
            },
            "metrics": {
                "cvssMetricV31": [
                    {
                        "cvssData": {
                            "baseSeverity": "HIGH",
                            "baseScore": 8.8,
                            "version": "3.1"
                        }
                    }
                ]
            }
        },
    ]


# ── Parser ────────────────────────────────────────────────────────────────────
def parse_cves(cves: list[dict]) -> list[NVDChunk]:
    """
    Convert CVE objects to NVDChunk objects for RAG.
    
    Handles missing fields gracefully.
    """
    chunks = []
    
    for item in cves:
        try:
            cve_obj = item.get("cve", {})
            cve_id = cve_obj.get("id", "UNKNOWN")
            
            # Extract description
            desc_data = cve_obj.get("description", {}).get("description_data", [])
            description = desc_data[0]["value"] if desc_data else "No description"
            
            # Extract severity and CVSS score
            severity = "UNKNOWN"
            cvss_score = 0.0
            metrics = item.get("metrics", {})
            
            # Try CVSS 3.1 first, then 3.0, then 2.0
            for metric_version in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                if metric_version in metrics:
                    m = metrics[metric_version][0].get("cvssData", {})
                    severity = m.get("baseSeverity", "UNKNOWN")
                    cvss_score = float(m.get("baseScore", 0))
                    break
            
            # Build rich text for embedding
            text = (
                f"NVD CVE: {cve_id}\n"
                f"Severity: {severity} (CVSS Score: {cvss_score})\n"
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


# ── Main loader ───────────────────────────────────────────────────────────────
def load_nvd(force_refresh: bool = False, days: int = 7) -> list[NVDChunk]:
    """
    Full NVD loading pipeline.
    
    Args:
        force_refresh: Force re-download even if cached
        days: Number of days back to fetch
        
    Returns:
        List of NVDChunk objects ready for embedding
    """
    if force_refresh and RAW_PATH.exists():
        log.info("Force refresh — deleting cached NVD file")
        RAW_PATH.unlink()
    
    if RAW_PATH.exists():
        log.info("Cache hit — loading from %s", RAW_PATH)
        raw_data = json.loads(RAW_PATH.read_text())
    else:
        raw_data = download_nvd_recent(days_back=days)
        RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
        RAW_PATH.write_text(json.dumps(raw_data, indent=2))
        log.info("Saved raw CVE data to %s", RAW_PATH)
    
    chunks = parse_cves(raw_data)
    
    CHUNK_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHUNK_PATH.write_text(json.dumps([asdict(c) for c in chunks], indent=2))
    log.info("Saved %d CVE chunks to %s", len(chunks), CHUNK_PATH)
    
    return chunks


# ── Quick stats ───────────────────────────────────────────────────────────────
def print_stats(chunks: list[NVDChunk]) -> None:
    """Print loading statistics."""
    if not chunks:
        print("\nℹ No CVE chunks to display")
        return
    
    # Calculate severity distribution
    severity_counts = {}
    for c in chunks:
        severity_counts[c.severity] = severity_counts.get(c.severity, 0) + 1
    
    # Calculate score ranges
    critical = len([c for c in chunks if 9.0 <= c.cvss_score <= 10.0])
    high = len([c for c in chunks if 7.0 <= c.cvss_score < 9.0])
    medium = len([c for c in chunks if 4.0 <= c.cvss_score < 7.0])
    low = len([c for c in chunks if c.cvss_score < 4.0])
    
    print("\n── CyberSentinel | NVD CVE Loader Stats ──────────────────")
    print(f"  Total CVEs: {len(chunks)}")
    print(f"  By Severity:")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]:
        if sev in severity_counts:
            print(f"    {sev:<10} {severity_counts[sev]:>3}")
    print(f"\n  By CVSS Score Range:")
    print(f"    Critical (9.0-10.0): {critical:>3}")
    print(f"    High     (7.0-8.9):  {high:>3}")
    print(f"    Medium   (4.0-6.9):  {medium:>3}")
    print(f"    Low      (0.0-3.9):  {low:>3}")
    print("──────────────────────────────────────────────────────────\n")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    chunks = load_nvd(days=7)
    print_stats(chunks)
