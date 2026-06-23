"""
Phase 3: LangGraph Orchestrator
Chains all agents together in a workflow
"""

import logging
from typing import Optional
from state import AgentState
from agents import (
    TriageAgent, ThreatCorrelatorAgent, 
    PlaybookGeneratorAgent, ReporterAgent
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class SOCAnalystOrchestrator:
    """
    Main orchestrator that runs all agents in sequence
    """
    
    def __init__(self, retriever=None):
        self.name = "Autonomous SOC Analyst"
        self.retriever = retriever  # RAG system from Phase 2
        
        # Initialize agents
        self.triage_agent = TriageAgent()
        self.correlator_agent = ThreatCorrelatorAgent(retriever=retriever)
        self.playbook_agent = PlaybookGeneratorAgent()
        self.reporter_agent = ReporterAgent()
        
        log.info(f"Initialized {self.name}")
    
    def process_alert(self, alert_text: str, alert_id: str = "ALERT-001") -> AgentState:
        """
        Process a security alert through the entire pipeline
        
        Args:
            alert_text: The security alert description
            alert_id: Unique identifier for this alert
            
        Returns:
            AgentState with full analysis and response plan
        """
        log.info("="*60)
        log.info(f"Processing alert: {alert_id}")
        log.info("="*60)
        
        # Create initial state
        state = AgentState(
            alert_text=alert_text,
            alert_id=alert_id
        )
        
        # Run agents in sequence
        try:
            # Agent 1: Triage
            log.info("\n[1/4] Running Triage Agent…")
            state = self.triage_agent.process(state)
            
            # Agent 2: Threat Correlation
            log.info("\n[2/4] Running Threat Correlator Agent…")
            state = self.correlator_agent.process(state)
            
            # Agent 3: Playbook Generation
            log.info("\n[3/4] Running Playbook Generator Agent…")
            state = self.playbook_agent.process(state)
            
            # Agent 4: Report Generation
            log.info("\n[4/4] Running Reporter Agent…")
            state = self.reporter_agent.process(state)
            
            log.info("\n" + "="*60)
            log.info("✓ Analysis complete!")
            log.info("="*60 + "\n")
            
        except Exception as e:
            log.error(f"Error during processing: {e}")
            state.errors.append(str(e))
        
        return state
    
    def print_report(self, state: AgentState):
        """
        Pretty print the final report
        """
        if not state.final_report:
            print("No report generated")
            return
        
        report = state.final_report
        
        print("\n")
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "CYBERSENTINEL | INCIDENT RESPONSE REPORT".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        print()
        
        print(f"Alert ID:              {report.alert_id}")
        print(f"Timestamp:             {report.timestamp}")
        print(f"Severity:              {report.severity}")
        print(f"Category:              {report.category}")
        print()
        
        print("THREAT INTELLIGENCE:")
        print(f"  MITRE Techniques:    {', '.join(report.mitre_techniques)}")
        print(f"  Threat Actors:       {', '.join(report.threat_actors)}")
        print()
        
        print("INCIDENT RESPONSE PLAYBOOK:")
        for step in report.response_steps:
            print(f"\n  Step {step.step_number}: {step.title}")
            print(f"  └─ {step.description}")
            print(f"  └─ Time: {step.estimated_time} | Priority: {step.priority}")
        
        print()
        print("RECOMMENDATIONS:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"  {i}. {rec}")
        
        if report.escalation_required:
            print()
            print(f"⚠️  ESCALATION REQUIRED TO: {report.escalation_required}")
        
        print()
        print("="*70)
        print()