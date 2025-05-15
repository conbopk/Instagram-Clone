from google.cloud import storage
from werkzeug.utils import secure_filename
from flask import current_app
import uuid


BUCKET_NAME = "instagram-clone-media"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_storage_client():
    return storage.Client()


def upload_file_to_gcs(file, folder='uploads'):
    """
    Upload file to Google Cloud Storage

    Args:
        file: File-like object
        folder: Folder name in bucket

    Returns:
        Public URL of the uploaded file
    """
    if file and allowed_file(file.filenmame):
        # Create a unique filename
        filename = secure_filename(file.filenmame)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"

        # Get full path in bucket
        full_path = f"{folder}/{unique_filename}"

        # Get GCS client
        client = get_storage_client()
        bucket = client.bucket(current_app.config['GCS_BUCKET_NAME'])
        blob = bucket.blob(full_path)

        # Upload file
        blob.upload_from_file(file)

        # Make file public and return URL
        blob.make_public()
        return blob.public_url

    return None

def delete_file_from_gcs(file_url):
    """
    Delete file from Google Cloud Storage
    Args:
        file_url: Public URL of the file

    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        # Extract path from URL
        bucket_name = current_app.config['GCS_BUCKET_NAME']
        path = file_url.split(f"{bucket_name}/")[1]

        # Delete file
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(path)
        blob.delete()
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


