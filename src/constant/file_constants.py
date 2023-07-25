import sys,os
import from_root

JOBS_DATA_FILE_PATH = "data/jobs_data.xlsx"
MONGODB_URL_KEY = "MONGO_DB_URL"
MONGO_DATABASE_NAME = "jobs_db"
MONGO_COLLECTION_NAME = "jobs_collection"
ARTIFACT_DIR = "artifacts"
PRODUCTION_DIR = "production"
PIPELINE_NAME = "job_recommender"
MODEL_NAME = "msmarco-distilbert-base-dot-prod-v3"
MODEL_INDEX_SIZE = 768
MODEL_LOCATION_DIR = "downloaded_model"


DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FILE_NAME = "jobs_data.parquet"

EMBED_INDEXING_DIR_NAME = "embed_indexing"
EMBED_INDEXING_FILE_NAME = "embedd_faiss.index"