import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load .env file
load_dotenv()

def upload_to_blob(file_path: str):
    connect_str = os.getenv("BLOB_CONNECTION_STRING")

    if not connect_str:
        raise ValueError(
            "BLOB_CONNECTION_STRING not found. "
            "Check .env file or environment variables."
        )

    container_name = "resumes"

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob=file_path)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)