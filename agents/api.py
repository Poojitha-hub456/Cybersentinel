"""
Phase 4: FastAPI Backend
Exposes the SOC analyst as REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from orchestrator import SOCAnalystOrchestrator
from state import AgentState, FinalReport

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CyberSentinel API",
    description="Autonomous SOC Analyst API",
    version="1.0.0"
)

# Add CORS middleware (allows requests from Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = SOCAnalystOrchestrator(retriever=None)

# ─────────────────────────────────────────────────────────────────────────────
# Request/Response Models
# ─────────────────────────────────────────────────────────────────────────────

class AlertRequest(BaseModel):
    """Incoming alert request"""
    alert_text: str
    alert_id: Optional[str] = "ALERT-001"

class PlaybookStepResponse(BaseModel):
    """Single playbook step"""
    step_number: int
    title: str
    description: str
    estimated_time: str
    priority: str

class IncidentReportResponse(BaseModel):
    """Complete incident report response"""
    alert_id: str
    timestamp: str
    severity: str
    category: str
    mitre_techniques: List[str]
    threat_actors: List[str]
    response_steps: List[PlaybookStepResponse]
    escalation_required: bool
    summary: str
    recommendations: List[str]

# ─────────────────────────────────────────────────────────────────────────────
# API Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "name": "CyberSentinel API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "POST /analyze",
            "health": "GET /health",
            "sample-alerts": "GET /sample-alerts"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CyberSentinel Autonomous SOC Analyst"
    }

@app.post("/analyze", response_model=IncidentReportResponse)
async def analyze_alert(request: AlertRequest):
    """
    Main endpoint: Analyze a security alert
    
    Args:
        alert_text: The security alert text
        alert_id: Unique alert identifier
        
    Returns:
        Structured incident response report
    """
    try:
        log.info(f"Received alert: {request.alert_id}")
        
        # Process alert through orchestrator
        state = orchestrator.process_alert(request.alert_text, request.alert_id)
        
        if not state.final_report:
            raise HTTPException(status_code=500, detail="Failed to generate report")
        
        report = state.final_report
        
        # Convert playbook steps to response format
        steps = [
            PlaybookStepResponse(
                step_number=step.step_number,
                title=step.title,
                description=step.description,
                estimated_time=step.estimated_time,
                priority=step.priority
            )
            for step in report.response_steps
        ]
        
        return IncidentReportResponse(
            alert_id=report.alert_id,
            timestamp=report.timestamp,
            severity=report.severity,
            category=report.category,
            mitre_techniques=report.mitre_techniques,
            threat_actors=report.threat_actors,
            response_steps=steps,
            escalation_required=report.escalation_required,
            summary=report.summary,
            recommendations=report.recommendations
        )
        
    except Exception as e:
        log.error(f"Error analyzing alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sample-alerts")
async def get_sample_alerts():
    """Return sample alerts for testing"""
    return {
        "alerts": [
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
    }

# ─────────────────────────────────────────────────────────────────────────────
# Run server
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)