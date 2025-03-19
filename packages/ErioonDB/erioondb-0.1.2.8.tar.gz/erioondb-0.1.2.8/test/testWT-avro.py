import json
import avro.schema
import avro.io
import io
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import os

# Azure Storage Credentials
STORAGE_ACCOUNT_NAME = "erioonstorage"  # Replace with your storage account name
STORAGE_ACCOUNT_KEY = "3OrHPLFyuwMRytBDEK+WYyl/cVkkRL9gYe0WQqMcL+S3M1RhSllKNSWTtSsI8LB/VBi5/HX/aVH4+AStiTI9Ow=="  # Replace with your storage account key
CONTAINER_NAME = "user-info"  # Blob storage container name


# Initialize Azure BlobServiceClient
blob_service_client = BlobServiceClient(account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net", credential=STORAGE_ACCOUNT_KEY)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Check if the container exists, and create it if necessary
def create_container_if_not_exists(container_client):
    try:
        # Try to get the container properties (this will raise an exception if the container doesn't exist)
        container_client.get_container_properties()
        print(f"Container '{CONTAINER_NAME}' already exists.")
    except Exception as e:
        # Container does not exist, so create it
        print(f"Container '{CONTAINER_NAME}' not found, creating it...")
        container_client.create_container()
        print(f"Container '{CONTAINER_NAME}' created.")

# Create the container if it doesn't exist
create_container_if_not_exists(container_client)

# Create a simple user schema for Avro
schema = {
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "_id", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "surname", "type": "string"},
        {"name": "email", "type": "string"},
    ]
}

# Parse the schema
avro_schema = avro.schema.parse(json.dumps(schema))

# Create user data
user_data = {
    "_id": "12345",
    "name": "John Doe",
    "surname": "test",
    "email": "johndoe@example.com",
}

# Convert user data to Avro format (Binary)
def convert_to_avro(data, schema):
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer = avro.io.DatumWriter(schema)
    writer.write(data, encoder)
    return bytes_writer.getvalue()

# Convert to Avro binary format
avro_binary_data = convert_to_avro(user_data, avro_schema)

# Define the Avro file blob name
avro_blob_name = f"user_{user_data['_id']}_avro.avro"
avro_blob_client = container_client.get_blob_client(avro_blob_name)

# Upload the Avro data to Azure Blob Storage
print(f"Uploading Avro data to Blob Storage as '{avro_blob_name}'...")
avro_blob_client.upload_blob(avro_binary_data, overwrite=True)
print(f"Avro data uploaded to {avro_blob_name}")

# Simulate saving data in WiredTiger-like format (binary file)
# Normally, WiredTiger format is managed by MongoDB, but here we'll just create a simple binary format for demonstration

wt_data = json.dumps(user_data).encode('utf-8')  # Simple binary encoding of user data (not actual WT format)

# Define the WT file blob name
wt_blob_name = f"user_{user_data['_id']}_wt.wt"
wt_blob_client = container_client.get_blob_client(wt_blob_name)

# Upload the WT data to Azure Blob Storage
print(f"Uploading WiredTiger-like data to Blob Storage as '{wt_blob_name}'...")
wt_blob_client.upload_blob(wt_data, overwrite=True)
print(f"WiredTiger-like data uploaded to {wt_blob_name}")

print("✅ User info stored in both Avro and WiredTiger-like formats in Azure Blob Storage!")