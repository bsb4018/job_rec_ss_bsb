from src.pipe.store_and_generate import StoreGeneratePipeline
from fastapi import FastAPI, File, UploadFile,Body
from starlette.responses import RedirectResponse
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from src.pipe.recommend import RecommenderPipeline
from src.constant.file_constants import APP_HOST, APP_PORT


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


class Job_Rec_Query(BaseModel):
    user_query: str
    


@app.get("/train")
async def train_routed():
    try:

        store_gen_pipeline = StoreGeneratePipeline()
        
        if store_gen_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        store_gen_pipeline.run_pipeline()
        return Response("Training successful !!")
    
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/recommend_jobs")
async def predict_route(item: Job_Rec_Query):
    try:
       
        item_dict = dict(item)
        prediction_pipeline = RecommenderPipeline()
        results = prediction_pipeline.get_recommendations(item_dict["user_query"])

        if not results:
            return Response("Model is not available")
        return { "Recommended Jobs": results}
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")
   

#if __name__ == "__main__":
    #app_run(app, host=APP_HOST, port=APP_PORT)

if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)



















'''
from memory_profiler import profile
from src.pipe.store_and_generate import StoreGeneratePipeline
import logging
import warnings
warnings.filterwarnings("ignore")
'''



'''
# create logger
logger = logging.getLogger('memory_profile_log')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler("memory_profile.log")
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)

from memory_profiler import LogFile
import sys
sys.stdout = LogFile('memory_profile_log', reportIncrementFlag=False)
'''
'''
#@profile
def main():
    try:
        store_gen_pipeline = StoreGeneratePipeline()
        store_gen_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)

if __name__ == "__main__":
    main()
'''