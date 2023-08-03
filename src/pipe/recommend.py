import os,sys
import pandas as pd
import numpy as np
from src.exception import JobRecException
from src.logger import logging
from src.components.model_recommender import ModelRecommender
import pprint
import warnings
warnings.filterwarnings("ignore")


class RecommenderPipeline:
    '''
    Defines the Model Prediction(Recommendation) Pipeline
    '''
    def __init__(self,):
        try:
            self.model_recommender = ModelRecommender()
        except Exception as e:
            raise JobRecException(e,sys) 

        
    def get_recommendations(self,query):
        '''
        Takes input a string query and gets the recommendations from recommendations component
        '''
        try:
            logging.info("Entered get_recommendations method of RecommenderPipeline class")

            logging.info("Calling the recommendation component to get the recommendations")        

            recommended_list = self.model_recommender.recommend(query)

            logging.info("Got Recommendations -> Displaying them to the end user")
            return recommended_list

        except Exception as e:
            raise JobRecException(e,sys)
        

if __name__ == "__main__":
    ob1 = RecommenderPipeline()
    pprint.pprint(ob1.get_recommendations("data analytics devops"))