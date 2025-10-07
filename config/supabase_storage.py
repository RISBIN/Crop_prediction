"""
Supabase Storage Backend for Django
Handles image uploads to Supabase Storage buckets
"""
import os
from io import BytesIO
from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
from datetime import datetime


class SupabaseStorage(Storage):
    """Custom storage backend for Supabase Storage"""

    def __init__(self, bucket_name='soil-images'):
        self.bucket_name = bucket_name
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.base_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket_name}"

    def _save(self, name, content):
        """
        Save file to Supabase Storage
        """
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{name}"

        # Read file content
        if hasattr(content, 'read'):
            file_content = content.read()
        else:
            file_content = content

        try:
            # Upload to Supabase Storage
            result = self.supabase.storage.from_(self.bucket_name).upload(
                path=filename,
                file=file_content,
                file_options={"content-type": self._get_content_type(name)}
            )
            return filename
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")
            # Fallback to local storage if upload fails
            return name

    def _open(self, name, mode='rb'):
        """
        Open file from Supabase Storage
        """
        try:
            # Download from Supabase
            response = self.supabase.storage.from_(self.bucket_name).download(name)
            return BytesIO(response)
        except Exception as e:
            print(f"Error downloading from Supabase: {e}")
            return None

    def exists(self, name):
        """
        Check if file exists in Supabase Storage
        """
        try:
            files = self.supabase.storage.from_(self.bucket_name).list()
            return any(f['name'] == name for f in files)
        except:
            return False

    def url(self, name):
        """
        Return public URL for file
        """
        return f"{self.base_url}/{name}"

    def delete(self, name):
        """
        Delete file from Supabase Storage
        """
        try:
            self.supabase.storage.from_(self.bucket_name).remove([name])
            return True
        except Exception as e:
            print(f"Error deleting from Supabase: {e}")
            return False

    def size(self, name):
        """
        Return file size
        """
        try:
            files = self.supabase.storage.from_(self.bucket_name).list()
            for f in files:
                if f['name'] == name:
                    return f.get('metadata', {}).get('size', 0)
            return 0
        except:
            return 0

    def _get_content_type(self, name):
        """
        Determine content type from file extension
        """
        ext = os.path.splitext(name)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
        }
        return content_types.get(ext, 'application/octet-stream')


class SoilImageStorage(SupabaseStorage):
    """Storage for soil classification images"""
    def __init__(self):
        super().__init__(bucket_name='soil-images')


class ProfilePictureStorage(SupabaseStorage):
    """Storage for user profile pictures"""
    def __init__(self):
        super().__init__(bucket_name='profile-pictures')
