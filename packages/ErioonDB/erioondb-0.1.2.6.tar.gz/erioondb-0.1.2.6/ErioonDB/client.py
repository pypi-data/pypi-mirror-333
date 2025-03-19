from azure.storage.blob import BlobServiceClient
from ErioonDB.auth import Auth
from ErioonDB.database import Database
import os
import json
from dotenv import load_dotenv
load_dotenv()

STORAGE_ACCOUNT_NAME = "erioonappstorage"
STORAGE_ACCOUNT_KEY = "uJLDbKohah/jrHNoWVds1OnTWeHlu/9NNIzJJ9RVZqMuV+ATGfRCIXNBuxrnSWzOXxcJ0bQ98q3S+AStQoo3lg=="

class ErioonClient:
    def __init__(self, auth_string, container_name):
        """
        Initialize ErioonClient with authentication using provided credentials.
        """
        self.auth_string = auth_string
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY
        )
        
        try:
            self.container_client = self.blob_service_client.get_container_client(container_name)

            if not self.container_client.exists():
                print(f"The provided user id does not exist. Please login or register at www.erioon.com/register to enable access.")
                return 
            else:
                self._authenticate(auth_string)

        except Exception as e:
            print(f"Error: {str(e)}")
            

    def _authenticate(self, auth_string):
        """Authenticate the user using the provided credentials (API_KEY/email:password)."""
        self.auth = Auth()
        self.authenticated, self.user_email, self.api_key = self.auth.authenticate(auth_string)

        if not self.authenticated:
            raise ValueError("Authentication failed. Invalid API Key or credentials.")
    
    def __call__(self, user_id):
        """Retrieve the user's database or create it if it doesn't exist."""
        if not self.container_client.exists():
            return "No ErioonDB account found. Please register at www.erioon.com/register"

        user_db_folder = f"{user_id}/" 
        user_db_blobs = self.container_client.list_blobs(name_starts_with=user_db_folder)
        
        db_found = False
        for blob in user_db_blobs:
            if blob.name.startswith(user_db_folder):
                db_found = True
                break

        if not db_found:
            print(f"Database '{user_id}' does not exist. Creating it now...")
            return self.create_database(user_id)
        else:
            return Database(user_id, self.container_name)

    def create_database(self, db_name):
        """Create a new user database folder inside the container."""
        user_db_folder = f"{db_name}/" 
        sys_settings_collection = f"{user_db_folder}sys_settings/"
        sys_settings_blob_client = self.container_client.get_blob_client(f"{sys_settings_collection}settings.json")
        
        try:
            empty_settings = {} 
            sys_settings_blob_client.upload_blob(json.dumps(empty_settings), overwrite=True)
            print(f"Database {db_name} created successfully!")
        except Exception as e:
            print(f"Error creating sys_settings collection or settings.json: {str(e)}")
        
        user_db = Database(db_name, self.container_name)
        return user_db
