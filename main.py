import os
from dotenv import load_load_env
load_env() # Load environment variables early

from graph import app

def run_pipeline_demo(input_text: str, label: str):
    print(f"\n--- Running Demo Case: {label} ---")
    initial_state = {
        "raw_input": input_text,
        "customer_id": "CUST-9081",
        "intent": "",
        "extracted_requirements": {},
        "confidence_score": 0.0,
        "needs_clarification": False,
        "clarification_question": None,
        "pricing_data": None,
        "quote_data": None,
        "requires_human_approval": False,
        "approval_reason": None,
        "approval_status": "pending",
        "logs": []
    }
    
    output = app.invoke(initial_state)
    
    # Print execution history logs nicely
    print("Execution System Logs:")
    for log in output.get("logs", []):
        print(f" -> {log}")
        
    if output.get("requires_human_approval") and output.get("approval_status") == "pending":
        print(f"\n[⚠️ HUMAN APPROVAL REQUIRED]: {output['approval_reason']}")
        print("Pipeline paused successfully. Feed back state token with an update to 'approval_status' to resume.")
    elif output.get("clarification_question"):
        print(f"\n[✉️ CLARIFICATION SENT]: {output['clarification_question']}")
    else:
        print(f"\n[🏁 SUCCESS]:\n{output['quote_data']['document_body']}")

if __name__ == "__main__":
    # Case A: Standard quote process path (Auto-approves and clears)
    run_pipeline_demo(
        input_text="Hi, I need a quick price estimate for 50 base units of product. I think our usual discount code is 0.02.",
        label="Standard Processing Path"
    )
    
    # Case B: High value exception path (Triggers human intervention)
    run_pipeline_demo(
        input_text="We need an enterprise deployment of 500 units immediately. Please apply a 0.10 discount.",
        label="High Value Human-In-The-Loop Flag Trigger"
    )
