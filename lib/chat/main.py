#!/usr/bin/env python

import os
from lib.chat.process_text import read_input_files, split_texts, create_documents, create_vectordb_from_docs, translate_documents, documents_from_csv, load_persisted_chromadb, get_fieldnames_from_csv
from lib.chat.retrieval_qa import setup_retrieval_qa
from lib.config import Config

def print_colored_output(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def chat_main():
    user_input_color = 35  # Green
    output_color = 37  # Blue
    
    # Asking the user for the directory containing input files
    input_directory = input(f"\033[{user_input_color}mEnter the directory containing input files: \033[0m ")

    all_files = os.listdir(input_directory)
    INPUT_FILES = [os.path.join(input_directory, file) for file in all_files if file.endswith((".txt", ".csv"))]

    # Separate .txt and .csv files
    txt_files = [file for file in INPUT_FILES if file.endswith(".txt")]
    csv_files = [file for file in INPUT_FILES if file.endswith(".csv")]
    if csv_files:
        #this gets the first row of the csv as fieldnames(columns)
        fieldnames = get_fieldnames_from_csv(csv_files[0])
        csv_docs = documents_from_csv(csv_files[0], fieldnames)

    if txt_files:
        # Asking the user if they want to translate the documents
        translate_choice = input(f"\033[{user_input_color}mDo you want to translate the documents? (yes/no): \033[0m")
        if translate_choice.lower() == 'yes':
            # Ask for the DeepL API key
            api_key = input(f"\033[{user_input_color}mEnter your DeepL API key: \033[0m")

            # Ask the user for the source and target languages
            source_lang = input("Enter the source language (e.g., EL for Greek): ")
            target_lang = input("Enter the target language (e.g., EN for English): ")

            # Translate the input files
            translated_files = translate_documents(txt_files, api_key, source_lang, target_lang)

            # Read and split the translated input files
            all_combined_articles = read_input_files(translated_files)
        else:
            # Read and split the input files without translation
            all_combined_articles = read_input_files(txt_files)

        all_texts = split_texts(all_combined_articles)
        prefixes = [os.path.splitext(os.path.basename(file))[0][:5] for file in txt_files]
        docs = create_documents(all_texts, prefixes)

        if csv_files:
            docs += csv_docs
    else:
        docs = csv_docs

    # Asking the user if they have already a vector database they want to load
    load_vectordb_choice = input(f"\033[{user_input_color}mDo you have already a vector database you want to load? (yes/no): \033[0m")

    if load_vectordb_choice.lower() == 'yes':
        # Asking the user for the persist directory path
        PERSIST_DIRECTORY = input(f"\033[{user_input_color}mEnter the path for the persist directory: \033[0m")
        vectordb = load_persisted_chromadb(PERSIST_DIRECTORY)
    else:
        persist_choice = input(f"\033[{user_input_color}mDo you want to persist the vector database? (yes/no): \033[0m")
        if persist_choice.lower() == 'yes':
            PERSIST_DIRECTORY = input(f"\033[{user_input_color}mEnter the path for the persist directory: \033[0m")
            vectordb = create_vectordb_from_docs(docs, PERSIST_DIRECTORY)
        else:
            vectordb = create_vectordb_from_docs(docs)

    qa = setup_retrieval_qa(vectordb)

    chat_history = []

    # Keep asking the user for queries until they type "stop"
    while True:
        # Asking the user for the query
        query = input(f"\033[{user_input_color}mEnter your query (type 'stop' to exit): \033[0m")
        
        # Break the loop if the user types "stop"
        if query.lower() == "stop":
            break

        vectordbkwargs = {"search_distance": 0.9}
        result = qa({"query": query, "vectordbkwargs": vectordbkwargs})
        
        # Append the result to chat_history
        chat_history.append(result["result"])
        
        print(result['result'])

if __name__ == "__main__":
    chat_main()
