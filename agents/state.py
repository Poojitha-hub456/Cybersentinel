"""
Phase 3: Agent State & Data Models
Defines the structure of data flowing between agents
"""

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class ThreatIntelligence:
    """Threat intelligence from RAG system"""
    mitre_techniques: List[str] = field(default_factory=list)
    relevant_articles: List[str] = field(default_factory=list)
    similar_attacks: List[str] = field(default_factory=list)
    threat_actors: List[str] = field(default_factory=list)

@dataclass
class TriageResult:
    """Output from Triage Agent"""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # e.g., "Command Execution", "Credential Access"
    confidence: float  # 0-100%
    summary: str  # Brief explanation

@dataclass
class CorrelationResult:
    """Output from Threat Correlator Agent"""
    mitre_tactics: List[str]  # e.g., ["execution", "persistence"]
    mitre_techniques: List[str]  # e.g., ["T1059", "T1566"]
    threat_actors: List[str]  # Known APT groups
    attack_patterns: List[str]  # Known attack names
    intelligence: ThreatIntelligence

@dataclass
class PlaybookStep:
    """Single step in incident response"""
    step_number: int
    title: str
    description: str
    estimated_time: str  # "5 minutes", "1 hour", etc.
    priority: str  # IMMEDIATE, HIGH, NORMAL

@dataclass
class PlaybookResult:
    """Output from Playbook Generator Agent"""
    steps: List[PlaybookStep]
    escalation_required: bool
    escalation_target: str  # e.g., "CISO", "Security Team"
    estimated_total_time: str

@dataclass
class FinalReport:
    """Final incident response report"""
    alert_id: str
    timestamp: str
    severity: str
    category: str
    mitre_techniques: List[str]
    threat_actors: List[str]
    response_steps: List[PlaybookStep]
    escalation_required: bool
    summary: str
    recommendations: List[str]

@dataclass
class AgentState:
    """Main state passed through LangGraph workflow"""
    # Input
    alert_text: str
    alert_id: str = "ALERT-001"
    
    # Triage output
    triage: Optional[TriageResult] = None
    
    # Correlation output
    correlation: Optional[CorrelationResult] = None
    
    # Playbook output
    playbook: Optional[PlaybookResult] = None
    
    # Final report
    final_report: Optional[FinalReport] = None
    
    # Errors
    errors: List[str] = field(default_factory=list)