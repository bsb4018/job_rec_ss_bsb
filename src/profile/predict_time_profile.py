
from src.pipe.recommend import RecommenderPipeline
import logging
import warnings
warnings.filterwarnings("ignore")
import line_profiler
import atexit
lp_profile = line_profiler.LineProfiler()
atexit.register(lp_profile.print_stats)


def recommend_pipeline(key_skills_query):
    try:
        recommender = RecommenderPipeline()
        results = recommender.get_recommendations(key_skills_query)
        return results
    except Exception as e:
        print(e)
        logging.exception(e)


@lp_profile
def main():
    try:
        key_skills_query = "data science python sql"
        recommend_pipeline(key_skills_query)

    except Exception as e:
        print(e)
        logging.exception(e)


if __name__ == "__main__":
    main()
