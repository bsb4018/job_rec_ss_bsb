from datetime import datetime
import os
from src.constant.file_constants import *

class StoreGenearatePipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp

class DataIngestionConfig:
    def __init__(self,store_gen_pipeline_config:StoreGenearatePipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
                store_gen_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
        )
        self.jobs_file_name: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FILE_NAME
        )

class EmbedIndexingConfig:
    def __init__(self,store_gen_pipeline_config:StoreGenearatePipelineConfig):
        self.embed_index_dir: str = os.path.join(
                store_gen_pipeline_config.artifact_dir, EMBED_INDEXING_DIR_NAME
        )
        self.index_file_name: str = os.path.join(
            self.embed_index_dir, EMBED_INDEXING_FILE_NAME
        )
