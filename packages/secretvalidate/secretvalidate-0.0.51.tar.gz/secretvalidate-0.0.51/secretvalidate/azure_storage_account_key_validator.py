from azure.storage.blob import BlobServiceClient
from secretvalidate.env_loader import (
    get_secret_active,
    get_secret_inactive,
    get_secret_inconclusive,
)
import base64
import re


def extract_connection_string(text):
    pattern = r"(DefaultEndpointsProtocol=https;AccountName=(?P<AccountName>\w+);AccountKey=(?P<AccountKey>[\w+/=]+);EndpointSuffix=core\.windows\.net)"
    match = re.search(pattern, text)
    if match:
        string = match.group(1)
        if "BlobEndpoint" not in string:
            return match.group(1)
        pattern = r"(DefaultEndpointsProtocol.*?==)"
        blob_match = re.search(pattern, text)
        return blob_match.group(1)
    return


def build_connection_string(blob, secret):
    pattern1 = r"((?<=Microsoft\.Storage\/storageAccounts\/)[^\/]+)"
    match = re.search(pattern1, blob)
    if match:
        account_name = match.group(0)
        return f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={secret};EndpointSuffix=core.windows.net"

    return get_secret_inconclusive()


def validate_azure_storage_account_key(blob, secret, response):
    try:
        connection_string = None
        blob_type = blob["type"]

        if blob_type == "pull_request_comment":
            connection_string = build_connection_string(blob["blob"], secret)
        if blob_type == "commit":
            try:
                content = base64.b64decode(blob["blob"]).decode("utf-8")
            except UnicodeDecodeError:
                content = base64.b64decode(blob["blob"]).decode("latin-1")
            connection_string = extract_connection_string(content)

        container_name = "dummy"
        if not connection_string or "Inconclusive" in connection_string:
            return f"{get_secret_inconclusive()}: Unable to form or extract connection string"
        else:
            blob_client = BlobServiceClient.from_connection_string(connection_string)
            container_client = blob_client.get_container_client(container_name)
            # If we can list a blob, the key is valid
            blobs_list = container_client.list_blobs()
            for blob in blobs_list:
                print(blob.name)
                break
            return (
                get_secret_active()
                if response
                else "Azure Storage Account Key is valid"
            )
    except Exception as e:
        if "ErrorCode:AuthenticationFailed" in str(e) or "Failed to resolve" in str(e):
            return (
                get_secret_inactive()
                if response
                else "Azure Storage Account Key is invalid"
            )
        elif "ErrorCode:ContainerNotFound" in str(e) or "AuthorizationFailure":
            return (
                get_secret_active()
                if response
                else "Azure Storage Account Key is valid"
            )
        else:
            return (
                f"{get_secret_inconclusive()} validation: {e}"
                if response
                else f"Inconclusive validation: {e}"
            )
