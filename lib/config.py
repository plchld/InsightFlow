from pathlib import Path
from local_settings import (
    OPENAI_API_KEY,
    YOUTUBE_API_KEY,
    DATA_PATH,
    CHAT_MODEL_TEMPERATURE,
    GPT_4_TEMPERATURE,
)


class _Config:
    def __init__(self, project="InsightFlow"):
        self.project_name = project

    @staticmethod
    def create(path):
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def data_path(self):
        path = Path(DATA_PATH)
        return self.create(path)

    @property
    def openai_key(self):
        return OPENAI_API_KEY

    @property
    def youtube_key(self):
        return YOUTUBE_API_KEY

    @property
    def chat_temp(self):
        return CHAT_MODEL_TEMPERATURE

    @property
    def gpt4_temp(self):
        return GPT_4_TEMPERATURE


Config = _Config()
