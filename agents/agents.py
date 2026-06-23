"""
Phase 3: Multi-Agent System
Three specialized agents for threat analysis
"""

import logging
from typing import Optional
from state import (
    TriageResult, CorrelationResult, PlaybookResult, 
    PlaybookStep, AgentState, ThreatIntelligence, FinalReport
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Mock LLM responses for now (we'll use real Claude API later)
class TriageAgent:
    """
    Agent 1: Analyzes alert and determines severity
    """
    
    def __init__(self):
        self.name = "Triage Agent"
        log.info(f"Initialized {self.name}")
    
    def process(self, state: AgentState) -> AgentState:
        """
        Analyze alert and determine:
        - Severity (CRITICAL, HIGH, MEDIUM, LOW)
        - Category (type of attack)
        - Confidence score
        """
        log.info(f"[{self.name}] Processing alert: {state.alert_id}")
        log.info(f"[{self.name}] Alert text: {state.alert_text[:100]}…")
        
        # Simple heuristic-based triage (replace with LLM later)
        alert_lower = state.alert_text.lower()
        
        # Determine severity
        if any(word in alert_lower for word in ["ransomware", "critical", "breach", "compromised"]):
            severity = "CRITICAL"
            confidence = 95.0
        elif any(word in alert_lower for word in ["exploit", "malware", "credential", "privilege"]):
            severity = "HIGH"
            confidence = 85.0
        elif any(word in alert_lower for word in ["suspicious", "unusual", "phishing"]):
            severity = "MEDIUM"
            confidence = 70.0
        else:
            severity = "LOW"
            confidence = 50.0
        
        # Determine category
        if "cmd" in alert_lower or "powershell" in alert_lower or "command" in alert_lower:
            category = "Command Execution"
        elif "credential" in alert_lower or "password" in alert_lower or "dump" in alert_lower:
            category = "Credential Access"
        elif "phishing" in alert_lower or "email" in alert_lower:
            category = "Initial Access"
        elif "privilege" in alert_lower or "escalation" in alert_lower:
            category = "Privilege Escalation"
        else:
            category = "Suspicious Activity"
        
        triage_result = TriageResult(
            severity=severity,
            category=category,
            confidence=confidence,
            summary=f"Alert classified as {severity} severity {category} with {confidence:.0f}% confidence"
        )
        
        state.triage = triage_result
        log.info(f"[{self.name}] ✓ Result: {severity} - {category}")
        
        return state


class ThreatCorrelatorAgent:
    """
    Agent 2: Maps alert to MITRE ATT&CK and known threats
    Uses RAG system to find relevant threat intel
    """
    
    def __init__(self, retriever=None):
        self.name = "Threat Correlator Agent"
        self.retriever = retriever  # RAG system from Phase 2
        log.info(f"Initialized {self.name}")
    
    def process(self, state: AgentState) -> AgentState:
        """
        Correlate alert with:
        - MITRE ATT&CK techniques
        - Known threat actors
        - Similar attacks
        """
        log.info(f"[{self.name}] Correlating threat…")
        
        if not state.triage:
            log.error(f"[{self.name}] Triage results required!")
            state.errors.append("Triage results missing")
            return state
        
        # Use RAG to find relevant threat intel
        intelligence = ThreatIntelligence()
        
        if self.retriever:
            log.info(f"[{self.name}] Searching RAG database…")
            results = self.retriever.search(state.alert_text, top_k=5)
            
            # Extract threat intel from results
            for result in results:
                if "T1" in result.get('text', ''):  # MITRE technique ID
                    intelligence.mitre_techniques.append(result.get('name', 'Unknown'))
                
                intelligence.relevant_articles.append(result.get('text', '')[:100])
        
        # Map to MITRE ATT&CK based on category
        category = state.triage.category if state.triage else ""
        
        mitre_mapping = {
            "Command Execution": ["T1059", "T1204"],
            "Credential Access": ["T1110", "T1555"],
            "Initial Access": ["T1566", "T1598"],
            "Privilege Escalation": ["T1548", "T1547"],
        }
        
        mitre_techniques = mitre_mapping.get(category, ["T1001"])
        
        # Map to common threat actors
        threat_actors = ["Unknown"]  # Would come from RAG
        if any(word in state.alert_text.lower() for word in ["emotet", "trickbot", "dridex"]):
            threat_actors = ["Emotet Botnet", "TrickBot"]
        elif "apt" in state.alert_text.lower():
            threat_actors = ["APT28", "APT29"]
        
        correlation_result = CorrelationResult(
            mitre_tactics=["execution"] if "T1059" in mitre_techniques else ["persistence"],
            mitre_techniques=mitre_techniques,
            threat_actors=threat_actors,
            attack_patterns=["Office Macro", "Living off the Land"] if "cmd" in state.alert_text.lower() else [],
            intelligence=intelligence
        )
        
        state.correlation = correlation_result
        log.info(f"[{self.name}] ✓ Mapped to MITRE techniques: {mitre_techniques}")
        
        return state


class PlaybookGeneratorAgent:
    """
    Agent 3: Generates incident response playbook
    Creates step-by-step remediation instructions
    """
    
    def __init__(self):
        self.name = "Playbook Generator Agent"
        log.info(f"Initialized {self.name}")
    
    def process(self, state: AgentState) -> AgentState:
        """
        Generate incident response steps:
        - Containment
        - Investigation
        - Remediation
        - Recovery
        """
        log.info(f"[{self.name}] Generating playbook…")
        
        if not state.correlation:
            log.error(f"[{self.name}] Correlation results required!")
            state.errors.append("Correlation results missing")
            return state
        
        steps = []
        
        # Step 1: Isolation (always first)
        steps.append(PlaybookStep(
            step_number=1,
            title="Isolate Affected System",
            description="Disconnect the compromised system from network to prevent lateral movement",
            estimated_time="5 minutes",
            priority="IMMEDIATE"
        ))
        
        # Step 2: Preserve Evidence
        steps.append(PlaybookStep(
            step_number=2,
            title="Preserve Evidence",
            description="Collect memory dump, logs, and artifacts for forensic analysis",
            estimated_time="15 minutes",
            priority="IMMEDIATE"
        ))
        
        # Step 3: Category-specific remediation
        if state.triage and "Command Execution" in state.triage.category:
            steps.append(PlaybookStep(
                step_number=3,
                title="Kill Malicious Processes",
                description="Terminate cmd.exe, PowerShell, and any suspicious child processes",
                estimated_time="5 minutes",
                priority="HIGH"
            ))
        
        if state.triage and "Credential" in state.triage.category:
            steps.append(PlaybookStep(
                step_number=len(steps)+1,
                title="Reset Credentials",
                description="Reset passwords for all accounts on affected system",
                estimated_time="30 minutes",
                priority="HIGH"
            ))
        
        # Step 4: Scan
        steps.append(PlaybookStep(
            step_number=len(steps)+1,
            title="Run Security Scan",
            description="Execute antivirus, EDR, and malware removal tools",
            estimated_time="1 hour",
            priority="HIGH"
        ))
        
        # Step 5: Communication
        steps.append(PlaybookStep(
            step_number=len(steps)+1,
            title="Notify Security Team",
            description="Alert security team and management about the incident",
            estimated_time="10 minutes",
            priority="IMMEDIATE"
        ))
        
        # Determine if escalation needed
        escalation_required = state.triage and state.triage.severity in ["CRITICAL", "HIGH"]
        escalation_target = "CISO" if escalation_required else "Security Team"
        
        playbook_result = PlaybookResult(
            steps=steps,
            escalation_required=escalation_required,
            escalation_target=escalation_target,
            estimated_total_time="2 hours"
        )
        
        state.playbook = playbook_result
        log.info(f"[{self.name}] ✓ Generated {len(steps)} response steps")
        
        return state


class ReporterAgent:
    """
    Agent 4: Generates final formatted report
    """
    
    def __init__(self):
        self.name = "Reporter Agent"
        log.info(f"Initialized {self.name}")
    
    def process(self, state: AgentState) -> FinalReport:
        """
        Generate final incident response report
        """
        log.info(f"[{self.name}] Generating final report…")
        
        from state import FinalReport
        
        severity = state.triage.severity if state.triage else "UNKNOWN"
        category = state.triage.category if state.triage else "Unknown"
        mitre_techniques = state.correlation.mitre_techniques if state.correlation else []
        threat_actors = state.correlation.threat_actors if state.correlation else []
        steps = state.playbook.steps if state.playbook else []
        
        recommendations = [
            "Review and update EDR configurations",
            "Conduct full network scan for similar indicators",
            "Review email security policies",
            "Conduct user awareness training"
        ]
        
        final_report = FinalReport(
            alert_id=state.alert_id,
            timestamp="2026-06-18 11:00:00",
            severity=severity,
            category=category,
            mitre_techniques=mitre_techniques,
            threat_actors=threat_actors,
            response_steps=steps,
            escalation_required=state.playbook.escalation_required if state.playbook else False,
            summary=f"Alert classified as {severity} {category}. {len(steps)} response steps generated.",
            recommendations=recommendations
        )
        
        state.final_report = final_report
        log.info(f"[{self.name}] ✓ Report complete")
        
        return state
    