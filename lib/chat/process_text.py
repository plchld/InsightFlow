# process_text.py

from lib.chat.setup import openai_embeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders.csv_loader import CSVLoader
import requests
import json
import chardet


def read_input_files(file_paths):
    combined_articles = []
    for file_path in file_paths:
        content = read_file(file_path)
        combined_articles.append(content)
    return combined_articles


def split_texts(all_combined_articles):
    all_texts = []
    text_splitter = RecursiveCharacterTextSplitter(
                                                  chunk_size=4096,
                                                  chunk_overlap=256,
                                                  length_function=len
                                                  )
    for combined_articles in all_combined_articles:
        all_texts.append(text_splitter.split_text(combined_articles))
    return all_texts

def create_documents(all_texts, prefixes):
    all_docs = []
    for texts, prefix in zip(all_texts, prefixes):
        metadatas = [{"SOURCES": f"{prefix}{i}"} for i in range(len(texts))]
        docs = [Document(id=f'{prefix}{i}', page_content=texts[i], metadata=metadatas[i]) for i in range(len(texts))]
        all_docs.extend(docs)
    return all_docs

def get_fieldnames_from_csv(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        fieldnames = csvfile.readline().strip().split(';')
    return fieldnames

def documents_from_csv(csv_path,fieldnames):
    loader = CSVLoader(file_path=csv_path,
                       csv_args={
                                'delimiter': ';',
                                'quotechar': '"',
                                'fieldnames': fieldnames
})
    docs = loader.load()
    return docs


def create_vectordb_from_docs(docs, persist_directory=None):
    vectordb = Chroma.from_documents(documents=docs, embedding=openai_embeddings, persist_directory=persist_directory)
    if persist_directory:
        vectordb.persist()
    return vectordb


def load_persisted_chromadb(persist_directory):
    vectordb = Chroma(persist_directory=persist_directory, 
                      embedding_function=openai_embeddings)
    return vectordb

def read_file(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    detected_encoding = chardet.detect(raw_data)['encoding']
    content = raw_data.decode(detected_encoding, errors='ignore')
    return content


def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def split_text(text, max_size=16 * 1024):
    words = text.split(' ')
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk)) + len(word) < max_size:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def translate_text(text, api_key, source_lang='EL', target_lang='EN'):
    url = 'https://api-free.deepl.com/v2/translate'
    headers = {'Authorization': f'DeepL-Auth-Key {api_key}'}
    data = {'text': text, 'source_lang': source_lang, 'target_lang': target_lang}
    response = requests.post(url, headers=headers, data=data)
    
    try:
        translations = json.loads(response.text)['translations']
        return translations[0]['text']
    except json.JSONDecodeError:
        print(f"Error: status code {response.status_code}, response content: {response.text}")
        return ""
    
    
def translate_documents(file_paths, api_key, source_lang, target_lang):
    translated_files = []
    for file_path in file_paths:
        text = read_file(file_path)
        chunks = split_text(text)
        translated_chunks = [translate_text(chunk, api_key, source_lang, target_lang) for chunk in chunks]
        translated_text = ' '.join(translated_chunks)

        translated_file_path = f"{file_path[:-4]}_translated.txt"
        write_file(translated_file_path, translated_text)
        translated_files.append(translated_file_path)

    return translated_files


