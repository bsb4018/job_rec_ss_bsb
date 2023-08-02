
from src.exception import JobRecException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact,EmbedIndexingArtifact
from src.entity.config_entity import ModelPusherConfig
import os,sys
import shutil

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                       data_embed_index_artifact: EmbedIndexingArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.data_embed_index_artifact = data_embed_index_artifact
        except Exception as e:
            raise JobRecException(e,sys) from e

    def initiate_model_pusher(self,) -> ModelPusherArtifact:
        '''
        Starts the model pusher component
        '''
        try:
            logging.info("Entered initiate_model_pusher method of ModelPusher class")

            logging.info("Model Pusher: Load embed index artifact...")

            faiss_index_file_path = self.data_embed_index_artifact.faiss_index_file_path
            
            logging.info("Model Pusher: Creating a production path of it does't exist...")
            #Pushing the trained model in a the saved path for production
            model_file_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=faiss_index_file_path, dst=model_file_path)
            
            logging.info("ModelPusher: Storing Artifacts...")
            #Prepare artifact
            model_pusher_artifact = ModelPusherArtifact(
                saved_model_embed_index_path = self.data_embed_index_artifact.faiss_index_file_path)
            
            logging.info(f"ModelPusher artifact: {model_pusher_artifact}")
            
            return model_pusher_artifact

        except Exception as e:
            raise JobRecException(e,sys) from e