from agno.models.google import Gemini
from src.utils.settings import settings
from src.models.interface import ProviderInterface


class Google(ProviderInterface):
    @classmethod
    def create_model(cls, model_id: str, **kwargs) -> Gemini:
        return Gemini(
            id=model_id,
            api_key=settings.google_api_key,
            thinking_budget=-1,
            **kwargs,
        )
