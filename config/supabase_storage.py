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
        try:
            self.supabase = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            self.base_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket_name}"
        except Exception as e:
            # Fallback to None if Supabase fails to initialize
            print(f"[WARNING] Supabase storage initialization failed: {e}")
            print("[INFO] Will use local file storage instead")
            self.supabase = None
            self.base_url = None

    def _save(self, name, content):
        """
        Save file to Supabase Storage or local storage as fallback
        """
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{name}"

        # Read file content
        if hasattr(content, 'read'):
            file_content = content.read()
        else:
            file_content = content

        # Try Supabase if available
        if self.supabase:
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

        # Fallback to local filesystem storage
        from django.core.files.storage import FileSystemStorage
        from django.conf import settings
        local_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

        # Reset content for local storage
        if hasattr(content, 'seek'):
            content.seek(0)

        return local_storage.save(name, content)

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
        if self.base_url:
            return f"{self.base_url}/{name}"
        else:
            # Fallback to local media URL
            from django.conf import settings
            return f"{settings.MEDIA_URL}{name}"

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
