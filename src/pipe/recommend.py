import os,sys
import pandas as pd
import numpy as np
from src.exception import JobRecException
from src.logger import logging
from src.components.model_recommender import ModelRecommender

import warnings
warnings.filterwarnings("ignore")


class RecommenderPipeline:
    def __init__(self,):
        try:
            self.model_recommender = ModelRecommender()
        except Exception as e:
            raise JobRecException(e,sys) 

        
    def get_recommendations(self,query):
        try:
            logging.info("Entered initiate_model_trainer method of ModelRecommender class")          

            recommended_list = self.model_recommender.recommend(query)
            return recommended_list

        except Exception as e:
            raise JobRecException(e,sys)
        

if __name__ == "__main__":
    ob1 = RecommenderPipeline()
    print(ob1.get_recommendations("data science analytics python"))