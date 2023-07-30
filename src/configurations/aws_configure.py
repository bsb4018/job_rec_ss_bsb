import os
from boto3 import Session
from src.constant.file_constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_REGION_NAME,AWS_SECRET_ACCESS_KEY_ENV_KEY,MODEL_BUCKET_NAME,DATA_BUCKET_NAME,DATA_VERSION_FOLER_NAME

class AwsStorage:
    '''
    Connecting to AWS using Credentials From System
    '''
    def __init__(self):
        self.ACCESS_KEY_ID = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
        self.SECRET_KEY = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)
        self.REGION_NAME = os.getenv(AWS_REGION_NAME)
        self.BUCKET_NAME = MODEL_BUCKET_NAME
        self.DATA_BUCKET_NAME = DATA_BUCKET_NAME

    def get_aws_storage_config(self):
        return self.__dict__
    

class StorageConnection:
    """
    Created connection with S3 bucket using boto3 api to fetch the model from Repository.
    """
    def __init__(self):
        self.config = AwsStorage()
        self.session = Session(aws_access_key_id=self.config.ACCESS_KEY_ID,
                               aws_secret_access_key=self.config.SECRET_KEY,
                               region_name=self.config.REGION_NAME)
        self.s3 = self.session.resource("s3")
        self.bucket = self.s3.Bucket(self.config.BUCKET_NAME)
        self.data_bucket = self.s3.Bucket(self.config.DATA_BUCKET_NAME)

    def download_data_from_s3(self):
        """
        Download the contents of a folder directory
        Args:
            bucket_name: the name of the s3 bucket
            s3_folder: the folder path in the s3 bucket
            local_dir: a relative or absolute directory path in the local file system
        """
        
        s3_folder = DATA_VERSION_FOLER_NAME
        local_dir = DATA_VERSION_FOLER_NAME
        bucket = self.data_bucket
        for obj in bucket.objects.filter(Prefix=s3_folder):
            target = obj.key if local_dir is None \
                else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            bucket.download_file(obj.key, target)


if __name__ == "__main__":
    connection = StorageConnection()
    connection.download_data_from_s3()