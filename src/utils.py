import os
import re
import docx
import time
import json
import pysrt
import requests
import trafilatura
import streamlit as st
from collections import defaultdict
from wikitextparser import parse, remove_markup


def styled_print(text, header=False, sleep_time=0):
    """Custom Print Function"""
    class style:
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

    if header:
        print(f'{style.BOLD}› {style.UNDERLINE}{text}{style.END}')
    else:
        print(f'    › {text}')
    time.sleep(sleep_time)


def create_dir(root_dir, new_dir, header=True):
    styled_print(
        f'creating directory ... {os.path.join(root_dir, new_dir)}', header=header)
    os.makedirs(os.path.join(root_dir, new_dir), exist_ok=True)
    return os.path.join(root_dir, new_dir)


def extract_paragraphs(file_path, min_char_count=1):
    styled_print(f"Extracting Paragraphs from {file_path}", header=False)
    paragraphs = {}
    document = docx.Document(file_path)
    for i in range(2, len(document.paragraphs)):
        if min_char_count is not None:
            if len(document.paragraphs[i].text) >= min_char_count:
                paragraphs[i] = document.paragraphs[i].text
        else:
            paragraphs[i] = document.paragraphs[i].text
    return paragraphs


def extract_text_from_srt(file_path):
    subtitle_dict = defaultdict(list)
    subtitles = pysrt.open(file_path)
    for sub in subtitles:
        subtitle_dict["start_hours"].append(sub.start.hours)
        subtitle_dict["start_minutes"].append(sub.start.minutes)
        subtitle_dict["start_seconds"].append(sub.start.seconds)
        subtitle_dict["end_hours"].append(sub.end.hours)
        subtitle_dict["end_minutes"].append(sub.end.minutes)
        subtitle_dict["end_seconds"].append(sub.end.seconds)
        subtitle_dict["text"].append(sub.text)
    return subtitle_dict


def extract_text_from_url(url):
    # Download HTML Code
    downloaded_url = trafilatura.fetch_url(url)

    # Try Extracting Text data as
    try:
        extract = trafilatura.extract(
            downloaded_url,
            output_format='json',
            favor_precisions=True,
            favour_recall=True,
            include_comments=False,
            include_tables=False,
            date_extraction_params={
                'extensive_search': True, 'original_date': True}
        )
    except AttributeError:
        extract = trafilatura.extract(
            downloaded_url,
            output_format='json',
            date_extraction_params={
                'extensive_search': True, 'original_date': True}
        )
    if extract:
        json_output = json.loads(extract)
        return json_output['text']
    else:
        return "None"


def extract_fandom_wikis(url, titles):
    def extract_sections(wikitext):
        parsed_wikitext = parse(wikitext)
        sections = {}
        for section in parsed_wikitext.sections:
            if section.title and section.title.strip():
                title = str(section.title.strip())
                title = remove_file_links(title)
                title = remove_newlines(title)
                title = remove_backslash(title)
                title = remove_markup(title)
            else:
                title = "No Title"
            if section.contents and section.contents.strip():
                contents = str(section.contents.strip())
                contents = remove_file_links(contents)
                contents = remove_newlines(contents)
                contents = remove_backslash(contents)
                contents = remove_markup(contents)
            else:
                contents = ""
            sections[title] = contents
        return sections

    data_dict = defaultdict(dict)
    response = requests.get(url + "?action=raw")
    wikitext_content = response.text
    parsed_wikitext = parse(wikitext_content)
    for section in parsed_wikitext.sections:
        if section.title in titles:
            data_dict[section.title] = extract_sections(section.contents)

    sample_dict = defaultdict(list)
    for key, value in data_dict.items():
        for k, v in value.items():
            if not v:
                continue
            sample_dict["header"].append(key)
            sample_dict["prompt"].append(k)
            sample_dict["paragraphs"].append(v)
    return sample_dict


def remove_file_links(text):
    pattern = r'\[\[File:(.*?)\]\]'
    return re.sub(pattern, '', text)


def remove_newlines(text):
    return re.sub(r"\n", "", text)


def remove_backslash(text):
    return re.sub(r"\\'", "'", text)


def save_uploadedfile(uploadedfile, path="tempDir"):
    with open(os.path.join(path, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"Saved File:{uploadedfile.name} to {path}")
