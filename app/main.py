from fastapi import FastAPI, Webhook
from app.agents.orchestrator import app as agent_app

app = FastAPI()

@app.post("/webhook/email")
async def handle_incoming_email(payload: dict):
    # 1. Parse email
    # 2. Run Agent
    result = agent_app.invoke({"customer_email": payload['body'], "messages": []})
    # 3. Save to DB
    # 4. If missing info, send email. If complete, save as 'Pending Approval'
    return {"status": "processed"}

@app.get("/quotes/pending")
async def get_pending_quotes():
    # Fetch quotes needing human approval
    pass

@app.post("/quotes/{id}/approve")
async def approve_quote(id: int):
    # Trigger final email sending and CRM update
    pass
