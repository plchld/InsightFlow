import sys
from pathlib import Path
sys.path.append(str(Path('.').resolve()))

from lib.doc_scraping.main import doc_scraping_main
from lib.transcribe.main import transcribe_main
from lib.chat.main import chat_main

if __name__ == "__main__":
    choice = input("Which module do you want to run? [doc_scraping/transcribe/chat]: ")

    if choice == "doc_scraping":
        doc_scraping_main()
    elif choice == "transcribe":
        video_id = input("Enter video id (v) or leave empty if using a file: ")
        file_path = None
        if not video_id:
            file_path = input("Enter path to file (f): ")
        transcribe_main(video_id, file_path)
    elif choice == "chat":
        chat_main()
    else:
        print("Invalid choice. Please enter either 'doc_scraping', 'transcribe', or 'chat'.")
