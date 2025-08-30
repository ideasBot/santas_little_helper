from enum import Enum
from src.models.interface import ProviderInterface


class ModelProvider(str, Enum):
    GOOGLE = "google"
    SELF_HOSTED = "self_hosted"

    @property
    def provider(self) -> ProviderInterface:
        if self == ModelProvider.GOOGLE:
            from src.models.google import Google

            return Google
        else:
            raise ValueError(f"Unsupported model provider: {self}")
