import os
import glob
import pandas as pd
import streamlit as st
from src.paragraph_analyzer import ParagraphAnalyzer
from streamlit_extras.switch_page_button import switch_page
from src.utils import styled_print, create_dir, fetch_session_state, add_to_session_state

# Set the title and instructions for the page
styled_print("Initiating Data Analyzer", header=True)

st.set_page_config(
    page_title="Data Analyzer",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/viralbthakar/',
        'Report a bug': "https://github.com/viralbthakar/fire-and-blood-qa/issues/new/choose",
        'About': "This is an *extremely* cool app!"
    }
)

out_dir = fetch_session_state(st.session_state, "out_dir")
analysis_data_dir = create_dir(out_dir, "analysis-images")
clean_data_dir = fetch_session_state(st.session_state, "clean_data_dir")
st.session_state = add_to_session_state(
    st.session_state, "analysis_data_dir", analysis_data_dir)

st.title("Data Analysis Tool")
st.write("Tool to perform data analysis on clean data.")

csv_files = []
for root, dirs, files in os.walk(clean_data_dir):
    for file in files:
        if (file.endswith(".csv")):
            csv_files.append(os.path.join(root, file))
selected_files = st.selectbox("Select Files", csv_files)
selected_files = [selected_files]

debug_data_analysis = st.button("Debug Analysis!")
all_data_analysis = st.button("Analysis All!")

if debug_data_analysis:
    for i, file in enumerate(selected_files):
        data_dict = pd.read_csv(file)
        st.subheader(f"Raw Data From {file}")
        st.dataframe(data_dict)
        analyzer = ParagraphAnalyzer(
            data_dict, 'cleaned_paragraphs', analysis_data_dir)

        with st.spinner('Wait for it...'):
            t1, t2, t3, t4, t5, t6 = st.tabs(
                [
                    "Char Histogram",
                    "Word Histogram",
                    "Average Word Length per Paragraph",
                    "Top 10 Non Stop Words",
                    "Top 10 Bigrams",
                    "Top 10 Trigrams"
                ]
            )
            fig = analyzer.characters_per_paragraph_histogram(
                figsize=(16, 16), dpi=300, save_flag=False)
            t1.pyplot(fig)

            fig = analyzer.words_per_paragraph_histogram(
                figsize=(16, 16), dpi=300, save_flag=False)
            t2.pyplot(fig)

            fig = analyzer.avg_word_len_per_paragraph_histogram(
                figsize=(16, 16), dpi=300, save_flag=False)
            t3.pyplot(fig)

            non_stop_words_corpus = analyzer.get_non_stop_words_corpus(
                language='english')
            top_k_non_stop_words = analyzer.get_top_k_non_stop_words(
                non_stop_words_corpus, top_k=10)
            fig = analyzer.plot_top_k_non_stop_words(
                top_k_non_stop_words, figsize=(16, 16), dpi=300, save_flag=False)
            t4.pyplot(fig)

            bigrams = analyzer.get_ngrams(n=2, return_list=True)
            top_k_bigrams = analyzer.get_top_k_ngrams(
                n=2, top_k=10)
            fig = analyzer.plot_top_k_ngrams(
                top_k_bigrams, title=f"Top {10} Bigrams", figsize=(16, 16), dpi=300, save_flag=False)
            t5.pyplot(fig)

            trigrams = analyzer.get_ngrams(n=3, return_list=True)
            top_k_trigrams = analyzer.get_top_k_ngrams(
                n=3, top_k=10)
            fig = analyzer.plot_top_k_ngrams(
                top_k_trigrams, title=f"Top {10} Trigrams", figsize=(16, 16), dpi=300, save_flag=False)
            t6.pyplot(fig)


if all_data_analysis:
    selected_files = [f for f in csv_files]
    with st.spinner('Analyzing all data ...'):
        for i, file in enumerate(selected_files):
            st.subheader(f"{os.path.basename(file)}")
            data_dict = pd.read_csv(file)
            st.subheader(f"Raw Data From {file}")
            st.dataframe(data_dict)
            analyzer = ParagraphAnalyzer(
                data_dict, 'cleaned_paragraphs', analysis_data_dir)
            with st.spinner('Wait for it...'):
                t1, t2, t3, t4, t5, t6 = st.tabs(
                    [
                        "Char Histogram",
                        "Word Histogram",
                        "Average Word Length per Paragraph",
                        "Top 10 Non Stop Words",
                        "Top 10 Bigrams",
                        "Top 10 Trigrams"
                    ]
                )
                fig = analyzer.characters_per_paragraph_histogram(
                    figsize=(16, 16), dpi=300, save_flag=False)
                t1.pyplot(fig)

                fig = analyzer.words_per_paragraph_histogram(
                    figsize=(16, 16), dpi=300, save_flag=False)
                t2.pyplot(fig)

                fig = analyzer.avg_word_len_per_paragraph_histogram(
                    figsize=(16, 16), dpi=300, save_flag=False)
                t3.pyplot(fig)

                non_stop_words_corpus = analyzer.get_non_stop_words_corpus(
                    language='english')
                top_k_non_stop_words = analyzer.get_top_k_non_stop_words(
                    non_stop_words_corpus, top_k=10)
                fig = analyzer.plot_top_k_non_stop_words(
                    top_k_non_stop_words, figsize=(16, 16), dpi=300, save_flag=False)
                t4.pyplot(fig)

                bigrams = analyzer.get_ngrams(n=2, return_list=True)
                top_k_bigrams = analyzer.get_top_k_ngrams(
                    n=2, top_k=10)
                fig = analyzer.plot_top_k_ngrams(
                    top_k_bigrams, title=f"Top {10} Bigrams", figsize=(16, 16), dpi=300, save_flag=False)
                t5.pyplot(fig)

                trigrams = analyzer.get_ngrams(n=3, return_list=True)
                top_k_trigrams = analyzer.get_top_k_ngrams(
                    n=3, top_k=10)
                fig = analyzer.plot_top_k_ngrams(
                    top_k_trigrams, title=f"Top {10} Trigrams", figsize=(16, 16), dpi=300, save_flag=False)
                t6.pyplot(fig)
