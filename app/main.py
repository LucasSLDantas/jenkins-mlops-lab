
from fastapi import FastAPI
from pydantic import BaseModel

APP_VERSION = "1.2.2"

app = FastAPI(
    title="Jenkins MLOps Lab",
    version=APP_VERSION
)


class TextInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "API Jenkins MLOps funcionando!",
        "version": APP_VERSION
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: TextInput):
    text = data.text.lower()

    positive = ["bom", "excelente", "otimo", "gostei"]
    negative = ["ruim", "pessimo", "horrivel", "odiei"]

    if any(word in text for word in positive):
        sentiment = "positivo"
    elif any(word in text for word in negative):
        sentiment = "negativo"
    else:
        sentiment = "neutro"

    return {
        "text": data.text,
        "sentiment": sentiment
    }
