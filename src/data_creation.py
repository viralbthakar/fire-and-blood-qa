import os
import nltk
import json
import argparse
import pandas as pd
from utils import styled_print, create_dir, extract_paragraphs, extract_text_from_srt, extract_text_from_url, extract_fandom_wikis

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Creation')
    parser.add_argument('--book-docx-path', type=str,
                        default="../data/raw-data/fire-and-blood.docx",
                        help="Path to DOCX file for the book.")
    parser.add_argument('--config-file', type=str,
                        default="../data/config/data-extraction.json", help="Path to JSON file")
    parser.add_argument('--out-dir', type=str,
                        default="../data/processed-data", help="Path to output directory.")
    args = parser.parse_args()

    styled_print("Initiating Data Extractor", header=True)

    if args.book_docx_path is not None:
        styled_print(
            "Extracting Data from The Fire and Blood Book", header=True)
        book_text_dir = create_dir(args.out_dir, "book-csvs", header=False)
        row_paragraphs = extract_paragraphs(
            args.book_docx_path, min_char_count=1)
        styled_print(
            f"Found Total {len(row_paragraphs)} Paragraphs from the Book {args.book_docx_path}", header=False)

        book_df = pd.DataFrame(row_paragraphs.items(),
                               columns=["id", "paragraphs"])
        book_df.to_csv(os.path.join(
            book_text_dir, "book-raw-paragraphs.csv"), index=False, header=True)

    if args.config_file is not None:
        styled_print(
            "Extracting Data for House of Dragons Season", header=True)
        out_dir = create_dir(args.out_dir, "house-of-dragons", header=False)

        with open(args.config_file, 'r') as f:
            hod_data = json.load(f)

        for key in hod_data["house-of-dragons"].keys():
            styled_print(
                f"Working on {key} of House of Dragons", header=True)
            element_dir = create_dir(out_dir, key, header=False)
            elements = {epi["title"]: epi["url"] for epi in
                        hod_data["house-of-dragons"][key]}
            if key != 'subtitles':
                headers = {epi["title"]: epi["headers"]
                           for epi in hod_data["house-of-dragons"][key]}

            styled_print(
                f"Found {len(elements.keys())} {key} ...", header=True)
            for title, url in elements.items():
                styled_print(f"Extracting {title} {key} ...")
                text_dict = extract_fandom_wikis(url, headers[title])
                styled_print(
                    f"Writing Text into {title.replace(' ', '-')}.csv ...")
                hod_df = pd.DataFrame.from_dict(text_dict)
                hod_df.to_csv(os.path.join(
                    element_dir, f"{title.replace(' ', '-')}.csv"), index=False, header=False)
