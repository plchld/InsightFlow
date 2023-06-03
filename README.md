# InsightFlow 🔍🧠🌐
Welcome to InsightFlow - an AI-powered solution for extracting valuable insights from videos, documentation, and (soon) more! We've harnessed the power of state-of-the-art technologies like Whisper AI, OpenAI GPT, and DeepL to bring an easy solution to chat with long documents. Say goodbye to manual searches and hello to lightning-fast, context-aware answers. 🧠🤖

### Features ✨
1. Video Transcription: Automatically transcribe audio from videos using Whisper AI and convert it into text files. 🎥➡️📄
2. HTML Parsing & Cleaning: Parse and clean HTML documentation pages using OpenAI GPT, making them more readable and concise. 🌐📖
3. Translation: Translate text files into your desired language using DeepL, breaking down language barriers. 🌍🔀🌎
4. Embeddings Creation: Generate embeddings from any number of text files, be it videos, documentation, or other sources. 📚🔗🧩
5. Vector Database Storage: Store your embeddings in a vector database, ensuring efficient and scalable data management. 🗄️💼
6. AI-Powered Q&A: Ask questions and get answers by querying the vector database and leveraging GPT to reason the answer from the most probable documents. 🤔💡
7. Chat Memory: Maintain conversation context with chat memory, providing a seamless and coherent Q&A experience. 💬🔁


### Installation 🛠️
Recommended python >= 3.7. Developed on python 3.10.

Clone the InsightFlow repository:
```bash
git clone https://github.com/plchld/InsightFlow.git
```
Navigate to the project directory:
```bash
cd InsightFlow
```
Install the required dependencies:
```bash
pip install -r requirements/base.txt
```
### Configuration 🔧
- Create a local_settings.py file in the project directory.
- Add your API keys, temperature settings for the GPT models, and the path for the - transcriptions to the local_settings.py file:

```python
YOUTUBE_API_KEY = "Your_Youtube_API_Key" #needed only if you use the video scraper
OPENAI_API_KEY = "Your_OpenAI_API_Key"
COHERE_API_KEY = "Your_Cohere_API_Key" #needed for the embeddings
DATA_PATH = "Your_pathname"
CHAT_MODEL_TEMPERATURE = 0.0 #temprature if using GPT3
GPT_4_TEMPERATURE = 0.0
```
Note: Make sure to replace the placeholders with your actual API keys. Keep the local_settings.py file secure and do not share it with others.

### Running InsightFlow 🚀
- Open a terminal or command prompt.
- Navigate to the InsightFlow project directory.
- Run the run.py script:
```bash
python run.py
```
You will be prompted to choose which module to run (doc_scraping, transcribe, or chat). Follow the prompts to provide the required information for the chosen module.

### Running the documentation scraper 📑
Run the run.py script and choose the "doc_scraping" module.
You will be prompted to enter the URL of the API documentation. The script will parse the HTML, clean the text, and save the cleaned markdown as a .txt file in the current directory.

### Running the YouTube Video Scraper 📹
Run the run.py script and choose the "transcribe" module.
You will be prompted to provide either a YouTube video ID or a file containing a list of YouTube video IDs, one per line.
The script will download the YouTube videos, transcribe the audio, and save the transcriptions to the data/transcripts directory.

### Running the Chat Module 🗣️
Run the run.py script and choose the "chat" module.
- Provide the file directories (it will take all .txt files)
- Choose if you want to translate source documents (it may improve Q&A performance and allow for more context window because of better tokenization)

Start asking questions and receive AI-powered answers with chat history.