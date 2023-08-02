import os,sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import JobRecException
from src.entity.config_entity import EmbedIndexingConfig
from src.model.load_model import LoadModel
from src.entity.artifact_entity import DataIngestionArtifact,EmbedIndexingArtifact
import faiss
from src.constant.file_constants import MODEL_INDEX_SIZE

class EmbedIndex:
    def __init__(self, embed_index_config: EmbedIndexingConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.embed_index_config = embed_index_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_loader = LoadModel()
        except Exception as e:
            raise JobRecException(e,sys)
    
    def store_embeddings(self,jobsdf):
        '''
        Take the dataframe, gets the requried attributes(key skills, job names), 
        loads the pretrianed SBERT model,create the embeddings, 
        converts the embeddings to numpy arrays and returns them
        '''
        try:
            logging.info("Embedding and Indexing: Loading Pretrianed SBERT Model...")
            model = self.model_loader.load_model()
            encoding_data = jobsdf.Key_Skills + jobsdf.Job_Name

            logging.info("Embedding and Indexing: Creating Embeddings-Model Encoding...")
            encoded_data = model.encode(encoding_data.tolist())
            encoded_data = np.asarray(encoded_data.astype('float32'))

            logging.info("Embedding and Indexing: Embedding Creation Complete...")
            return encoded_data
        
        except Exception as e:
            raise JobRecException(e,sys)

    def faiss_indexing(self,encoded_data,jobsdf):
        '''
        Takes the embeddings and original data to create a FAISS indexing for similarity search
        '''
        try:
            logging.info("Embedding and Indexing: Creating FAISS indexing...")
            index = faiss.IndexIDMap(faiss.IndexFlatIP(MODEL_INDEX_SIZE))
            index.add_with_ids(encoded_data, np.array(range(0, len(jobsdf))))
            
            logging.info("Embedding and Indexing: Creating directories and Saving the index file...")
            indexing_file_save_location = self.embed_index_config.index_file_name
            dir_name = os.path.dirname(indexing_file_save_location)
            os.makedirs(dir_name, exist_ok=True)
            with open(indexing_file_save_location, 'w'):
                pass
            #os.path.basename(indexing_file_save_location)
            logging.info("Embedding and Indexing: Index File Saved")
            faiss.write_index(index, indexing_file_save_location)

        except Exception as e:
            raise JobRecException(e,sys)

    def initiate_data_embed_indexing(self) -> EmbedIndexingArtifact:
        '''
        Strating Embedding and Indexing component
        '''
        try:
            logging.info("Entered initiate_data_embed_indexing method of EmbedIndex class")

            logging.info("Embedding and Indexing: Load data ingestion artifact...")
            jobsdf = pd.read_parquet(self.data_ingestion_artifact.jobs_file_path)

            logging.info("Embedding and Indexing: Starting Embedding and Indexing...")
            encoded_data = self.store_embeddings(jobsdf)
            self.faiss_indexing(encoded_data,jobsdf)

            logging.info("EmbedIndex: Storing Artifacts...")
            data_embed_index_artifact = EmbedIndexingArtifact(
                faiss_index_file_path = self.embed_index_config.index_file_name,
            )
            logging.info(f"EmbedIndex artifact: {data_embed_index_artifact}")
            return data_embed_index_artifact
        
        except Exception as e:
            raise JobRecException(e, sys)
