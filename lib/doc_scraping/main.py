#!/usr/bin/env python

import local_settings
import lib.doc_scraping.utils as utils


def doc_scraping_main():
    # Get user input for the URL
    url = input("Enter the URL of the API documentation: ")

    # Parse the HTML page and extract the text content
    text_content = utils.parse_html_to_text(url)

    if text_content:
        # Clean the text and convert it to markdown using GPT
        cleaned_markdown = utils.clean_transcription(text_content)

        # Save the cleaned markdown to a new .txt file in the current folder
        output_file_name = "api_documentation_cleaned_python.txt"
        utils.save_text_to_file(cleaned_markdown, output_file_name)

        print(f"Cleaned markdown has been saved to {output_file_name}")
    else:
        print("Error: Unable to parse API documentation")

if __name__ == '__main__':
    doc_scraping_main()
