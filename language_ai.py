import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

def get_language_client():
    key = os.getenv("AZURE_LANGUAGE_KEY")
    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")

    if not key or not endpoint:
        raise ValueError(
            "Azure Language credentials not found. "
            "Check AZURE_LANGUAGE_KEY and AZURE_LANGUAGE_ENDPOINT"
        )

    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

def extract_key_skills(text: str):
    client = get_language_client()

    response = client.extract_key_phrases([text])

    if response[0].is_error:
        return []

    return response[0].key_phrases