from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from dashscope import Generation
import json

class AgentState(TypedDict):
    customer_email: str
    extracted_data: dict
    missing_info: List[str]
    quote_draft: str
    approval_status: str # 'pending', 'approved', 'rejected'
    messages: List[dict]

def extract_requirements(state: AgentState):
    # Call Qwen-Max to extract JSON from email
    prompt = f"Extract details from: {state['customer_email']}"
    response = Generation.call(model='qwen-max', messages=[{'role': 'user', 'content': prompt}])
    # Parse JSON response into state['extracted_data']
    return state

def check_completeness(state: AgentState):
    if not state['extracted_data'].get('quantity'):
        state['missing_info'].append("Quantity is missing")
    return state

def generate_quote(state: AgentState):
    # Use deterministic pricing engine + Qwen for narrative
    price = calculate_quote_total(state['extracted_data']['items'])
    state['quote_draft'] = f"Total: ${price}. Details: ..."
    return state

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("extract", extract_requirements)
workflow.add_node("check", check_completeness)
workflow.add_node("quote", generate_quote)

workflow.set_entry_point("extract")
workflow.add_edge("extract", "check")
workflow.add_conditional_edges(
    "check",
    lambda state: "quote" if not state['missing_info'] else END
)
workflow.add_edge("quote", END)

app = workflow.compile()
