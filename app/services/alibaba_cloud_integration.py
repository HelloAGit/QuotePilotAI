"""
alibaba_cloud_integration.py

This module demonstrates the integration of QuotePilot AI with Alibaba Cloud services.
It serves as proof that the backend infrastructure relies on Alibaba Cloud components:
1. DashScope (Model Studio) for Qwen LLM inference.
2. OSS (Object Storage Service) for storing generated quote PDFs.
3. Function Compute runtime environment detection.
4. RAM-based credential management via Environment Variables.
"""

import os
import json
import logging
from typing import Optional

# 1. Import Alibaba Cloud Specific SDKs
import dashscope  # Official SDK for Qwen/Tongyi Qianwen
from oss2 import Auth, Bucket, ObjectIterator  # Official SDK for Alibaba OSS

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlibabaCloudService:
    """
    Centralized service class for interacting with Alibaba Cloud resources.
    """

    def __init__(self):
        # PROOF POINT 1: Using Alibaba Cloud Environment Variables
        # These are injected by Alibaba Function Compute or ECS Instance RAM Role
        self.dashscope_api_key = os.getenv('DASHSCOPE_API_KEY')
        self.oss_access_key_id = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
        self.oss_access_key_secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
        self.oss_endpoint = os.getenv('OSS_ENDPOINT', 'oss-cn-hangzhou.aliyuncs.com')
        self.oss_bucket_name = os.getenv('OSS_BUCKET_NAME', 'quotepilot-assets')
        
        if not self.dashscope_api_key:
            raise ValueError("DASHSCOPE_API_KEY is missing. Ensure it is set in Alibaba Cloud FC Environment Variables.")

    def generate_quote_with_qwen(self, prompt: str) -> str:
        """
        PROOF POINT 2: Demonstrates use of Alibaba DashScope (Qwen Model).
        Calls Qwen-Max to generate quote content.
        """
        logger.info("Calling Alibaba DashScope Qwen-Max...")
        try:
            response = dashscope.Generation.call(
                model='qwen-max',
                messages=[{'role': 'user', 'content': prompt}],
                api_key=self.dashscope_api_key,
                result_format='message'
            )
            
            if response.status_code == 200:
                return response.output.choices[0].message.content
            else:
                logger.error(f"DashScope Error: {response.code} - {response.message}")
                return None
        except Exception as e:
            logger.error(f"Failed to call DashScope: {str(e)}")
            raise e

    def save_quote_to_oss(self, file_content: bytes, filename: str) -> str:
        """
        PROOF POINT 3: Demonstrates use of Alibaba OSS (Object Storage Service).
        Uploads generated PDF/HTML quotes to Alibaba Cloud storage.
        """
        logger.info(f"Uploading {filename} to Alibaba OSS bucket: {self.oss_bucket_name}")
        try:
            auth = Auth(self.oss_access_key_id, self.oss_access_key_secret)
            bucket = Bucket(auth, self.oss_endpoint, self.oss_bucket_name)
            
            # Upload file
            bucket.put_object(filename, file_content)
            
            # Return public URL (assuming bucket is configured for public read or signed URL)
            url = f"https://{self.oss_bucket_name}.{self.oss_endpoint}/{filename}"
            logger.info(f"File saved successfully at: {url}")
            return url
        except Exception as e:
            logger.error(f"Failed to upload to OSS: {str(e)}")
            raise e

    def check_alibaba_runtime(self) -> dict:
        """
        PROOF POINT 4: Detects if running within Alibaba Cloud Function Compute.
        """
        is_fc = os.getenv('FC_RUNTIME_API') is not None
        region = os.getenv('REGION_ID', 'unknown')
        
        return {
            "platform": "Alibaba Cloud",
            "service": "Function Compute" if is_fc else "ECS/Local",
            "region": region,
            "oss_connected": bool(self.oss_access_key_id),
            "dashscope_connected": bool(self.dashscope_api_key)
        }

# Singleton instance for easy import
alibaba_service = AlibabaCloudService()
