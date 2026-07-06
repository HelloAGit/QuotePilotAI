# QuotePilotAI
QuotePilot AI is an autonomous business workflow agent that handles incoming customer inquiries, understands the requirement, asks clarification questions when needed, generates a quote, routes it for human approval, sends the quote to the customer, and updates CRM/accounting systems.


## Alibaba Cloud Deployment Proof

This backend explicitly integrates with Alibaba Cloud services:

- Imports Alibaba Cloud SDKs: `dashscope` (Qwen models) and `oss2` (Object Storage Service).
- Uses Alibaba-specific environment variables:
  - `ALIBABA_CLOUD_ACCESS_KEY_ID`
  - `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
  - `ALIBABA_CLOUD_REGION`
  - `DASHSCOPE_API_KEY`
  - `ALIBABA_OSS_BUCKET`
- Interacts with core Alibaba services in `app/alibaba_cloud_integration.py`:
  - Calls DashScope (`qwen-turbo`) for text generation.
  - Uploads a proof file (`alibaba_proof.txt`) to OSS.

To run the proof locally or on Alibaba Cloud:

```bash
pip install -r requirements.txt
python main.py
