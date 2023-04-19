import requests
from bs4 import BeautifulSoup
import openai
from local_settings import OPENAI_API_KEY

def parse_html_to_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for unwanted_tag in soup(['script', 'style']):
            unwanted_tag.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        cleaned_text = '\n'.join(line for line in lines if line)
        return cleaned_text
    else:
        print(f"Error: Unable to fetch the page (Status code: {response.status_code})")
        return None

def clean_transcription(transcription):
    max_tokens = 2048
    text_chunks = [transcription[i:i+max_tokens] for i in range(0, len(transcription), max_tokens)]
    clean_text_chunks = []
    openai.api_key = OPENAI_API_KEY
    for chunk in text_chunks:
        messages = [
                    {"role": "system", "content": """You are an AI language model that specializes in 
                    cleaning and converting plain text API documentation into well-structured and 
                    nicely formatted markdown. Your task is to take the given plain text and create 
                    markdown that is easy to read and understand, with appropriate headings, 
                    code blocks, and lists where necessary. 
                    DO NOT OUTPUT ANYTHING ELSE EXCEPT the cleaned and formatted markdown as output\\n """},
                    {"role": "user", "content": f"Please clean and convert the following API documentation text into markdown: {chunk}"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.0,
            messages=messages,
        )
        clean_chunk = response['choices'][0]['message']['content']
        clean_text_chunks.append(clean_chunk)
    return ''.join(clean_text_chunks)

def save_text_to_file(text, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)
