"""
CNN model architecture for Cats vs Dogs binary classification.
"""

import tensorflow as tf
from tensorflow.keras import layers, models


def build_baseline_cnn(input_shape=(224, 224, 3), learning_rate=0.001):
    """
    Build a baseline CNN model for binary classification.
    
    Architecture:
    - 3 Convolutional blocks with MaxPooling
    - Flatten and Dense layers
    - Dropout for regularization
    - Sigmoid activation for binary output
    
    Args:
        input_shape: Shape of input images (height, width, channels)
        learning_rate: Learning rate for optimizer
    
    Returns:
        Compiled Keras model
    """
    model = models.Sequential([
        # First convolutional block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Third convolutional block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Fourth convolutional block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    
    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]
    )
    
    return model


def get_model_summary(model):
    """
    Get model architecture summary as string.
    
    Args:
        model: Keras model
    
    Returns:
        String representation of model summary
    """
    import io
    stream = io.StringIO()
    model.summary(print_fn=lambda x: stream.write(x + '\n'))
    return stream.getvalue()
