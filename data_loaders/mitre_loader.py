"""
MITRE ATT&CK STIX JSON Data Loader
=====================================
Downloads the MITRE ATT&CK Enterprise matrix and extracts:
  - Techniques (attack-pattern)
  - Mitigations (course-of-action)
  - Threat Groups (intrusion-set)

Each record is converted into a clean text chunk with metadata,
ready to be embedded into ChromaDB in Phase 2.
"""

import json
import re
import time
import logging
import urllib.request
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
MITRE_URL = (
    "https://raw.githubusercontent.com/mitre/cti/master/"
    "enterprise-attack/enterprise-attack.json"
)
RAW_PATH   = Path("data/raw/mitre_enterprise.json")
CHUNK_PATH = Path("data/chunks/mitre_chunks.json")


# ── Data model ────────────────────────────────────────────────────────────────
@dataclass
class MitreChunk:
    """One text chunk ready for embedding."""
    chunk_id:    str            # e.g. "technique-T1055.011-chunk-0"
    text:        str            # the passage that gets embedded
    source:      str            # "mitre_attack"
    object_type: str            # "technique" | "mitigation" | "group"
    mitre_id:    str            # T1055.011 / M1050 / G0119
    name:        str
    tactics:     list[str]      # only set for techniques
    platforms:   list[str]      # only set for techniques
    is_subtechnique: bool       # only set for techniques
    url:         str            # ATT&CK permalink


# ── Helpers ───────────────────────────────────────────────────────────────────
def _clean(text: str) -> str:
    """Strip markdown links, citations, and extra whitespace."""
    # Remove [text](url) → text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove bare URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove citation markers like (Citation: ...)
    text = re.sub(r'\(Citation:[^)]+\)', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _get_external_id(obj: dict, source: str = "mitre-attack") -> str:
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == source:
            return ref.get("external_id", "")
    return ""


def _get_url(obj: dict, source: str = "mitre-attack") -> str:
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == source:
            return ref.get("url", "")
    return ""


def _chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """
    Split a long description into overlapping word-level chunks.
    overlap = number of words shared between consecutive chunks.
    """
    words = text.split()
    if len(words) <= chunk_size:
        return [text]

    chunks, start = [], 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks


# ── Downloader ────────────────────────────────────────────────────────────────
def download_stix(url: str = MITRE_URL, dest: Path = RAW_PATH) -> dict:
    """
    Download the MITRE ATT&CK STIX bundle.
    Returns the parsed JSON dict and caches it to disk.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        log.info("Cache hit — loading from %s", dest)
        return json.loads(dest.read_text())

    log.info("Downloading MITRE ATT&CK STIX bundle from GitHub …")
    start = time.time()
    with urllib.request.urlopen(url, timeout=60) as resp:
        raw = resp.read()
    elapsed = time.time() - start
    log.info("Downloaded %.1f MB in %.1fs", len(raw) / 1e6, elapsed)

    dest.write_bytes(raw)
    log.info("Saved raw STIX to %s", dest)
    return json.loads(raw)


# ── Parsers ───────────────────────────────────────────────────────────────────
def parse_techniques(objects: list[dict]) -> list[MitreChunk]:
    """Extract and chunk all non-deprecated ATT&CK techniques."""
    chunks = []

    for obj in objects:
        if obj.get("type") != "attack-pattern":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue

        mitre_id = _get_external_id(obj)
        if not mitre_id:
            continue

        name        = obj.get("name", "")
        description = _clean(obj.get("description", ""))
        tactics     = [p["phase_name"] for p in obj.get("kill_chain_phases", [])]
        platforms   = obj.get("x_mitre_platforms", [])
        is_sub      = obj.get("x_mitre_is_subtechnique", False)
        url         = _get_url(obj)

        # Build a rich passage so the embedding captures all key fields
        header = (
            f"MITRE ATT&CK Technique {mitre_id}: {name}\n"
            f"Tactics: {', '.join(tactics) or 'N/A'}\n"
            f"Platforms: {', '.join(platforms) or 'N/A'}\n"
        )
        full_text  = header + description
        text_parts = _chunk_text(full_text)

        for i, part in enumerate(text_parts):
            chunks.append(MitreChunk(
                chunk_id        = f"technique-{mitre_id}-chunk-{i}",
                text            = part,
                source          = "mitre_attack",
                object_type     = "technique",
                mitre_id        = mitre_id,
                name            = name,
                tactics         = tactics,
                platforms       = platforms,
                is_subtechnique = is_sub,
                url             = url,
            ))

    log.info("Parsed %d technique chunks", len(chunks))
    return chunks


def parse_mitigations(objects: list[dict]) -> list[MitreChunk]:
    """Extract and chunk all non-deprecated mitigations."""
    chunks = []

    for obj in objects:
        if obj.get("type") != "course-of-action":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue

        mitre_id    = _get_external_id(obj)
        name        = obj.get("name", "")
        description = _clean(obj.get("description", ""))
        url         = _get_url(obj)

        header    = f"MITRE ATT&CK Mitigation {mitre_id}: {name}\n"
        full_text = header + description
        text_parts = _chunk_text(full_text)

        for i, part in enumerate(text_parts):
            chunks.append(MitreChunk(
                chunk_id        = f"mitigation-{mitre_id}-chunk-{i}",
                text            = part,
                source          = "mitre_attack",
                object_type     = "mitigation",
                mitre_id        = mitre_id,
                name            = name,
                tactics         = [],
                platforms       = [],
                is_subtechnique = False,
                url             = url,
            ))

    log.info("Parsed %d mitigation chunks", len(chunks))
    return chunks


def parse_groups(objects: list[dict]) -> list[MitreChunk]:
    """Extract and chunk all non-deprecated threat actor groups."""
    chunks = []

    for obj in objects:
        if obj.get("type") != "intrusion-set":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue

        mitre_id    = _get_external_id(obj)
        name        = obj.get("name", "")
        aliases     = obj.get("aliases", [])
        description = _clean(obj.get("description", ""))
        url         = _get_url(obj)

        alias_str = ", ".join(a for a in aliases if a != name)
        header    = (
            f"MITRE ATT&CK Threat Group {mitre_id}: {name}\n"
            + (f"Also known as: {alias_str}\n" if alias_str else "")
        )
        full_text  = header + description
        text_parts = _chunk_text(full_text)

        for i, part in enumerate(text_parts):
            chunks.append(MitreChunk(
                chunk_id        = f"group-{mitre_id}-chunk-{i}",
                text            = part,
                source          = "mitre_attack",
                object_type     = "group",
                mitre_id        = mitre_id,
                name            = name,
                tactics         = [],
                platforms       = [],
                is_subtechnique = False,
                url             = url,
            ))

    log.info("Parsed %d threat group chunks", len(chunks))
    return chunks


# ── Main loader ───────────────────────────────────────────────────────────────
def load_mitre(
    url: str   = MITRE_URL,
    dest: Path = RAW_PATH,
    out: Path  = CHUNK_PATH,
    force_refresh: bool = False,
) -> list[MitreChunk]:
    """
    Full pipeline:
      1. Download (or load from cache) the STIX bundle
      2. Parse techniques, mitigations, and groups
      3. Save chunks to JSON for use in Phase 2 (embedding)
      4. Return the list of MitreChunk objects

    Args:
        url:           STIX bundle URL
        dest:          Where to cache the raw JSON
        out:           Where to write the processed chunks
        force_refresh: Re-download even if cache exists
    """
    if force_refresh and dest.exists():
        log.info("Force refresh — deleting cached STIX file")
        dest.unlink()

    bundle  = download_stix(url, dest)
    objects = bundle.get("objects", [])
    log.info("Loaded %d STIX objects", len(objects))

    techniques  = parse_techniques(objects)
    mitigations = parse_mitigations(objects)
    groups      = parse_groups(objects)

    all_chunks = techniques + mitigations + groups
    log.info("Total chunks: %d", len(all_chunks))

    # Save to disk for Phase 2
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([asdict(c) for c in all_chunks], indent=2))
    log.info("Saved %d chunks to %s", len(all_chunks), out)

    return all_chunks


# ── Quick stats ───────────────────────────────────────────────────────────────
def print_stats(chunks: list[MitreChunk]) -> None:
    by_type: dict[str, int] = {}
    for c in chunks:
        by_type[c.object_type] = by_type.get(c.object_type, 0) + 1

    print("\n── CyberSentinel | MITRE Loader Stats ──────────────────")
    for obj_type, count in sorted(by_type.items()):
        print(f"  {obj_type:<16} {count:>5} chunks")
    print(f"  {'TOTAL':<16} {len(chunks):>5} chunks")

    # Sample output
    sample = next((c for c in chunks if c.object_type == "technique"), None)
    if sample:
        print("\n── Sample technique chunk ───────────────────────────────")
        print(f"  chunk_id : {sample.chunk_id}")
        print(f"  mitre_id : {sample.mitre_id}")
        print(f"  name     : {sample.name}")
        print(f"  tactics  : {sample.tactics}")
        print(f"  platforms: {sample.platforms}")
        print(f"  text[:200]: {sample.text[:200]} …")
    print("─────────────────────────────────────────────────────────\n")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    chunks = load_mitre()
    print_stats(chunks)
