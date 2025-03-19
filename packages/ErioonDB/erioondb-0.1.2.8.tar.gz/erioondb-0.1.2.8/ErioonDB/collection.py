import json
from fastavro import writer, reader
from io import BytesIO
from azure.storage.blob import BlobClient

class Collection:
    def __init__(self, database, collection_name):
        self.database = database
        self.collection_name = collection_name
        self.container_client = self.database.container_client  # Assuming you can access this from Database
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the collection folder and schema.json exists in the blob storage."""
        # First, check if the schema exists in the blob storage
        schema = self.database.get_schema(self.collection_name)

        if schema is None:
            print(f"Collection '{self.collection_name}' not found. Creating it now...")
            # If the schema doesn't exist, create an empty schema
            self._create_empty_collection()
        else:
            self.schema = schema
            self._apply_schema_to_existing_avros()

    def _create_empty_collection(self):
        """Create an empty collection folder and schema.json in Azure Blob Storage."""
        schema_blob = self.database._get_blob_client(f"{self.database.db_name}/{self.collection_name}/schema.json")
        index_blob = self.database._get_blob_client(f"{self.database.db_name}/{self.collection_name}/index.json")

        # Create an empty schema (just an empty JSON object for now)
        empty_schema = {"type": "record", "name": "Collection", "fields": []} 
        try:
            schema_blob.upload_blob(json.dumps(empty_schema), overwrite=True)
            index_blob.upload_blob(json.dumps(empty_schema), overwrite=True)
            print(f"Collection '{self.collection_name}' created successfully.")
        except Exception as e:
            print(f"Error creating collection or schema.json: {e}")

    def set_schema(self, schema):
        """Set the schema for the collection and update the schema.json file."""
        schema_blob = self.database._get_blob_client(f"{self.database.db_name}/{self.collection_name}/schema.json")
        index_blob = self.database._get_blob_client(f"{self.database.db_name}/{self.collection_name}/index.json")
        
        # Upload the new schema to schema.json
        try:
            schema_blob.upload_blob(json.dumps(schema), overwrite=True)
            index_blob.upload_blob(json.dumps(schema), overwrite=True)
            self.schema = schema
            print(f"Schema for collection '{self.collection_name}' set successfully.")
            self._apply_schema_to_existing_avros()
        except Exception as e:
            print(f"Error setting schema: {e}")

    def _apply_schema_to_existing_avros(self):
        """Apply the schema to any existing Avro files in the collection."""
        # Fetch blobs directly from Azure Blob Storage
        blobs = self._get_collection_blobs()

        for blob in blobs:
            if blob.name.endswith('.avro'):
                print(f"Updating Avro file '{blob.name}' to match the new schema...")
                self._validate_and_apply_schema_to_avro(blob)

    def _get_collection_blobs(self):
        """Retrieve all blobs in the collection's folder."""
        blob_list = []
        try:
            blob_list = list(self.container_client.list_blobs(name_starts_with=f"{self.database.db_name}/{self.collection_name}/"))
        except Exception as e:
            print(f"Error fetching blobs: {e}")
        return blob_list

    def _validate_and_apply_schema_to_avro(self, blob):
        """Validate and apply the schema to an Avro file."""
        # Read the existing Avro file from blob storage
        avro_file = self.database._get_blob_client(blob.name)
        avro_data = avro_file.download_blob().readall()

        try:
            # Attempt to read the Avro data directly from the binary data
            avro_reader = reader(BytesIO(avro_data))  # This is correct
            records = list(avro_reader)

            # Validate if records match the schema (you can add additional validation if needed)
            writer(BytesIO(), self.schema, records)  # Apply the schema to the records
            print(f"Avro file '{blob.name}' is now valid with the updated schema.")
        except Exception as e:
            print(f"Error validating Avro file with schema: {e}")
            print(f"The file '{blob.name}' may not be a valid Avro file.")

    def _get_latest_avro_file(self):
        """Find the latest Avro file based on the naming convention."""
        blobs = self._get_collection_blobs()
        avro_files = [blob for blob in blobs if blob.name.endswith('.avro')]
        
        # Sort by file name (e.g., collection_name_1.avro, collection_name_2.avro...)
        avro_files.sort(key=lambda x: x.name)
        
        return avro_files[-1] if avro_files else None
    
    def _get_avro_record_count(self, avro_blob):
        """Return the number of records in the Avro file."""
        # Ensure avro_blob is a BlobClient, not BlobProperties
        if not isinstance(avro_blob, BlobClient):
            avro_blob = self.database._get_blob_client(avro_blob.name)

        avro_data = avro_blob.download_blob().readall()
        avro_reader = reader(BytesIO(avro_data))
        return len(list(avro_reader))


    def insert(self, record):
        """Insert a record into the collection."""
        print(f"Inserting record into collection '{self.collection_name}'...")
        
        # Find the latest Avro file and check the record count
        latest_avro_blob = self._get_latest_avro_file()
        
        # If no file exists or the latest file has more than 1000 records, create a new one
        if not latest_avro_blob or self._get_avro_record_count(latest_avro_blob) >= 1000:
            last_avro_num = len(self._get_collection_blobs())
            if last_avro_num == 1:
                new_avro_file_name = f"{self.database.db_name}/{self.collection_name}/{self.collection_name}_1.avro"
            else:
                new_avro_file_name = f"{self.database.db_name}/{self.collection_name}/{self.collection_name}_{len(self._get_collection_blobs()) + 1}.avro"
            self._create_new_avro_file(new_avro_file_name, [record])
        else:
            print("Not enterning")
            # Otherwise, just insert into the existing Avro file
            self.database.insert(self.collection_name, record)

    def _create_new_avro_file(self, file_name, records):
        """Create a new Avro file."""
        avro_file = self.database._get_blob_client(file_name)
    
        # Prepare a BytesIO buffer to hold the Avro data
        buffer = BytesIO()
    
        # Write records to the buffer
        try:
            writer(buffer, self.schema, records)
            buffer.seek(0)  # Ensure we are at the beginning of the buffer before uploading
            avro_file.upload_blob(buffer, overwrite=True)  # Upload the buffer as a blob
            print(f"Created new Avro file: {file_name}")
        except Exception as e:
            print(f"Error creating new Avro file: {e}")

    def insert_one(self, record):
        """Insert a single record into the collection."""
        print(f"Inserting a single record into collection '{self.collection_name}'...")
        try:
            self.insert(record)
            print(f"Record inserted successfully: {record}")
        except Exception as e:
            print(f"Error inserting record: {e}")

    def retrieve(self, record_id):
        """Retrieve a record from the collection by ID."""
        print(f"Retrieving record with ID {record_id} from collection '{self.collection_name}'...")
        return self.database.retrieve(self.collection_name, record_id)

    def delete(self, record_id):
        """Delete a record from the collection by ID."""
        print(f"Deleting record with ID {record_id} from collection '{self.collection_name}'...")
        self.database.delete(self.collection_name, record_id)

    def get_all(self):
        """Get all records in the collection."""
        print(f"Retrieving all records from collection '{self.collection_name}'...")
        return self.database._load_collection(self.collection_name)
