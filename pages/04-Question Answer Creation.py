import os
import glob
import pandas as pd
import streamlit as st
from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
from streamlit_extras.switch_page_button import switch_page
from src.utils import styled_print, create_dir, fetch_session_state, add_to_session_state, extract_NER, create_qa_pairs_from_NER

# Set the title and instructions for the page
styled_print("Initiating Question Answer Creator", header=True)

st.set_page_config(
    page_title="QA Creator",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/viralbthakar/',
        'Report a bug': "https://github.com/viralbthakar/fire-and-blood-qa/issues/new/choose",
        'About': "This is an *extremely* cool app!"
    }
)

st.title("Question Answer Creation Tool")
st.write("Tool to perform create question, answer and context data for model training.")

question_answer_dir = create_dir("./", "data/qa-data")
out_dir = fetch_session_state(st.session_state, "out_dir")
clean_data_dir = fetch_session_state(st.session_state, "clean_data_dir")
st.session_state = add_to_session_state(
    st.session_state, "question_answer_dir", question_answer_dir)

genre = st.radio(
    "Select Method to Use",
    ('NER', 'Other'))

csv_files = []
for root, dirs, files in os.walk(clean_data_dir):
    for file in files:
        if (file.endswith(".csv")):
            csv_files.append(os.path.join(root, file))
selected_files = st.selectbox("Select Files", csv_files)
selected_files = [selected_files]

debug_qa_extraction = st.button("Debug QA Creation!")
all_qa_extraction = st.button("QA Create All!")

if debug_qa_extraction:
    if genre == 'NER':
        qa_csv_path = create_dir(question_answer_dir, genre)
        for i, file in enumerate(selected_files):
            data_df = pd.read_csv(file)
            question_answers = defaultdict(list)
            st.subheader(f"Raw Data From {file}")
            st.dataframe(data_df)
            if os.path.isfile(os.path.join(qa_csv_path, os.path.basename(file))):
                st.warning(
                    "Question Answer file already exists. Skipping extraction.")
                qa_df = pd.read_csv(os.path.join(
                    qa_csv_path, os.path.basename(file)))
                st.dataframe(qa_df)
            else:
                with st.spinner('Generating Question Answers ...'):
                    for index, row in data_df.iterrows():
                        paragraph = row['cleaned_paragraphs']
                        sentences = sent_tokenize(paragraph)
                        for sentence in sentences:
                            doc = extract_NER(sentence, model="en_core_web_lg")
                            qas = create_qa_pairs_from_NER(doc)
                            for que, ans in qas:
                                question_answers["context"].append(sentence)
                                question_answers["questions"].append(que)
                                question_answers["answers"].append(ans)
                    qa_df = pd.DataFrame.from_dict(question_answers)
                    qa_df.to_csv(os.path.join(qa_csv_path, os.path.basename(
                        file)), index=False, header=True)
                    st.dataframe(qa_df)
                    st.success(
                        f"Saved File: {os.path.join(qa_csv_path, os.path.basename(file))}")

if all_qa_extraction:
    selected_files = [f for f in csv_files]
    if genre == 'NER':
        qa_csv_path = create_dir(question_answer_dir, genre)
        with st.spinner('Creating QA Pairs ...'):
            for i, file in enumerate(selected_files):
                data_df = pd.read_csv(file)
                question_answers = defaultdict(list)
                st.subheader(f"Raw Data From {file}")
                st.dataframe(data_df)

                if os.path.isfile(os.path.join(qa_csv_path, os.path.basename(file))):
                    st.warning(
                        "Question Answer file already exists. Skipping extraction.")
                    qa_df = pd.read_csv(os.path.join(
                        qa_csv_path, os.path.basename(file)))
                    st.dataframe(qa_df)
                else:
                    with st.spinner('Generating Question Answers ...'):
                        for index, row in data_df.iterrows():
                            paragraph = row['cleaned_paragraphs']
                            sentences = sent_tokenize(paragraph)
                            for sentence in sentences:
                                doc = extract_NER(
                                    sentence, model="en_core_web_lg")
                                qas = create_qa_pairs_from_NER(doc)
                                for que, ans in qas:
                                    question_answers["context"].append(
                                        sentence)
                                    question_answers["questions"].append(que)
                                    question_answers["answers"].append(ans)
                        qa_df = pd.DataFrame.from_dict(question_answers)
                        qa_df.to_csv(os.path.join(qa_csv_path, os.path.basename(
                            file)), index=False, header=True)
                        st.dataframe(qa_df)
                        st.success(
                            f"Saved File: {os.path.join(qa_csv_path, os.path.basename(file))}")

st.sidebar.success("Question Answer Creation is Done!")

qa_model_page = st.button("QA Model!")
if qa_model_page:
    switch_page("Question Answer Model")
    print(st.session_state)
