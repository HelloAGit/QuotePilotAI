import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from schema import AgentState, InquiryAnalysis

# Swapping the backend to Qwen Cloud via its OpenAI-compatible endpoint
llm = ChatOpenAI(
    model="qwen3.7-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    temperature=0
)

def inquiry_understanding_agent(state: AgentState) -> Dict[str, Any]:
    """Classifies user intent, extracts fields, and assigns evaluation marks."""
    system_prompt = (
        "You are an expert Inquiry Understanding Agent. Analyze the client's input. "
        "Extract key entities, quantify details, identify missing information, and score your extraction confidence."
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Customer Input: {raw_input}")
    ])
    
    # Force structured LLM response matching our schema
    structured_llm = llm.with_structured_output(InquiryAnalysis)
    chain = prompt | structured_llm
    analysis = chain.invoke({"raw_input": state["raw_input"]})
    
    # Enforce minimum data confidence constraints
    needs_clarify = analysis.needs_clarification or (analysis.confidence_score < 0.75)
    
    return {
        "intent": analysis.intent,
        "extracted_requirements": analysis.extracted_requirements,
        "confidence_score": analysis.confidence_score,
        "needs_clarification": needs_clarify,
        "logs": state.get("logs", []) + ["Inquiry parsed successfully."]
    }

def clarification_agent(state: AgentState) -> Dict[str, Any]:
    """Asks minimal information questions targeting critical pricing details missing."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a customer relationship coordinator. Write a polite email asking for the missing variables needed to process an order without asking redundant queries."),
        ("user", "Current parsed state: {extracted_requirements}")
    ])
    chain = prompt | llm
    response = chain.invoke({"extracted_requirements": state["extracted_requirements"]})
    
    return {
        "clarification_question": response.content,
        "logs": state.get("logs", []) + ["Generated clarification follow-up question."]
    }

def quote_generation_agent(state: AgentState) -> Dict[str, Any]:
    """Formats calculated data arrays into structured visual quote content."""
    pricing = state["pricing_data"]
    requirements = state["extracted_requirements"]
    
    quote_summary = (
        f"=== COMMERCIAL QUOTE ===\n"
        f"Customer Account Ref: {state['customer_id']}\n"
        f"Calculated Gross base value: ${pricing['gross_value']:.2f}\n"
        f"Discount Rate adjustment: {pricing['discount_applied'] * 100}%\n"
        f"Net Terms Due total: ${pricing['net_value']:.2f}\n"
        f"Legal terms: Standard 30-day fulfillment applies."
    )
    return {
        "quote_data": {"document_body": quote_summary},
        "logs": state.get("logs", []) + ["Quote generated successfully."]
    }
