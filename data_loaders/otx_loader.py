"""
AlienVault OTX (Open Threat Exchange) Loader
==============================================
Fetches threat intelligence: pulse data (threat campaigns).

Requires:
    - Free AlienVault OTX account: https://otx.alienvault.com
    - API key in config/.env: OTX_API_KEY=your_key_here

Usage:
    python3 otx_loader.py
"""

import os
import json
import logging
import requests
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Config ───────────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv("config/.env")
except ImportError:
    log.warning("python-dotenv not found, make sure config/.env exists")

API_KEY = os.getenv("OTX_API_KEY")
OTX_URL = "https://otx.alienvault.com/api/v1"
RAW_PATH = Path("data/raw/otx_pulses.json")
CHUNK_PATH = Path("data/chunks/otx_chunks.json")


# ── Data model ────────────────────────────────────────────────────────────────
@dataclass
class OTXChunk:
    """One OTX threat pulse chunk."""
    chunk_id: str
    text: str
    source: str
    object_type: str
    pulse_id: str
    name: str
    author: str
    adversary_names: list[str]
    ioc_count: int
    url: str


# ── Downloader ────────────────────────────────────────────────────────────────
def fetch_otx_pulses(limit: int = 50) -> list[dict]:
    """
    Fetch latest threat intelligence pulses from OTX API.
    
    Args:
        limit: Number of pulses to fetch (max 50 per request)
        
    Returns:
        List of pulse objects from OTX
        
    Note:
        Requires OTX_API_KEY environment variable.
    """
    if not API_KEY:
        log.warning("OTX_API_KEY not found in config/.env")
        log.warning("To use OTX:")
        log.warning("  1. Go to https://otx.alienvault.com")
        log.warning("  2. Sign up (free)")
        log.warning("  3. Get API key from Settings > API")
        log.warning("  4. Create config/.env with: OTX_API_KEY=your_key")
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
    except requests.exceptions.HTTPError as e:
        if "401" in str(e):
            log.error("Authentication failed — check OTX_API_KEY in config/.env")
        else:
            log.error("HTTP error fetching OTX data: %s", e)
        return []
    except requests.exceptions.RequestException as e:
        log.error("Failed to fetch OTX data: %s", e)
        return []


def _get_sample_otx_pulses() -> list[dict]:
    """
    Sample OTX pulses for demo/testing when API unavailable.
    """
    return [
        {
            "id": "sample-001",
            "name": "Emotet Malware Campaign",
            "author_name": "OTX Community",
            "description": "Emotet is a modular banking trojan that has been active since 2014. "
                          "It can be used as a loader for other malware. Recently observed spreading "
                          "via malicious Office documents.",
            "adversary": {"name": "Emotet Botnet"},
            "indicators": [
                {"indicator": "192.168.1.1", "type": "IPv4"},
                {"indicator": "malware.example.com", "type": "domain"},
            ]
        },
        {
            "id": "sample-002",
            "name": "APT28 Infrastructure",
            "author_name": "OTX Community",
            "description": "This pulse contains indicators of compromise associated with APT28, "
                          "a sophisticated threat actor attributed to Russian military intelligence.",
            "adversary": {"name": "APT28"},
            "indicators": [
                {"indicator": "10.0.0.0/8", "type": "IPv4"},
            ]
        },
    ]


# ── Parser ────────────────────────────────────────────────────────────────────
def parse_otx_pulses(pulses: list[dict]) -> list[OTXChunk]:
    """
    Convert OTX pulses to OTXChunk objects for RAG.
    
    Handles missing fields gracefully.
    """
    chunks = []
    
    for pulse in pulses:
        try:
            pulse_id = pulse.get("id", "UNKNOWN")
            name = pulse.get("name", "Unknown Pulse")
            author = pulse.get("author_name", "Unknown")
            description = pulse.get("description", "No description")
            
            # Extract adversary names (can be dict or list or string)
            adversary_data = pulse.get("adversary", {})
            if isinstance(adversary_data, dict):
                adversary_names = [adversary_data.get("name")] if adversary_data.get("name") else []
            elif isinstance(adversary_data, list):
                adversary_names = [a.get("name") if isinstance(a, dict) else str(a) 
                                  for a in adversary_data]
            else:
                adversary_names = [str(adversary_data)] if adversary_data else []
            
            adversary_names = [a for a in adversary_names if a]  # Remove empty strings
            
            # Count indicators (IOCs)
            indicators = pulse.get("indicators", [])
            ioc_count = len(indicators)
            
            # Build rich text for embedding
            adversary_str = ", ".join(adversary_names) if adversary_names else "Unknown"
            text = (
                f"AlienVault OTX Threat Intelligence Pulse: {name}\n"
                f"Author: {author}\n"
                f"Adversaries: {adversary_str}\n"
                f"Threat Indicators: {ioc_count} IOCs included\n\n"
                f"Description: {description}"
            )
            
            url = f"https://otx.alienvault.com/pulse/{pulse_id}"
            
            chunks.append(OTXChunk(
                chunk_id=f"otx-pulse-{pulse_id}",
                text=text,
                source="alienvault_otx",
                object_type="threat_pulse",
                pulse_id=pulse_id,
                name=name,
                author=author,
                adversary_names=adversary_names,
                ioc_count=ioc_count,
                url=url,
            ))
        except Exception as e:
            log.warning("Skipped pulse: %s", e)
            continue
    
    log.info("Parsed %d OTX chunks", len(chunks))
    return chunks


# ── Main loader ───────────────────────────────────────────────────────────────
def load_otx(force_refresh: bool = False, limit: int = 30) -> list[OTXChunk]:
    """
    Full OTX loading pipeline.
    
    Args:
        force_refresh: Force re-download even if cached
        limit: Number of pulses to fetch
        
    Returns:
        List of OTXChunk objects ready for embedding
    """
    if force_refresh and RAW_PATH.exists():
        log.info("Force refresh — deleting cached OTX file")
        RAW_PATH.unlink()
    
    if RAW_PATH.exists():
        log.info("Cache hit — loading from %s", RAW_PATH)
        raw_data = json.loads(RAW_PATH.read_text())
    else:
        raw_data = fetch_otx_pulses(limit=limit)
        
        # If API fetch failed, use samples for demo
        if not raw_data:
            log.info("No API data available, using sample pulses for demo")
            raw_data = _get_sample_otx_pulses()
        
        RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
        RAW_PATH.write_text(json.dumps(raw_data, indent=2))
        log.info("Saved raw OTX data to %s", RAW_PATH)
    
    chunks = parse_otx_pulses(raw_data)
    
    CHUNK_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHUNK_PATH.write_text(json.dumps([asdict(c) for c in chunks], indent=2))
    log.info("Saved %d OTX chunks to %s", len(chunks), CHUNK_PATH)
    
    return chunks


# ── Quick stats ───────────────────────────────────────────────────────────────
def print_stats(chunks: list[OTXChunk]) -> None:
    """Print loading statistics."""
    if not chunks:
        print("\nℹ No OTX chunks to display")
        return
    
    total_iocs = sum(c.ioc_count for c in chunks)
    
    print("\n── CyberSentinel | OTX Loader Stats ──────────────────────")
    print(f"  Total Pulses:     {len(chunks)}")
    print(f"  Total IOCs:       {total_iocs}")
    
    # Show top authors
    authors = {}
    for c in chunks:
        authors[c.author] = authors.get(c.author, 0) + 1
    
    if authors:
        print(f"  Top Authors:")
        for author, count in sorted(authors.items(), key=lambda x: -x[1])[:5]:
            print(f"    {author:<30} {count:>2} pulses")
    
    # Show detected adversaries
    adversaries = set()
    for c in chunks:
        adversaries.update(c.adversary_names)
    
    if adversaries:
        print(f"  Adversaries tracked: {len(adversaries)}")
        for adv in sorted(list(adversaries))[:5]:
            print(f"    - {adv}")
    
    print("──────────────────────────────────────────────────────────\n")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    chunks = load_otx(limit=30)
    print_stats(chunks)
