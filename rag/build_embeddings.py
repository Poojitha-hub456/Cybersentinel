"""
Phase 2: Build Embeddings and ChromaDB Vector Store
"""

import json
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Paths
CHUNKS_PATH = Path("../data_loaders/data/chunks/all_chunks_combined.json")
CHROMA_PATH = Path("./chroma_db")
MODEL_NAME = "all-MiniLM-L6-v2"  # Fast, free, good quality

def load_chunks():
    """Load the chunks from Phase 1"""
    log.info("Loading chunks from Phase 1…")
    
    if not CHUNKS_PATH.exists():
        log.error("File not found: %s", CHUNKS_PATH)
        log.error("Did you run Phase 1? Check data/chunks/all_chunks_combined.json")
        return []
    
    with open(CHUNKS_PATH, 'r') as f:
        chunks = json.load(f)
    
    log.info("Loaded %d chunks", len(chunks))
    return chunks

def build_embeddings(chunks):
    """
    Convert text chunks to embeddings using sentence-transformers
    This creates vector representations of the threat data
    """
    log.info("Loading embedding model: %s…", MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME)
    log.info("Model loaded! Encoding %d chunks…", len(chunks))
    
    # Extract just the text from each chunk
    texts = [chunk.get('text', '') for chunk in chunks]
    
    # Convert text to embeddings (vectors)
    embeddings = model.encode(texts, show_progress_bar=True)
    
    log.info("✓ Created %d embeddings", len(embeddings))
    return embeddings, texts

def create_chromadb(chunks, texts, embeddings):
    """
    Store embeddings in ChromaDB vector database
    """
    log.info("Setting up ChromaDB at %s…", CHROMA_PATH)
    
    # Create ChromaDB client (new API - persistent)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    
    # Delete old collection if exists
    try:
        client.delete_collection(name="threat_intelligence")
        log.info("Deleted old collection")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection(
        name="threat_intelligence",
        metadata={"hnsw:space": "cosine"}
    )
    
    log.info("Created collection. Adding %d documents…", len(chunks))
    
    # Add chunks to collection
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        if i % 100 == 0 and i > 0:
            log.info("  Added %d documents…", i)
        
        try:
            collection.add(
                ids=[chunk.get('chunk_id', f'chunk-{i}')],
                embeddings=[embedding.tolist()],
                documents=[chunk.get('text', '')],
                metadatas=[{
                    'source': chunk.get('source', 'unknown'),
                    'object_type': chunk.get('object_type', 'unknown'),
                    'name': chunk.get('name', 'unknown'),
                }]
            )
        except Exception as e:
            log.warning("Failed to add chunk %d: %s", i, e)
            continue
    
    log.info("✓ Saved all embeddings to ChromaDB")
    return client, collection

def test_retrieval(collection):
    """
    Test the retriever with example queries
    """
    log.info("\n" + "="*60)
    log.info("Testing Semantic Search…")
    log.info("="*60)
    
    test_queries = [
        "SQL injection attack",
        "ransomware threat",
        "credential stealing",
        "phishing campaigns",
        "privilege escalation",
    ]
    
    for query in test_queries:
        log.info(f"\nQuery: '{query}'")
        try:
            results = collection.query(
                query_texts=[query],
                n_results=3
            )
            
            if results and results['documents'] and results['documents'][0]:
                log.info(f"  Top 3 results:")
                for j, (doc, dist) in enumerate(zip(results['documents'][0], results['distances'][0]), 1):
                    relevance = 100 * (1 - dist)  # Convert distance to relevance %
                    log.info(f"    {j}. Relevance: {relevance:.1f}%")
                    log.info(f"       {doc[:100]}…")
            else:
                log.info("  No results found")
        except Exception as e:
            log.error(f"  Error querying: {e}")

def main():
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  CyberSentinel | Phase 2: RAG Pipeline  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Step 1: Load chunks
    chunks = load_chunks()
    if not chunks:
        log.error("No chunks loaded. Exiting.")
        return
    
    # Step 2: Create embeddings
    embeddings, texts = build_embeddings(chunks)
    
    # Step 3: Store in ChromaDB
    client, collection = create_chromadb(chunks, texts, embeddings)
    
    # Step 4: Test retrieval
    test_retrieval(collection)
    
    # Done
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Phase 2: Complete! ✓  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    log.info("ChromaDB is ready at: %s", CHROMA_PATH.resolve())
    log.info("Next: Run 'python retriever.py' to test semantic search")
    print("\n")

if __name__ == "__main__":
    main()