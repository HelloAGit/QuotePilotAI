from langgraph.graph import StateGraph, END
from schema import AgentState
from agents import inquiry_understanding_agent, clarification_agent, quote_generation_agent
from tools import calculate_pricing_and_policy, mock_crm_update, mock_send_email

# Define Core Node Operations
def process_inquiry(state: AgentState):
    return inquiry_understanding_agent(state)

def ask_clarification(state: AgentState):
    res = clarification_agent(state)
    mock_send_email(f"client_{state['customer_id']}@firm.com", "Action Required: Order Clarification", res["clarification_question"])
    return res

def compute_pricing(state: AgentState):
    pricing = calculate_pricing_and_policy(state["extracted_requirements"])
    return {
        "pricing_data": pricing,
        "requires_human_approval": pricing["requires_approval"],
        "approval_reason": pricing["approval_reason"],
        "logs": state.get("logs", []) + [f"Deterministic pricing ran. Flagged Approval = {pricing['requires_approval']}"]
    }

def generate_quote(state: AgentState):
    return quote_generation_agent(state)

def finalize_workflow(state: AgentState):
    # Conditional sync logic representation based on manual override
    final_status = "Auto-sent to client" if not state.get("requires_human_approval") else f"Approved by Manager: {state.get('approval_status')}"
    sync_log = mock_crm_update({"quote": state.get("quote_data"), "status": final_status})
    return {"logs": state.get("logs", []) + [f"Workflow completed. CRM Sync status: {sync_log}"]}

# Router Logic Functions
def route_after_parsing(state: AgentState):
    if state["needs_clarification"]:
        return "clarify"
    return "pricing"

def route_after_policy(state: AgentState):
    if state["requires_human_approval"] and state["approval_status"] == "pending":
        return "human_checkpoint"
    return "generate_quote"

# State Machine Compilation Setup
workflow = StateGraph(AgentState)

# Add Node mapping instances
workflow.add_node("inquiry_understanding", process_inquiry)
workflow.add_node("clarification_node", ask_clarification)
workflow.add_node("pricing_node", compute_pricing)
workflow.add_node("quote_gen_node", generate_quote)
workflow.add_node("finalization_node", finalize_workflow)

# Build Edge Paths
workflow.set_entry_point("inquiry_understanding")

workflow.add_conditional_edges(
    "inquiry_understanding",
    route_after_parsing,
    {
        "clarify": "clarification_node",
        "pricing": "pricing_node"
    }
)

workflow.add_edge("clarification_node", END)

workflow.add_conditional_edges(
    "pricing_node",
    route_after_policy,
    {
        "human_checkpoint": END, # Pause execution graph runtime for manual UI interaction 
        "generate_quote": "quote_gen_node"
    }
)

workflow.add_edge("quote_gen_node", "finalization_node")
workflow.add_edge("finalization_node", END)

# Compile Application Interface
app = workflow.compile()
