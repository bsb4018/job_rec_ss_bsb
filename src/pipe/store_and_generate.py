import os,sys
from src.exception import JobRecException
from src.logger import logging
from src.constant.file_constants import MODEL_BUCKET_NAME,SAVED_MODEL_DIR
from src.entity.config_entity import StoreGenearatePipelineConfig
from src.entity.artifact_entity import DataIngestionArtifact,EmbedIndexingArtifact
from src.entity.config_entity import DataIngestionConfig,EmbedIndexingConfig,ModelPusherConfig
from src.components.data_ingestion import DataIngestion
from src.components.embed_index import EmbedIndex
from src.components.model_pusher import ModelPusher
from src.configurations.aws_s3_syncer import S3Sync


class StoreGeneratePipeline:
    '''
    Defines the Data Storing Embedding Indexing and Pushing to Production Pipeline
    '''
    is_pipeline_running=False
    def __init__(self,):
        try:
            self.store_gen_pipeline_config = StoreGenearatePipelineConfig()
            self.s3_sync = S3Sync()
        except Exception as e:
            raise JobRecException(e,sys)
        
    #@profile
    def start_data_ingestion(self) -> DataIngestionArtifact:
        '''
        Starts the data ingestion pipeline
        '''
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
        
    def start_data_embed_indexing(self,data_ingestion_artifact:DataIngestionArtifact) -> EmbedIndexingArtifact:
        '''
        Takes input the data ingestion artifact and Starts the data nembeddung and indexing pipeline
        '''
        try:
            
            logging.info(
              "Entered the start_data_embed_indexing method of StoreGeneratePipeline class"
            )
            self.data_embed_index_config = EmbedIndexingConfig(store_gen_pipeline_config=self.store_gen_pipeline_config)
            
            logging.info("Starting data embeding and indexing")
            data_embed_index = EmbedIndex(
            embed_index_config = self.data_embed_index_config, data_ingestion_artifact = data_ingestion_artifact
            )
            data_embed_index_artifact = data_embed_index.initiate_data_embed_indexing()
            logging.info(f"start_data_embed_indexing completed and artifact: {data_embed_index_artifact}")
            logging.info(
                "Exited the start_data_embed_indexing method of StoreGeneratePipeline class"
            )
            
            return data_embed_index_artifact
    
        except Exception as e:
            raise JobRecException(e, sys)
    
    def start_model_pusher(self,data_embed_index_artifact:EmbedIndexingArtifact):
        '''
        Takes input the data embedding and indexing artifact and Starts the model pusher pipeline
        '''
        try:
            logging.info("Entered the start_model_pusher method of StoreGeneratePipeline class")
            model_pusher_config = ModelPusherConfig(store_gen_pipeline_config=self.store_gen_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config, data_embed_index_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()

            logging.info("Performed the Model Pusher operation")
            logging.info(
                "Exited the start_model_pusher method of StoreGeneratePipeline class"
            )

            return model_pusher_artifact
        except  Exception as e:
            raise  JobRecException(e,sys)
    
    def sync_logs_dir_to_s3(self):
        '''
        Starts syncing the logs to AWS S3
        '''
        try:
            logging.info("Entered the sync_logs_dir_to_s3 method of StoreGeneratePipeline class")
            aws_bucket_url = f"s3://{MODEL_BUCKET_NAME}/logs"
            logs_dir = os.path.join("logs")
            self.s3_sync.sync_folder_to_s3(folder = logs_dir,aws_buket_url=aws_bucket_url)
            logging.info("Performed Syncing of logs to S3 bucket")

        except Exception as e:
            raise JobRecException(e,sys)

    def sync_artifact_dir_to_s3(self):
        '''
        Starts syncing the artifacts to AWS S3
        '''
        try:
            logging.info("Entered the sync_artifact_dir_to_s3 method of StoreGeneratePipeline class")
            aws_bucket_url = f"s3://{MODEL_BUCKET_NAME}/artifact/{self.store_gen_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.store_gen_pipeline_config.artifact_dir, aws_buket_url=aws_bucket_url)
            logging.info("Performed Syncing of artifact to S3 bucket")

        except Exception as e:
            raise JobRecException(e,sys)

    def sync_saved_model_dir_to_s3(self):
        '''
        Starts syncing the production index file to AWS S3
        '''
        try:
            logging.info("Entered the sync_saved_model_dir_to_s3 method of StoreGeneratePipeline class")
            aws_bucket_url = f"s3://{MODEL_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder=SAVED_MODEL_DIR, aws_buket_url=aws_bucket_url)
            logging.info("Performed Syncing of production models to S3 bucket")

        except Exception as e:
            raise JobRecException(e,sys)

 
    def run_pipeline(self):
        '''
        Starts the main model creation pipeline
        '''
        try:
            logging.info("Starting the Data Storing and Embedding Genearation Pipeline")
            StoreGenearatePipelineConfig.is_pipeline_running=True

            logging.info("Starting the Data Ingestion Pipeline")
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()

            logging.info("Starting the Data Embedding and Indexing Pipeline")
            data_embed_index_artifact: EmbedIndexingArtifact = self.start_data_embed_indexing(data_ingestion_artifact)
            
            logging.info("Starting the Model Pusher Pipeline")
            model_pusher_artifact = self.start_model_pusher(data_embed_index_artifact)
            StoreGenearatePipelineConfig.is_pipeline_running=False
            
            #self.sync_logs_dir_to_s3()
            logging.info("Starting the Syncing Pipelines")
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            logging.info("Data Ingested, Embedded, Indexed and Pushed to Production -> Done")

        except Exception as e:
            self.sync_artifact_dir_to_s3()
            StoreGenearatePipelineConfig.is_pipeline_running=False
            raise JobRecException(e,sys)
        

if __name__ == "__main__":
    #Call the Pipeline
    data_store_pipeline  =  StoreGeneratePipeline()
    data_store_pipeline.run_store_and_generate_pipeline()