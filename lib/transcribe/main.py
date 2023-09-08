import os

from lib.transcribe.utils import (
    get_youtube_video_url_title,
    get_video_id_from_url,
    download_youtube_video,
    transcribe_audio_file,
    save_to_file,
)

from lib.config import Config

def transcribe_main(video_id=None, local_video_file_path=None, prompt_text=None):

    if video_id and not local_video_file_path:
        video_url, video_title = get_youtube_video_url_title(video_id)
        print(f"Processing video: {video_title}")
        download_youtube_video(video_url)
        transcription = transcribe_audio_file(
            os.path.join(f'{Config.data_path}/audio/audio_{video_id}.mp3'),
            prompt_text=prompt_text,
        )
        save_to_file(f"transctipt_{video_id}", transcription)
        print(
            f"Transcription saved to {Config.data_path}/transcripts/"
            f"transcript_{video_id}"
        )

    elif local_video_file_path and not video_id:
        print(f"Processing local video file: {local_video_file_path}")
        transcription = transcribe_audio_file(
            local_video_file_path,
            prompt_text=prompt_text,
        )
        save_to_file(f"transcript_{os.path.basename(local_video_file_path)}.txt", transcription)
        print(
            f"Transcription saved to {Config.data_path}/transcripts/"
            f"transcript_{os.path.basename(local_video_file_path)}.txt"
        )

    else:
        print("Pass either a video id or a local video file path.")


if __name__ == "__main__":
    transcribe_main()
