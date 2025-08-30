from src.utils.settings import settings

permium_model = settings.default_premium_model_provider.provider.create_model(
    settings.default_premium_model_id
)
model = settings.default_model_provider.provider.create_model(settings.default_model_id)
lite_model = settings.default_lite_model_provider.provider.create_model(
    settings.default_lite_model_id
)

if __name__ == "__main__":
    print("Permium Model:", permium_model)
    print("Model:", model)
    print("Lite Model:", lite_model)
