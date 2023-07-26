import os,sys
from src.logger import logging
from src.exception import JobRecException
from src.constant.file_constants import SAVED_MODEL_DIR,SAVED_MODEL_FILE_NAME
from src.configurations.aws_configure import AwsStorage
from boto3 import Session

class LoadIndex:
    def __init__(self,):
        try:
            self.index_file_path = os.path.join(SAVED_MODEL_DIR)
        except Exception as e:
            raise JobRecException(e,sys)

    def download_latest_model(self,bucket):
        try:
            logging.info("Connecting to Bucket -> Starting Download")
            s3_folder = "production"
            local_dir = SAVED_MODEL_DIR
            bucket = bucket
            for obj in bucket.objects.filter(Prefix=s3_folder):
                target = obj.key if local_dir is None \
                    else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
                if not os.path.exists(os.path.dirname(target)):
                    os.makedirs(os.path.dirname(target))
                if obj.key[-1] == '/':
                    continue
                bucket.download_file(obj.key, target)

            logging.info("Download Complete")
        except Exception as e:
            raise JobRecException(e,sys)
        
    def timestamp_converter(self,integer_timestamp):
        try:
            # Convert the integer back to individual components
            second = integer_timestamp % 100
            integer_timestamp //= 100
            minute = integer_timestamp % 100
            integer_timestamp //= 100
            hour = integer_timestamp % 100
            integer_timestamp //= 100

            year = integer_timestamp % 10000
            integer_timestamp //= 10000
            day = integer_timestamp % 100
            integer_timestamp //= 100
            month = integer_timestamp % 100
            
            # Format the components as strings with leading zeros if necessary
            day_str = str(day).zfill(2)
            month_str = str(month).zfill(2)
            year_str = str(year).zfill(4)
            hour_str = str(hour).zfill(2)
            minute_str = str(minute).zfill(2)
            second_str = str(second).zfill(2)

            # Concatenate the components with underscores
            timestamp = f"{month_str}_{day_str}_{year_str}_{hour_str}_{minute_str}_{second_str}"
            return timestamp
        
        except Exception as e:
            raise JobRecException(e,sys)

    
    def get_best_index_path(self,) -> str:
        try:
            if not os.path.exists(self.index_file_path):
                config = AwsStorage()
                session = Session(aws_access_key_id=config.ACCESS_KEY_ID,
                                   aws_secret_access_key=config.SECRET_KEY,
                                   region_name=config.REGION_NAME)
                s3 = session.resource("s3")
                bucket = s3.Bucket(config.BUCKET_NAME)
                
                self.download_latest_model(bucket)
            
            timestamps = os.listdir(self.index_file_path)
            if len(timestamps) == 0:
                return False

            timestamps = list(map(int, os.listdir(self.index_file_path)))
            latest_timestamp = max(timestamps)
            latest_timestamp = self.timestamp_converter(latest_timestamp)
            latest_index_path = os.path.join(self.index_file_path, f"{latest_timestamp}", SAVED_MODEL_FILE_NAME)
            return latest_index_path       
        
        except Exception as e:
            raise JobRecException(e,sys)
        

if __name__ == "__main__":
    ob1 = LoadIndex()
    print(ob1.get_best_index_path())
    