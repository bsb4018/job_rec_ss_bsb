from src.pipe.store_and_generate import StoreGeneratePipeline
import logging
import warnings
warnings.filterwarnings("ignore")

def main():
    try:
        store_gen_pipeline = StoreGeneratePipeline()
        store_gen_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)

if __name__ == "__main__":
    main()
