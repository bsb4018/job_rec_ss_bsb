import numpy as np
import pandas as pd
import streamlit as st
from src.pipe.recommend import RecommenderPipeline
from src.pipe.store_and_generate import StoreGeneratePipeline
import pprint

st.title(" Job Recommendations  ")


train_button = st.button(label="Train Model", type="primary")

if train_button:
    # Run the train function and get the results
    store_gen_pipeline = StoreGeneratePipeline()
    
    if store_gen_pipeline.is_pipeline_running:
        st.write("Training pipeline is already running.")
        
    store_gen_pipeline.run_pipeline()
    st.write("Training successful !!")


# Get the search term from the user through a text input widget
search_term = st.text_input(
    label=":blue[Enter some of your Key Skills]",
    placeholder="enter key skills like data science, java, management, sales etc...",
)

# Get the search button trigger from the user
search_button = st.button(label="Get Recommendations", type="primary")

def is_valid_input(user_input):
    # Your validation logic here
    return isinstance(user_input, str) and len(user_input) > 0

def get_job_recommendations(key_skills_query, pprint=True):
    recommender = RecommenderPipeline()
    results = recommender.get_recommendations(key_skills_query)
    return results


# If the user has entered a search term
if is_valid_input(search_term):
    # And if they have clicked the search button
    if search_button:
        # Run the search function and get the results
        answer = get_job_recommendations(search_term, True)
        # Iterate through the results and display the recommendations
        #st.write(answer)
        for item in answer:
            st.write(item)
        
#else:
    #st.info("Please Enter Some Key Skills")