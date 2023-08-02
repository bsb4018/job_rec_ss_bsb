import os,sys
import pandas as pd
from src.logger import logging
from src.exception import JobRecException
from src.entity.config_entity import DataIngestionConfig
from src.constant.file_constants import DATA_VERSION_FOLER_NAME,DATA_FILE_NAME
from src.configurations.mongo_setup import MongoDBClient
from src.entity.artifact_entity import DataIngestionArtifact
from src.configurations.aws_configure import StorageConnection
class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.mongo_client = MongoDBClient()
            self.collection = self.mongo_client.dbcollection
            self.aws_connection = StorageConnection()

        except Exception as e:
            raise JobRecException(e,sys)

    def download_data_from_s3(self):
        '''
        Downloads data from AWS S3
        '''
        try:
            logging.info("DATA INGESTION: Downloading Data from Cloud...")
            self.aws_connection.download_data_from_s3()
            
            logging.info("DATA INGESTION: Downloading Data from Cloud Complete")
        except Exception as e:
            raise JobRecException(e,sys)
        
    def load_data(self):
        '''
        Loads the downloaded data, removes missing columns and rows, adds indexes and saves the data into parquet file
        '''
        try:
            logging.info("DATA INGESTION: Loading Data...")
            data_filepath = os.path.join(DATA_VERSION_FOLER_NAME,DATA_FILE_NAME)
            jobsdf = pd.read_excel(data_filepath)

            logging.info("DATA INGESTION: Dropping Missing Columns and Rows...")
            jobsdf.dropna(inplace=True)
            
            logging.info("DATA INGESTION: Creating job indexes...")
            job_ids = [i for i in range(0,len(jobsdf))]
            jobsdf["job_id"] = job_ids

            save_users_file = self.data_ingestion_config.jobs_file_name
            dir_path = os.path.dirname(save_users_file)

            logging.info("DATA INGESTION: Saving the ingested data in aprquet...")
            os.makedirs(dir_path, exist_ok=True)
            jobsdf.to_parquet(save_users_file, engine='fastparquet', index=False)

            logging.info("DATA INGESTION: Data store done...")

            return jobsdf
        
        except Exception as e:
            raise JobRecException(e,sys)
        
    def store_data_mongodb(self,df):
        '''
        Takes the loaded dataframe and stores the data in MongoDB for use in prediction/recommendation
        '''
        try:
            logging.info("Storing data in MongoDB")
            for index,row in df.iterrows():
                job_id = row["job_id"]
                job_name = row["Job_Name"]
                company_name = row["Company_Name"]
                key_skills = row["Key_Skills"]             
                self.collection.insert_one({"job_id": job_id, "job_name": job_name, "company_name": company_name, "key_skills": key_skills})
            logging.info("Successfully stored data in MongoDB")

        except Exception as e:
            raise JobRecException(e,sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        '''
        Starts the data ingestion component
        '''
        try:
            logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
            self.download_data_from_s3()
            df = self.load_data()
            self.store_data_mongodb(df)
            logging.info("DATA INGESTION: Storing Artifacts...")
            data_ingestion_artifact = DataIngestionArtifact(
                jobs_file_path=self.data_ingestion_config.jobs_file_name,
            )
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise JobRecException(e, sys)