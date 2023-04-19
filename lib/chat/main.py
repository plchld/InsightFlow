#!/usr/bin/env python

import os
from lib.chat.process_text import read_input_files, split_texts, create_documents, create_vectordb_from_docs, translate_documents
from lib.chat.retrieval_qa import setup_retrieval_qa

def chat_main():
    # Asking the user for the directory containing input files
    input_directory = input("Enter the directory containing input files: ")

    all_files = os.listdir(input_directory)
    INPUT_FILES = [os.path.join(input_directory, file) for file in all_files if file.endswith(".txt")]

    # Asking the user if they want to translate the documents
    translate_choice = input("Do you want to translate the documents? (yes/no): ")
    if translate_choice.lower() == 'yes':
        # Ask for the DeepL API key
        api_key = input("Enter your DeepL API key: ")

        # Ask the user for the source and target languages
        source_lang = input("Enter the source language (e.g., EL for Greek): ")
        target_lang = input("Enter the target language (e.g., EN for English): ")

        # Translate the input files
        translated_files = translate_documents(INPUT_FILES, api_key, source_lang, target_lang)

        # Read and split the translated input files
        all_combined_articles = read_input_files(translated_files)
    else:
        # Read and split the input files without translation
        all_combined_articles = read_input_files(INPUT_FILES)

    all_texts = split_texts(all_combined_articles)


    # Get the prefixes for each input file
    prefixes = [os.path.splitext(os.path.basename(file))[0][:5] for file in INPUT_FILES]

    # Asking the user for the persist directory path
    PERSIST_DIRECTORY = input("Enter the path for the persist directory: ")

    docs = create_documents(all_texts, prefixes)
    vectordb = create_vectordb_from_docs(docs, PERSIST_DIRECTORY)
    qa = setup_retrieval_qa(vectordb)

    chat_history = []

    # Keep asking the user for queries until they type "stop"
    while True:
        # Asking the user for the query
        query = input("Enter your query (type 'stop' to exit): ")
        
        # Break the loop if the user types "stop"
        if query.lower() == "stop":
            break

        vectordbkwargs = {"search_distance": 0.9}
        result = qa({"query": query, "vectordbkwargs": vectordbkwargs, "chat_history": chat_history})
        
        # Append the result to chat_history
        chat_history.append(result["result"])
        
        print(result['result'])
if __name__ == "__main__":
    chat_main()
