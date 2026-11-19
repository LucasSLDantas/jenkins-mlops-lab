from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Jenkins MLOps Lab",
    version="1.0.0"
)

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {
        "message": "API Jenkins MLOps funcionando!",
        "version": "1.0.0"
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
