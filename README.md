# QuotePilotAI

QuotePilot AI is an autonomous business workflow agent that handles incoming customer inquiries, understands requirements, asks clarification questions when needed, generates quotes, routes them for human approval, sends quotes to customers, and updates CRM/accounting systems.

## Overview

QuotePilotAI is a sophisticated multi-agent system built with LangGraph and LLMs that automates the complete quoting workflow. It intelligently processes customer requests, validates requirements, performs dynamic pricing calculations, and manages the approval process before finalizing quotes.

### Key Features

- **Intelligent Intent Recognition**: Automatically parses and understands customer inquiries
- **Smart Clarification**: Asks targeted follow-up questions when critical information is missing
- **Dynamic Quote Generation**: Creates professional quotes with configurable pricing and discount logic
- **Human-in-the-Loop Approval**: Routes high-value or complex quotes for human review
- **Multi-Cloud Support**: Built with Alibaba Cloud integration (DashScope, Object Storage Service)
- **State Management**: Robust workflow state tracking and logging throughout the process
- **API-Ready**: FastAPI endpoints for webhook integration with email systems and CRM platforms

## Architecture

The system uses a LangGraph-based workflow with multiple specialized agents:

- **Orchestrator Agent**: Manages the overall workflow and agent coordination
- **Intent Extraction Agent**: Parses customer requirements and intent
- **Clarification Agent**: Generates contextual follow-up questions
- **Pricing Agent**: Calculates quotes based on parameters and pricing rules
- **Approval Agent**: Determines if quotes need human review

```
Customer Inquiry 
    ↓
Intent Recognition 
    ↓
Requirement Validation 
    ↓
Clarification (if needed) 
    ↓
Quote Generation 
    ↓
Approval Gate 
    ↓
Quote Delivery & CRM Update
```

## Tech Stack

- **Python 3.8+**
- **LangGraph**: Multi-agent orchestration framework
- **LangChain**: LLM integration and prompt management
- **FastAPI**: REST API framework
- **Pydantic**: Data validation and serialization
- **Alibaba DashScope**: LLM inference (Qwen models)
- **Alibaba OSS**: Cloud object storage

## Project Structure

```
QuotePilotAI/
├── main.py                 # Entry point and demo pipeline
├── agents.py              # Agent definitions and configurations
├── graph.py               # LangGraph workflow definition
├── tools.py               # Agent tools and utilities
├── schema.py              # Data models and state schema
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── app/
│   ├── main.py           # FastAPI application
│   └── alibaba_cloud_integration.py  # Alibaba Cloud services integration
├── .env.example           # Environment variables template
└── LICENSE               # MIT License
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Alibaba Cloud account (for DashScope and OSS)
- OpenAI API key (optional, for LangChain integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HelloAGit/QuotePilotAI.git
   cd QuotePilotAI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials:
   ```

   **Required environment variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DASHSCOPE_API_KEY`: Your Alibaba DashScope API key
   - `ALIBABA_CLOUD_ACCESS_KEY_ID`: Your Alibaba Cloud access key ID
   - `ALIBABA_CLOUD_ACCESS_KEY_SECRET`: Your Alibaba Cloud access key secret
   - `ALIBABA_CLOUD_REGION`: Alibaba Cloud region (e.g., `cn-beijing`)
   - `ALIBABA_OSS_BUCKET`: Your OSS bucket name
   - `LANGCHAIN_API_KEY`: Optional, for LangChain tracing
   - `LANGCHAIN_PROJECT`: Optional, project name for tracing

### Running the Demo

The demo includes two test cases demonstrating different workflow paths:

```bash
python main.py
```

**Demo Cases:**
1. **Standard Processing Path**: A typical quote request that auto-approves
2. **High Value Human-In-The-Loop**: An enterprise request requiring human approval

### Running the API Server

Start the FastAPI server for webhook integration:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with automatic documentation at `/docs`.

## Workflow States

The system maintains a comprehensive state object throughout execution:

```python
{
    "raw_input": str,                    # Original customer inquiry
    "customer_id": str,                  # Customer identifier
    "intent": str,                       # Recognized intent
    "extracted_requirements": dict,      # Parsed requirements
    "confidence_score": float,           # Intent confidence (0-1)
    "needs_clarification": bool,         # Whether clarification is needed
    "clarification_question": str,       # Generated follow-up question
    "pricing_data": dict,                # Cost and pricing information
    "quote_data": dict,                  # Generated quote document
    "requires_human_approval": bool,     # Whether approval is required
    "approval_reason": str,              # Reason for requiring approval
    "approval_status": str,              # "pending", "approved", "rejected"
    "logs": list                         # Execution history
}
```

## Alibaba Cloud Integration

QuotePilotAI has explicit integration with Alibaba Cloud services:

### DashScope (LLM)
- Uses the Qwen-turbo model for text generation
- Configurable via `config.yaml`
- Handles all natural language processing tasks

### Object Storage Service (OSS)
- Stores generated quote documents
- Maintains audit trails and proof files
- Provides reliable document archival

**Configuration in config.yaml:**
```yaml
model: qwen-turbo
endpoint: https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
parameters:
  max_tokens: 1024
  temperature: 0.7
  top_p: 0.9
```

## API Endpoints

### Webhook Integration
- **POST** `/webhook/email`: Receive and process incoming customer emails

### Quote Management
- **GET** `/quotes/pending`: Retrieve pending quotes awaiting approval
- **POST** `/quotes/{id}/approve`: Approve and finalize a quote

## Error Handling

The system includes robust error handling for:
- Missing or invalid customer data
- API rate limiting
- Network failures
- Invalid approval states
- Processing timeouts

## Logging

Comprehensive logging is maintained throughout the workflow. Each execution generates:
- Agent action logs
- Tool invocation records
- State transitions
- Error messages

Access logs via the `logs` field in the output state.

## Testing

Run the included demo pipeline to test the complete workflow:

```bash
python main.py
```

The demo validates:
- Intent recognition accuracy
- Requirement extraction
- Quote generation
- Approval logic
- State management

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bug reports and feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ using LangGraph, LangChain, and Alibaba Cloud**
