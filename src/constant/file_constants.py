
#JOBS_DATA_FILE_PATH = "data/jobs_data.xlsx"
ARTIFACT_DIR = "artifacts"
PRODUCTION_DIR = "production"
PIPELINE_NAME = "job_recommender"


#MODEL CONSTANTS
MODEL_NAME = "msmarco-distilbert-base-dot-prod-v3"
MODEL_INDEX_SIZE = 768
MODEL_LOCATION_DIR = "downloaded_model"
SAVED_MODEL_DIR = "production"
SAVED_MODEL_FILE_NAME = "production_embed_index.index"
TOP_N_RESULTS = 8


#APP CONSTANTS
APP_HOST = "0.0.0.0"
APP_PORT = 5000

#DATA INGESTION COMPONENT CONSTANTS
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FILE_NAME = "jobs_data.parquet"


#DATA EMBEDDING AND INDEXING COMPONENT CONSTANTS
EMBED_INDEXING_DIR_NAME = "embed_indexing"
EMBED_INDEXING_FILE_NAME = "embedd_faiss.index"


#CLOUD CONSTANTS
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_REGION_NAME = "AWS_REGION"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
MODEL_BUCKET_NAME =   "31137bsb4018-job-rec-s3" #"job-recommender-sys-model-bucket-bsb6775"
DATA_BUCKET_NAME = "job-recommender-sys-model-data-bucket-bsb6775"

MONGODB_URL_KEY = "MONGO_DB_URL"
MONGO_DATABASE_NAME = "jobs_db"
MONGO_COLLECTION_NAME = "jobs_collection"

DATA_VERSION_FOLER_NAME = "data-v1.0"
DATA_FILE_NAME = "jobs_data.xlsx"

