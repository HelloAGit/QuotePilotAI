# app/alibaba_cloud_integration.py
# Explicit Alibaba Cloud integration for Qwen Cloud proof

import os
from dashscope import Generation
import oss2

ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
REGION = os.getenv("ALIBABA_CLOUD_REGION", "cn-beijing")
BUCKET = os.getenv("ALIBABA_OSS_BUCKET")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# Configure DashScope (Qwen models)
Generation.api_key = DASHSCOPE_API_KEY

# Configure OSS client
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
endpoint = f"https://{REGION}.aliyuncs.com"
bucket_client = oss2.Bucket(auth, endpoint, BUCKET)


def test_dashscope() -> str:
    """Call DashScope Qwen model to prove backend uses Alibaba AI service."""
    resp = Generation.call(
        model="qwen-turbo",
        prompt="Say: Backend is running on Alibaba Cloud via DashScope."
    )
    # Response structure may vary slightly; adjust if needed
    return resp.get("output", {}).get("text", "No text output")


def test_oss() -> str:
    """Upload a small proof file to OSS to prove backend uses Alibaba storage."""
    content = "Backend running on Alibaba Cloud (OSS proof file)."
    bucket_client.put_object("alibaba_proof.txt", content)
    return "Uploaded alibaba_proof.txt to OSS bucket"


def run_all_tests() -> dict:
    """Run both DashScope and OSS tests and return a combined result."""
    return {
        "dashscope_output": test_dashscope(),
        "oss_status": test_oss(),
        "region_used": REGION,
        "bucket_used": BUCKET,
    }
