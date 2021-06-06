from storages.backends.s3boto3 import S3Boto3Storage, S3Boto3StorageFile


class StaticStorage(S3Boto3Storage):
    location = "static/"
    file_overwrite = False


class UploadStorage(S3Boto3Storage, S3Boto3StorageFile):
    location = "uploads/"