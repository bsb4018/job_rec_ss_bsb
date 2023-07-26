import os,sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import JobRecException
import faiss
from src.configurations.mongo_setup import MongoDBClient
from src.model.load_model import LoadModel
from src.model.load_index import LoadIndex
from src.constant.file_constants import TOP_N_RESULTS
import time

class ModelRecommender:
    def __init__(self,):
        try:
            self.model_loader = LoadModel()
            self.index_loader = LoadIndex()
            self.mongo_client = MongoDBClient()
            self.collection = self.mongo_client.dbcollection
        except Exception as e:
            raise JobRecException(e,sys)
        
    def fetch_job_results(self, index):
        try:
            meta_dict = {}
            job_name = ""
            company_name = ""
            required_skills = ""
            result = self.collection.find_one({'job_id': index}, {'job_name': 1,'company_name': 1, 'key_skills': 1})
            if result:
                job_name = result['job_name']
                company_name = result['company_name']
                required_skills = result['key_skills']
            else:
                job_name = "None"
                company_name = "None"
                required_skills = "None"

            meta_dict['Job_Name'] = job_name
            meta_dict['Company_Name'] = company_name
            meta_dict['Required_Skills'] = required_skills
            return meta_dict
        
        except Exception as e:
            raise JobRecException(e,sys)
        
    '''
    def fetch_job_info(self, dataframe_idx, jobsdf):
        try:
            
            info = jobsdf.iloc[dataframe_idx]
            meta_dict = {}
            meta_dict['Job_Name'] = info['Job_Name']
            meta_dict['Company_Name'] = info['Company_Name']
            meta_dict['Required_Skills'] = info['Key_Skills']
            return meta_dict
        
        except Exception as e:
            raise JobRecException(e,sys)
    '''

    def job_search(self, query, topk, index, model):
        try:
            t = time.time()
                       
            query_vector = model.encode([query])
            topk = index.search(query_vector, topk)

            print('>>>> Results in Total Time: {}'.format(time.time()-t))
   
            topk_ids = topk[1].tolist()[0]
            topk_ids = list(np.unique(topk_ids))
            results = [self.fetch_job_results(int(idx.item())) for idx in topk_ids]

            return results
        
        except Exception as e:
            raise JobRecException(e,sys)
        
    def recommend(self, query):
        try:
            topk = TOP_N_RESULTS

            #load model path from model location
            model = self.model_loader.load_model()
            
            #load index file path from production
            jobs_index_path = self.index_loader.get_best_index_path()
            index = faiss.read_index(jobs_index_path)

            #pass to model recommender
            results = self.job_search(query, topk, index, model)
            return results
        
        except Exception as e:
            raise JobRecException(e,sys)
        

if __name__ == "__main__":
    ob1 = ModelRecommender()
    print(ob1.recommend("data science analytics python"))