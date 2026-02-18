"""Create a simple test model if none exists."""
import os
import tensorflow as tf
from tensorflow.keras import layers, models

MODEL_PATH = 'models/cats_dogs_model.h5'

if not os.path.exists(MODEL_PATH):
    print(f"Creating model at {MODEL_PATH}...")
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    os.makedirs('models', exist_ok=True)
    model.save(MODEL_PATH)
    print(f"✓ Model created successfully")
else:
    print(f"✓ Model already exists at {MODEL_PATH}")
