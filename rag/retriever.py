"""
Phase 2: Semantic Search Retriever
Query the threat intelligence database
"""

import logging
from pathlib import Path
import chromadb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

CHROMA_PATH = Path("./chroma_db")

class ThreatIntelRetriever:
    """
    Semantic search engine for threat intelligence
    """
    
    def __init__(self):
        """Initialize connection to ChromaDB"""
        log.info("Loading ChromaDB from %s…", CHROMA_PATH)
        
        try:
            self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
            self.collection = self.client.get_collection(
                name="threat_intelligence"
            )
            log.info("✓ Retriever ready! Collection has %d documents", 
                     self.collection.count())
        except Exception as e:
            log.error("Failed to load ChromaDB: %s", e)
            log.error("Did you run 'python build_embeddings.py' first?")
            raise
    
    def search(self, query: str, top_k: int = 5):
        """
        Search for threat intelligence related to a query
        
        Args:
            query: Natural language query (e.g., "SQL injection attack")
            top_k: Number of results to return
            
        Returns:
            List of relevant threat chunks
        """
        log.info(f"Searching for: '{query}'")
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
        except Exception as e:
            log.error("Query failed: %s", e)
            return []
        
        if not results or not results['documents'] or not results['documents'][0]:
            log.warning("No results found")
            return []
        
        # Format results
        formatted_results = []
        for doc, distance, metadata in zip(
            results['documents'][0],
            results['distances'][0],
            results['metadatas'][0]
        ):
            relevance = 100 * (1 - distance)  # Convert to percentage
            
            formatted_results.append({
                'text': doc,
                'relevance': relevance,
                'source': metadata.get('source'),
                'type': metadata.get('object_type'),
                'name': metadata.get('name'),
            })
        
        return formatted_results
    
    def display_results(self, results):
        """Pretty print search results"""
        if not results:
            print("No results found.\n")
            return
        
        print(f"\n{'─' * 70}")
        print(f"Found {len(results)} relevant threat intelligence chunks:")
        print(f"{'─' * 70}\n")
        
        for i, result in enumerate(results, 1):
            print(f"[{i}] {result['name']} ({result['source']})")
            print(f"    Relevance: {result['relevance']:.1f}%")
            print(f"    Type: {result['type']}")
            print(f"    Content: {result['text'][:150]}…\n")

def main():
    """Interactive search demo"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  CyberSentinel | Threat Intelligence Search  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Initialize retriever
    try:
        retriever = ThreatIntelRetriever()
    except Exception as e:
        print(f"Error: {e}")
        print("Did you run 'python build_embeddings.py' first?")
        return
    
    # Example queries
    print("Running example queries:\n")
    
    example_queries = [
        "SQL injection vulnerabilities",
        "ransomware and encryption attacks",
        "privilege escalation techniques",
        "phishing and social engineering",
        "credential dumping LSASS",
    ]
    
    for query in example_queries:
        print(f"🔍 Query: '{query}'")
        results = retriever.search(query, top_k=3)
        retriever.display_results(results)
        print()
    
    print("✓ Semantic search demo complete!")
    print("\n")

if __name__ == "__main__":
    main()
