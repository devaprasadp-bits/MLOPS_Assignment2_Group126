#!/usr/bin/env python
"""Quick script to create a minimal test model for demo purposes."""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TF warnings

print("Creating minimal test model...")
print("(This takes ~30 seconds on first TensorFlow import)")

from tensorflow import keras
from tensorflow.keras import layers

# Create a simple CNN model matching the expected architecture
model = keras.Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Binary classification: cat vs dog
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Save the model
os.makedirs('models', exist_ok=True)
model.save('models/cats_dogs_model.h5')

print("✓ Model saved to models/cats_dogs_model.h5")
print("  This is a minimal untrained model for testing the API/Docker infrastructure.")
print("  For production, train with: python src/train.py --epochs 20")
