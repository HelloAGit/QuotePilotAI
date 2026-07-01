from typing import Dict, Any

def calculate_pricing_and_policy(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic calculation engine. Eliminates LLM hallucinations for pricing.
    """
    base_unit_price = 100.0
    quantity = int(requirements.get("quantity", 1))
    requested_discount = float(requirements.get("discount", 0.0))
    
    gross_value = base_unit_price * quantity
    applied_discount = min(requested_discount, 0.20) # Max 20% cap hard rule
    net_value = gross_value * (1 - applied_discount)
    
    # Dynamic Policy Validations (Human-in-the-loop Triggers)
    requires_approval = False
    approval_reason = None
    
    if net_value > 25000:
        requires_approval = True
        approval_reason = "High-value quote threshold exceeded (> $25,000)"
    elif applied_discount > 0.05:
        requires_approval = True
        approval_reason = "Requested discount exceeds normal limit (> 5%)"
        
    return {
        "gross_value": gross_value,
        "discount_applied": applied_discount,
        "net_value": net_value,
        "requires_approval": requires_approval,
        "approval_reason": approval_reason,
        "tax_rules": "Standard State Tax Apply"
    }

def mock_crm_update(state_data: Dict[str, Any]) -> str:
    return "Successfully synced log files and quote snapshot to CRM Database."

def mock_send_email(recipient: str, subject: str, content: str) -> str:
    return f"Email dispatched successfully to {recipient}."
