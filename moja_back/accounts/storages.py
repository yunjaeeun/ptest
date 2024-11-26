from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class CustomS3Storage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

    def url(self, name):
        """
        Returns the static S3 URL for a file instead of generating a presigned URL.
        """
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/media/{name}"
