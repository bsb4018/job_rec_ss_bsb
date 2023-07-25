import os,sys
from src.logger import logging
from src.exception import JobRecException
from src.constant.file_constants import MODEL_NAME,MODEL_LOCATION_DIR
from sentence_transformers import SentenceTransformer

class LoadModel:
    def __init__(self,):
        try:
            self.model_location_path = os.path.join("src", "model", MODEL_LOCATION_DIR)
        except Exception as e:
            raise JobRecException(e,sys)
        
    def download_model(self):
        try:
            model = SentenceTransformer(MODEL_NAME)
            model_location_path = self.model_location_path
            os.makedirs(model_location_path, exist_ok=True)
            model.save(model_location_path)
            
            return model
        
        except Exception as e:
            raise JobRecException(e,sys)
    
    def load_model(self):
        try:
            if not os.path.exists(self.model_location_path):
                model = self.download_model()
            else:
                model = SentenceTransformer(self.model_location_path)

            return model
        
        except Exception as e:
            raise JobRecException(e,sys)
    

if __name__ == "__main__":
    ob1 = LoadModel()
    model = ob1.load_model()
    print("Yes!Running")