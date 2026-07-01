from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field

class InquiryAnalysis(BaseModel):
    intent: str = Field(description="The primary goal of the customer (e.g., Request Quote, Feature Inquiry)")
    extracted_requirements: Dict[str, Any] = Field(description="Extracted variables like quantities, models, dates")
    urgency: str = Field(description="Estimated urgency: Low, Medium, High")
    confidence_score: float = Field(description="Confidence value between 0.0 and 1.0")
    needs_clarification: bool = Field(description="True if mandatory data is missing to calculate a quote")

class AgentState(TypedDict):
    # Core Inputs / Context
    raw_input: str
    customer_id: str
    
    # Analysis & Routing State
    intent: str
    extracted_requirements: Dict[str, Any]
    confidence_score: float
    needs_clarification: bool
    clarification_question: Optional[str]
    
    # Execution & Document State
    pricing_data: Optional[Dict[str, Any]]
    quote_data: Optional[Dict[str, Any]]
    
    # Policy & Human-in-the-loop State
    requires_human_approval: bool
    approval_reason: Optional[str]
    approval_status: str # "pending", "approved", "rejected"
    
    # System Actions
    logs: List[str]
