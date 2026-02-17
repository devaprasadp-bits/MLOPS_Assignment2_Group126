"""
Data preprocessing utilities for Cats vs Dogs classification.
This module handles loading, preprocessing, and augmentation of image data.
"""

import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split


def load_and_preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess a single image.
    
    Args:
        image_path: Path to the image file
        target_size: Tuple of (height, width) for resizing
    
    Returns:
        Preprocessed image array normalized to [0, 1]
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize(target_size)
        img_array = np.array(img) / 255.0
        return img_array
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None


def preprocess_image_bytes(image_bytes, target_size=(224, 224)):
    """
    Preprocess image from bytes for inference.
    
    Args:
        image_bytes: Image data in bytes
        target_size: Tuple of (height, width) for resizing
    
    Returns:
        Preprocessed image array ready for model input
    """
    try:
        img = Image.open(image_bytes).convert('RGB')
        img = img.resize(target_size)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {e}")


def create_data_generators(train_dir, validation_dir, batch_size=32, target_size=(224, 224)):
    """
    Create data generators for training and validation with augmentation.
    
    Args:
        train_dir: Directory containing training data
        validation_dir: Directory containing validation data
        batch_size: Batch size for training
        target_size: Image dimensions
    
    Returns:
        Tuple of (train_generator, validation_generator)
    """
    # Apply data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    validation_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary',
        shuffle=True
    )
    
    validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary',
        shuffle=False
    )
    
    return train_generator, validation_generator


def prepare_dataset_split(data_dir, output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """
    Split dataset into train, validation, and test sets.
    
    Args:
        data_dir: Directory containing all images organized by class
        output_dir: Directory to save split datasets
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set
    """
    if not os.path.exists(data_dir):
        raise ValueError(f"Data directory {data_dir} does not exist")
    
    # Create output directories
    for split in ['train', 'validation', 'test']:
        for class_name in ['cats', 'dogs']:
            os.makedirs(os.path.join(output_dir, split, class_name), exist_ok=True)
    
    print(f"Dataset split prepared: {train_ratio*100}% train, {val_ratio*100}% val, {test_ratio*100}% test")


def validate_image(image_path):
    """
    Validate if an image file is readable and has correct format.
    
    Args:
        image_path: Path to image file
    
    Returns:
        Boolean indicating if image is valid
    """
    try:
        img = Image.open(image_path)
        img.verify()
        return True
    except:
        return False
