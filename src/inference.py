"""
FastAPI inference service for Cats vs Dogs classification model.
Provides REST API endpoints for health check and prediction.
"""

import os
import io
import time
import logging
from datetime import datetime
from typing import Optional
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .data_preprocessing import preprocess_image_bytes


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Application metadata
app = FastAPI(
    title="Cats vs Dogs Classification API",
    description="Binary image classification service for pet adoption platform",
    version="1.0.0"
)


# Global variables for model and metrics
model = None
MODEL_PATH = os.environ.get('MODEL_PATH', 'models/cats_dogs_model.h5')
request_count = 0
total_latency = 0.0


class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    class_label: str
    probability: float
    prediction_time_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    model_loaded: bool
    model_path: str
    requests_served: int
    average_latency_ms: float


def load_model():
    """
    Load the trained model from disk.
    
    Returns:
        Loaded Keras model
    """
    global model
    try:
        if not os.path.exists(MODEL_PATH):
            logger.error(f"Model file not found at {MODEL_PATH}")
            return None
        
        logger.info(f"Loading model from {MODEL_PATH}")
        model = tf.keras.models.load_model(MODEL_PATH)
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None


@app.on_event("startup")
async def startup_event():
    """Load model on application startup."""
    logger.info("Starting up inference service...")
    load_model()
    if model is None:
        logger.warning("Model not loaded - service running in degraded mode")
    else:
        logger.info("Inference service ready")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        Service health status and metrics
    """
    global request_count, total_latency
    
    avg_latency = total_latency / request_count if request_count > 0 else 0.0
    
    return HealthResponse(
        status="healthy" if model is not None else "degraded",
        model_loaded=model is not None,
        model_path=MODEL_PATH,
        requests_served=request_count,
        average_latency_ms=round(avg_latency, 2)
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Prediction endpoint for image classification.
    
    Args:
        file: Uploaded image file
    
    Returns:
        Prediction result with class label and probability
    """
    global request_count, total_latency
    
    start_time = time.time()
    
    try:
        # Validate model is loaded
        if model is None:
            logger.error("Prediction requested but model not loaded")
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            logger.warning(f"Invalid file type received: {file.content_type}")
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and preprocess image
        logger.info(f"Processing image: {file.filename}")
        image_bytes = await file.read()
        image_stream = io.BytesIO(image_bytes)
        
        try:
            processed_image = preprocess_image_bytes(image_stream, target_size=(224, 224))
        except ValueError as e:
            logger.error(f"Image preprocessing failed: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        
        # Make prediction
        prediction = model.predict(processed_image, verbose=0)
        probability = float(prediction[0][0])
        
        # Determine class (0: cat, 1: dog)
        class_label = "dog" if probability > 0.5 else "cat"
        confidence = probability if probability > 0.5 else 1 - probability
        
        # Calculate latency
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        # Update metrics
        request_count += 1
        total_latency += latency_ms
        
        # Log prediction
        logger.info(f"Prediction: {class_label}, Confidence: {confidence:.4f}, Latency: {latency_ms:.2f}ms")
        
        return PredictionResponse(
            class_label=class_label,
            probability=round(confidence, 4),
            prediction_time_ms=round(latency_ms, 2),
            timestamp=datetime.utcnow().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Cats vs Dogs Classification API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        },
        "description": "Binary image classification for pet adoption platform"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
