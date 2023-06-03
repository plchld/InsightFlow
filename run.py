import sys
from pathlib import Path
sys.path.append(str(Path('.').resolve()))

from lib.doc_scraping.main import doc_scraping_main
from lib.transcribe.main import transcribe_main
from lib.chat.main import chat_main

def print_colored_output(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

user_input_color = 35  # Green
output_color = 37  # Blue

if __name__ == "__main__":
    choice = input(f"\033[{user_input_color}mWhich module do you want to run? [doc_scraping/transcribe/chat]: \033[0m ")

    if choice == "doc_scraping":
        doc_scraping_main()
    elif choice == "transcribe":
        video_id = input("Enter video id (v) or leave empty if using a file: ")
        prompt_text = input("Enter a prompt text as context for the transcription: ")
        file_path = None
        if not video_id:
            file_path = input("Enter path to file (f): ")
        transcribe_main(video_id, file_path, prompt_text)
    elif choice == "chat":
        chat_main()
    else:
        print("Invalid choice. Please enter either 'doc_scraping', 'transcribe', or 'chat'.")
