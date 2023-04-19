import os

from lib.transcribe.utils import (
    get_video_urls,
    get_youtube_video_url_title,
    get_video_id_from_url,
    download_youtube_video,
    transcribe_audio_file,
    save_to_file,
)

from lib.config import Config

def transcribe_main(video_id=None, file_path=None):

    if video_id and not file_path:
        video_url, video_title = get_youtube_video_url_title(video_id)
        print(f"Processing video: {video_title}")
        download_youtube_video(video_url)
        transcription = transcribe_audio_file(
            os.path.join(f'{Config.data_path}/audio/audio_{video_id}.mp3')
        )
        save_to_file(f"transctipt_{video_id}", transcription)
        print(
            f"Transcription saved to {Config.data_path}/transcripts/"
            f"transcript_{video_id}"
        )

    elif file_path and not video_id:
        urls = get_video_urls(file_path)
        for url in urls:
            videoid = get_video_id_from_url(url)

            video_url, video_title = get_youtube_video_url_title(videoid)
            print(f"Processing video: {video_title}")
            download_youtube_video(video_url)
            transcription = transcribe_audio_file(
                os.path.join(f'{Config.data_path}/audio/audio_{videoid}.mp3')
            )
            save_to_file(f"transctipt_{videoid}", transcription)
            print(
                f"Transcription saved to {Config.data_path}/transcripts/"
                f"transcript_{videoid}.txt"
            )

    else:
        print("Choose only one of arguments -v or -f")

if __name__ == "__main__":
    transcribe_main()
