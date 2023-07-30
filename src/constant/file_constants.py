

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
SAVED_MODEL_DIR = "production"
SAVED_MODEL_FILE_NAME = "production_embed_index.index"
TOP_N_RESULTS = 6

DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FILE_NAME = "jobs_data.parquet"

EMBED_INDEXING_DIR_NAME = "embed_indexing"
EMBED_INDEXING_FILE_NAME = "embedd_faiss.index"

AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_REGION_NAME = "AWS_REGION"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
MODEL_BUCKET_NAME = "job-recommender-sys-model-bucket-bsb6775"
DATA_BUCKET_NAME = "job-recommender-sys-model-data-bucket-bsb6775"

DATA_VERSION_FOLER_NAME = "data-v1.0"
DATA_FILE_NAME = "jobs_data.xlsx"