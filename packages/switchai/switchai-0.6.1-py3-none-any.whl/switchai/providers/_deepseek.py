from openai import OpenAI

from ._openai import OpenaiClientAdapter
from ..utils import Task

SUPPORTED_MODELS = {
    "deepseek-chat": [Task.TEXT_GENERATION],
    "deepseek-reasoner": [Task.TEXT_GENERATION],
}


class DeepseekClientAdapter(OpenaiClientAdapter):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
