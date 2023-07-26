import os
from src.constant.file_constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_REGION_NAME,AWS_SECRET_ACCESS_KEY_ENV_KEY,MODEL_BUCKET_NAME
class AwsStorage:
    '''
    Connecting to AWS using Credentials From System
    '''
    def __init__(self):
        self.ACCESS_KEY_ID = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
        self.SECRET_KEY = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)
        self.REGION_NAME = os.getenv(AWS_REGION_NAME)
        self.BUCKET_NAME = MODEL_BUCKET_NAME

    def get_aws_storage_config(self):
        return self.__dict__