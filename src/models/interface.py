from abc import ABC, abstractmethod


class ProviderInterface(ABC):
    @classmethod
    @abstractmethod
    def create_model(cls, model_id: str, **kwargs):
        pass
