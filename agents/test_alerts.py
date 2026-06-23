"""
Phase 3: Test Alerts
Sample security alerts to test the SOC analyst
"""

import logging
from orchestrator import SOCAnalystOrchestrator

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Sample alerts
TEST_ALERTS = [
    {
        "id": "ALERT-001",
        "text": "Suspicious process spawning: cmd.exe spawned from Excel.exe with unusual command line arguments attempting to download file from external URL"
    },
    {
        "id": "ALERT-002",
        "text": "Credential Access Alert: Multiple failed RDP login attempts followed by successful login from unusual geographic location with extracted LSASS memory dump"
    },
    {
        "id": "ALERT-003",
        "text": "Ransomware Detection: File encryption activity detected on file server with ransom note dropped in multiple directories"
    },
    {
        "id": "ALERT-004",
        "text": "Phishing Email: User reported suspicious email with malicious attachment claiming to be from IT department requesting urgent password update"
    },
    {
        "id": "ALERT-005",
        "text": "Privilege Escalation: Unusual UAC bypass attempt detected using token impersonation technique"
    },
]

def main():
    """
    Run the SOC analyst on test alerts
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "CyberSentinel | Autonomous SOC Analyst - Phase 3 Test".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Initialize orchestrator (no RAG yet, will add later)
    orchestrator = SOCAnalystOrchestrator(retriever=None)
    
    # Process ALL alerts
    for i, alert in enumerate(TEST_ALERTS, 1):
        state = orchestrator.process_alert(alert['text'], alert['id'])
        orchestrator.print_report(state)
        
        # Pause between alerts
        if i < len(TEST_ALERTS):
            print("\n" + "─" * 70)
            input("Press Enter to process next alert...")
    
    # Print report
    orchestrator.print_report(state)
    
    # Show all available alerts
    print("\nOther sample alerts available:")
    for alert in TEST_ALERTS[1:]:
        print(f"  - {alert['id']}: {alert['text'][:60]}…")
    
    print("\n")

if __name__ == "__main__":
    main()