from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .configModels import Config, Settings, ModelName
from .models import PredictionRequest, PredictionResponse
from .predictor import Predictor
from .autocomplete import AutocompleteModel
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_app():
    config = Config()
    settings = Settings()
    model_name = ModelName()

    app = FastAPI(
        title=config.TITLE,
        description=config.DESCRIPTION,
        version=config.VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    autocomplete_model = AutocompleteModel(model_name=model_name.name)
    model, tokenizer = autocomplete_model.get_model_and_tokenizer()
    predictor = Predictor(model, tokenizer)

    @app.post("/api/predict", response_model=PredictionResponse)
    async def predict(request: PredictionRequest):

        if len(request.text.split()) < settings.MIN_WORDS:
            logger.info(f"Still building context: {request.text}")
            return PredictionResponse(predictions=[])
        else:
            request.text = request.text.rstrip()
            predictions = predictor.predict_next_words(request.text)
            logger.info(f"Predictions: {predictions}")
            return PredictionResponse(predictions=predictions)

    app.mount("/", StaticFiles(directory=settings.FRONTEND_DIR, html=True), name="frontend")

    return app
