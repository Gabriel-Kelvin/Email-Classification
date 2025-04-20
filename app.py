from fastapi import FastAPI
from api.api import router as api_router
from preprocessing.preprocessor import load_dataset, preprocess_dataset
import os

os.environ["TRANSFORMERS_NO_TF"] = "1"

app = FastAPI(
    title="Email Classifier API",
    description="API for classifying emails with PII masking and demasking",
    version="1.0.0"
)

# Mount routes from api/api.py
app.include_router(api_router)

# Optional: Preload and preprocess data on startup (if needed)
@app.on_event("startup")
async def startup_event():
    try:
        path = "data/combined.csv"  # relative path from project root
        df = load_dataset(path)
        df = preprocess_dataset(df)
        print(f"✅ Loaded and preprocessed {len(df)} emails from {path}")
    except Exception as e:
        print(f"❌ Failed to load dataset: {e}")

# Optional root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Email Classifier API"}

# Add this at the bottom of app.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)