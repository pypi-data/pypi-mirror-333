from azure.storage.blob import BlobServiceClient
import json
from ErioonDB.collection import Collection
import os
from dotenv import load_dotenv
load_dotenv()

STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
STORAGE_ACCOUNT_KEY = os.getenv("STORAGE_ACCOUNT_KEY")

class Database:
    def __init__(self, db_name, container_name):
        self.db_name = db_name
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY
        )
        self.container_client = self.blob_service_client.get_container_client(container_name)

        try:
            self.container_client.create_container()
        except Exception as e:
            return None

    def _get_blob_client(self, blob_name):
        """Get a blob client for the given blob name."""
        return self.container_client.get_blob_client(blob_name)

    def set_schema(self, collection_name, schema_json):
        """Save schema in Azure Blob Storage."""
        schema_blob = self._get_blob_client(f"{self.db_name}/{collection_name}/schema.json")
        try:
            schema_blob.upload_blob(json.dumps(schema_json), overwrite=True)
        except Exception as e:
            print(f"Error setting schema: {e}")

    def get_schema(self, collection_name):
        """Retrieve schema from Azure Blob Storage."""
        schema_blob = self._get_blob_client(f"{self.db_name}/{collection_name}/schema.json")
        try:
            return json.loads(schema_blob.download_blob().readall())
        except Exception as e:
            return None 

    def _save_collection(self, collection_name, data):
        """Save collection data in Azure Blob Storage."""
        collection_blob = self._get_blob_client(f"{self.db_name}/{collection_name}.avro")
        try:
            collection_blob.upload_blob(json.dumps(data), overwrite=True)
        except Exception as e:
            print(f"Error saving collection: {e}")

    def _load_collection(self, collection_name):
        """Load collection data from Azure Blob Storage."""
        collection_blob = self._get_blob_client(f"{self.db_name}/{collection_name}.avro")
        try:
            return json.loads(collection_blob.download_blob().readall())
        except Exception as e:
            return []

    def insert(self, collection_name, record):
        """Insert a record into a collection."""
        collection_data = self._load_collection(collection_name)
        collection_data.append(record)
        self._save_collection(collection_name, collection_data)

    def retrieve(self, collection_name, record_id):
        """Retrieve a record by ID."""
        collection_data = self._load_collection(collection_name)
        return next((record for record in collection_data if record.get("id") == record_id), None)

    def delete(self, collection_name, record_id):
        """Delete a record by ID."""
        collection_data = self._load_collection(collection_name)
        collection_data = [record for record in collection_data if record.get("id") != record_id]
        self._save_collection(collection_name, collection_data)

    def __getitem__(self, collection_name):
        """Access a collection by name."""
        return Collection(self, collection_name)
