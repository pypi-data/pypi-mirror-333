import json
import avro.schema
import avro.io
import io
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor
from azure.storage.blob import BlobServiceClient

# Azure Storage Credentials
STORAGE_ACCOUNT_NAME = "erioonsa"
STORAGE_ACCOUNT_KEY = "iVSFvK58XMcAWHqtSx6ETELGcLM4NTARINrp3kFPhpX50YplywBawSlqST0RYOlotnKoa8s0IpW9+AStSFvGQA=="
CONTAINER_NAME = "erioon-collection"


class ErioonClient:
    def __init__(self, api_key):
        """ Initializes session with API key and Azure Blob Storage connection """
        self.api_key = api_key
        self.blob_service = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY
        )
        self.container_client = self.blob_service.get_container_client(CONTAINER_NAME)

        # Ensure the container exists
        try:
            self.container_client.get_container_properties()
            print(f"✅ Container '{CONTAINER_NAME}' exists.")
        except Exception as e:
            print(f"❌ Container '{CONTAINER_NAME}' does not exist, creating it now...")
            self.blob_service.create_container(CONTAINER_NAME)
            print(f"✅ Container '{CONTAINER_NAME}' created.")

    def get_database(self, db_name):
        """ Returns a database instance """
        return Database(self.blob_service, db_name)


class Database:
    def __init__(self, blob_service, db_name):
        self.db_name = db_name
        self.blob_service = blob_service

    def get_collection(self, collection_name):
        """ Returns a collection instance """
        return Collection(self.blob_service, self.db_name, collection_name)


class Collection:
    def __init__(self, blob_service, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.blob_service = blob_service

        # Define Avro schema for the collection
        self.schema = avro.schema.Parse("""
        {
            "type": "record",
            "name": "SystemSettings",
            "fields": [
                {"name": "setting_name", "type": "string"},
                {"name": "value", "type": "string"}
            ]
        }
        """)
        
        # Define the blob name for the collection file
        self.blob_name = f"{self.db_name}/{self.collection_name}/collection.avro"
        self.blob_client = self.blob_service.get_blob_client(CONTAINER_NAME, self.blob_name)

    def insert_many(self, documents):
        """ Insert a batch of documents into the Azure Blob Storage in a single Avro file """
        print(f"📥 Inserting a batch of {len(documents)} documents into collection '{self.collection_name}'...")

        # Read the existing Avro data if the file already exists, else create a new file
        try:
            blob_data = self.blob_client.download_blob().readall()
            existing_data = io.BytesIO(blob_data)
            decoder = avro.io.BinaryDecoder(existing_data)
            reader = avro.io.DatumReader(self.schema)
            records = []
            while not existing_data.tell() == len(blob_data):
                records.append(reader.read(decoder))  # Read existing records
        except Exception as e:
            print("No existing file found or error reading it, creating a new one.")
            records = []

        # Append new records to existing ones
        records.extend(documents)

        # Write the updated data back to the Avro file
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer = avro.io.DatumWriter(self.schema)

        # Write all the records (existing + new) to the Avro file
        for record in records:
            writer.write(record, encoder)
        
        avro_data = bytes_writer.getvalue()

        # Save to Azure Blob Storage
        self.blob_client.upload_blob(avro_data, overwrite=True)
        print(f"✅ Batch of {len(documents)} documents stored successfully!")

    def generate_data(self, num_records):
        """ Generates fake data for testing insertion of a huge amount of data """
        data = []
        for i in range(num_records):
            setting_name = f"setting_{i}"
            value = ''.join(random.choices(string.ascii_lowercase + string.digits, k=100))  # Random 100 char string
            data.append({"setting_name": setting_name, "value": value})
        return data


# Main simulation
if __name__ == "__main__":
    print("🚀 Starting user session...")

    # Initialize the client and set up database and collection
    session = ErioonClient("123456789")
    db = session.get_database("System")
    collection = db.get_collection("system_settings")

    # Generate a large amount of data (e.g., 500,000 records)
    num_records = 1
    print(f"📊 Generating {num_records} records for insertion...")
    data = collection.generate_data(num_records)

    # Batch size for processing
    batch_size = 1
    batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

    # Start timer
    start_time = time.time()

    # Use ThreadPoolExecutor to insert data concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(collection.insert_many, batches)

    # End timer and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"✅ Successfully inserted {num_records} records in {elapsed_time:.2f} seconds.")
