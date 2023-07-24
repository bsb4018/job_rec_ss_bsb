import os,sys
from memory_profiler import profile
from src.exception import JobRecException
from src.logger import logging
from src.entity.config_entity import StoreGenearatePipelineConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig
from src.components.data_ingestion import DataIngestion

class StoreGeneratePipeline:
    '''
    Defines the Data Storing Pipeline
    '''
    def __init__(self,):
        try:
            self.store_gen_pipeline_config = StoreGenearatePipelineConfig()
        except Exception as e:
            raise JobRecException(e,sys)
        
    #@profile
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            
            logging.info(
              "Entered the start_data_ingestion method of StoreGeneratePipeline class"
            )
            self.data_ingestion_config = DataIngestionConfig(store_gen_pipeline_config=self.store_gen_pipeline_config)
            
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            logging.info(
                "Exited the start_data_ingestion method of StoreGeneratePipelinee class"
            )
            
            return data_ingestion_artifact
    
        except Exception as e:
            raise JobRecException(e, sys)

    #@profile    
    def run_pipeline(self):
        try:
            logging.info("Starting the Data Storing and Embedding Genearation Pipeline")
            StoreGenearatePipelineConfig.is_pipeline_running=True
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            

            logging.info("Data Ingested, Processed and Stored into MongoDB")
        except Exception as e:
            raise JobRecException(e,sys)
        

if __name__ == "__main__":
    #Call the Pipeline
    data_store_pipeline  =  StoreGeneratePipeline()
    data_store_pipeline.run_store_and_generate_pipeline()