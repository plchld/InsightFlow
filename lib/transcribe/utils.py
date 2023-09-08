import math, io, os
import yt_dlp
import pandas as pd
from typing import Tuple, Optional
from pydub import AudioSegment
from lib.config import Config
from googleapiclient.discovery import build
import openai


# Initialize the OpenAI & Youtube API client
openai.api_key = Config.openai_key
youtube = build('youtube', 'v3', developerKey=Config.youtube_key)

from pydub.utils import which

AudioSegment.converter = which("ffmpeg")

def transcribe_local_video_file(video_file_path: str, prompt_text: Optional[str] = None) -> str:
    """
    Wrapper function for transcription of a local video file.

    :param video_file_path: path to local video file
    :param prompt_text: Optional, a context prompt text if available.
    :return: string with transcription
    """
    # Extract audio from the video file
    video = AudioSegment.from_file(video_file_path, "mp4")
    audio_file_path = video_file_path.rsplit(".", 1)[0] + ".wav"
    video.export(audio_file_path, format="wav")

    # Transcribe the audio file
    audio_chunks = split_audio_file(audio_file_path)
    transcription = transcribe_audio_chunks(audio_chunks, prompt_text)

    return transcription


def get_youtube_video_url_title(video_id: str) -> Tuple[str, str]:
    """Gets the YouTube video's URL and title.

    :param video_id: string.
    :return: video's url and title
    """
    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    )
    response = request.execute()
    video = response['items'][0]
    title = video['snippet']['title']
    return f"https://www.youtube.com/watch?v={video_id}", title


def get_video_id_from_url(video_url: str) -> str:
    """Gets video's id from url. url must be of the following form:
    ``https://www.youtube.com/watch?v={video_id}``.

    :param video_url: string, url
    :return: video id
    """

    if not video_url.startswith("https://www.youtube.com/watch?v="):
        raise ValueError(f"{video_url} is not a valid YT URL.")

    return video_url.split("=")[-1]


# Download and save the YouTube video as an audio file
def download_youtube_video(video_url: str) -> None:
    """Downloads and saves the YouTube video as an audio .mp3 file

    :param video_url: string
    :return: None
    """
    video_id = get_video_id_from_url(video_url)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{Config.data_path}/audio/audio_{video_id}',
        'postprocessor_args': ['-vn'],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def download_youtube_videos(video_urls: list) -> None:
    """Download and save multiple videos.

    :param video_urls: list of video urls
    :return: None
    """
    if not video_urls:
        raise ValueError("List of urls is empty")

    for video_url in video_urls:
        download_youtube_video(video_url)

    return None


#splitting because maximum duration is 25min
def split_audio_file(
    audio_file_path: str,
    max_duration: int=25*60*1000,
) -> list:
    """Splits audio file in chunks of ``max_duration`` miliseconds.

    :param audio_file_path:
    :param max_duration: integer, maximum duration of each chunk in ms.
        Default: ``25 ms``.
    :return: list containing audio chunks
    """

    # Max duration in milliseconds (25 minutes)
    audio = AudioSegment.from_file(audio_file_path)
    audio_length = len(audio)
    num_chunks = math.ceil(audio_length / max_duration)
    audio_chunks = []

    for i in range(num_chunks):
        start = i * max_duration
        end = min((i + 1) * max_duration, audio_length)
        audio_chunk = audio[start:end]
        audio_chunks.append(audio_chunk)

    return audio_chunks



def transcribe_audio_chunks(
    audio_chunks: list,
    prompt_text: Optional[str] = None,
) -> str:
    """
    Transcribes the audio chunks one at a time, using the 80 last tokens of each
    chunk as prompt context for the next.

    :param audio_chunks: list of audio chunks.
    :param prompt_text: Optional, a context prompt text if available.
    :return: the transcription
    """
    transcriptions = []

    class NamedBytesIO(io.BytesIO):
        def __init__(self, name, *args, **kwargs):
            self.name = name
            super().__init__(*args, **kwargs)

    for i, audio_chunk in enumerate(audio_chunks):
        with NamedBytesIO(name="chunk.mp3") as byte_stream:
            audio_chunk.export(byte_stream, format="mp3")
            byte_stream.seek(0)

            if prompt_text:
                # Use the transcript of the preceding segment as a prompt
                preceding_transcript = ' '.join(transcriptions[-80:])
                prompt = prompt_text + " " + preceding_transcript
            else:
                prompt = ' '.join(transcriptions[-80:])

            response = openai.Audio.transcribe("whisper-1", byte_stream, prompt=prompt)
        transcriptions.append(response['text'])

    return ' '.join(transcriptions)


def transcribe_audio_file(
    audio_file_path: str,
    prompt_text: Optional[str] = None,
) -> str:
    """
    Wrapper function for transcription of one file.

    :param audio_file_path: path to audio file
    :param prompt_text: Optional, a context prompt text if available.
    :return: string with transcription
    """
    audio_chunks = split_audio_file(audio_file_path)
    transcription = transcribe_audio_chunks(audio_chunks, prompt_text)

    return transcription


def save_to_file(file_name, content):
    transcripts_path = Config.data_path.joinpath("transcripts")
    transcripts_path.mkdir(parents=True, exist_ok=True)
    
    # Save the file to the transcripts directory
    with open(
        os.path.join(transcripts_path, file_name),
        "w",
        encoding="utf-8",
    ) as file:
        file.write(content)



