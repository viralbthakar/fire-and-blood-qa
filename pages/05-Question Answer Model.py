import os
import glob
import pandas as pd
import streamlit as st
import tensorflow as tf
from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
from streamlit_extras.switch_page_button import switch_page
from src.utils import styled_print, create_dir, fetch_session_state, add_to_session_state, extract_NER, create_qa_pairs_from_NER
from transformers import pipeline
from src import model_trainer
# Set the title and instructions for the page
styled_print("Initiating Question Answer Model", header=True)

st.set_page_config(
    page_title="QA Model",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/viralbthakar/',
        'Report a bug': "https://github.com/viralbthakar/fire-and-blood-qa/issues/new/choose",
        'About': "This is an *extremely* cool app!"
    }
)

st.title("Question Answer Model Creation Tool")
st.write("Tool to create question, answer model")
model_dir = create_dir("./", "data/qa-model")
qa_data_dir = fetch_session_state(st.session_state, "question_answer_dir")

genre = st.radio(
    "Select Method to Use",
    ('Pretrained BERT', 'Train Bert'))

if genre == "Pretrained BERT":
    question_txt = st.text_area('Question')
    context_txt = st.text_area('Context')
    qa_button = st.button("Send A Raven!")
    if qa_button:
        question_answerer = pipeline(
            "question-answering", model="distilbert-base-cased-distilled-squad")
        pred = question_answerer(question=question_txt, context=context_txt)
        st.write(f"{pred['answer']} with score : {pred['score']}")

elif genre == "Train Bert":
    csv_files = []
    for root, dirs, files in os.walk(qa_data_dir):
        for file in files:
            if (file.endswith(".csv")):
                csv_files.append(os.path.join(root, file))
    selected_files = st.selectbox("Select Files", csv_files)
    selected_files = [selected_files]

    debug_qa_train = st.button("Debug QA Training!")
    all_qa_train = st.button("QA Train All!")

    if debug_qa_train:
        for i, file in enumerate(selected_files):
            st.subheader(f"Training Model with {file}")
            data_df = pd.read_csv(file)
            with st.spinner('Training Question Answers ...'):
                model = model_trainer.main_trainer(data_df, model_dir)
                st.session_state = add_to_session_state(
                    st.session_state, "model", model)

    question_txt = st.text_area('Question')
    context_txt = st.text_area('Context')
    qa_button = st.button("Send A Raven!")

    if qa_button:
        model = fetch_session_state(st.session_state, "model")
        outpu = model_trainer.inference(model, question_txt, context_txt)
        st.write(outpu)
