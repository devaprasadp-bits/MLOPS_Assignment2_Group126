"""
Training script for Cats vs Dogs classification model with MLflow experiment tracking.
"""

import os
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
import mlflow
import mlflow.tensorflow

from model import build_baseline_cnn
from data_preprocessing import create_data_generators


def plot_training_history(history, save_path='training_history.png'):
    """
    Plot and save training history (loss and accuracy curves).
    
    Args:
        history: Keras training history object
        save_path: Path to save the plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot accuracy
    axes[0].plot(history.history['accuracy'], label='Train Accuracy')
    axes[0].plot(history.history['val_accuracy'], label='Val Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True)
    
    # Plot loss
    axes[1].plot(history.history['loss'], label='Train Loss')
    axes[1].plot(history.history['val_loss'], label='Val Loss')
    axes[1].set_title('Model Loss')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Training history plot saved to {save_path}")


def plot_confusion_matrix(y_true, y_pred, save_path='confusion_matrix.png'):
    """
    Generate and save confusion matrix visualization.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        save_path: Path to save the plot
    """
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Cat', 'Dog'], 
                yticklabels=['Cat', 'Dog'])
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Confusion matrix saved to {save_path}")


def evaluate_model(model, test_generator):
    """
    Evaluate model on test set and generate metrics.
    
    Args:
        model: Trained Keras model
        test_generator: Test data generator
    
    Returns:
        Dictionary of evaluation metrics
    """
    # Get predictions
    predictions = model.predict(test_generator)
    y_pred = (predictions > 0.5).astype(int).flatten()
    y_true = test_generator.classes
    
    # Calculate metrics
    test_loss, test_accuracy, test_precision, test_recall = model.evaluate(test_generator)
    
    # Generate confusion matrix
    plot_confusion_matrix(y_true, y_pred)
    
    # Generate classification report
    report = classification_report(y_true, y_pred, target_names=['Cat', 'Dog'])
    print("\nClassification Report:")
    print(report)
    
    metrics = {
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'test_precision': float(test_precision),
        'test_recall': float(test_recall)
    }
    
    return metrics


def train_model(train_dir, val_dir, config):
    """
    Main training function with MLflow tracking.
    
    Args:
        train_dir: Training data directory
        val_dir: Validation data directory
        config: Dictionary of training configuration
    """
    print("=" * 50)
    print("Starting Training Run")
    print("=" * 50)
    
    # Set MLflow experiment
    mlflow.set_experiment("cats_vs_dogs_classification")
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(config)
        
        # Create data generators
        print("\nPreparing data generators...")
        train_generator, val_generator = create_data_generators(
            train_dir, 
            val_dir,
            batch_size=config['batch_size'],
            target_size=(config['image_size'], config['image_size'])
        )
        
        print(f"Training samples: {train_generator.samples}")
        print(f"Validation samples: {val_generator.samples}")
        
        # Build model
        print("\nBuilding model...")
        model = build_baseline_cnn(
            input_shape=(config['image_size'], config['image_size'], 3),
            learning_rate=config['learning_rate']
        )
        
        print(model.summary())
        
        # Callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                verbose=1
            )
        ]
        
        # Train model
        print("\nStarting training...")
        history = model.fit(
            train_generator,
            epochs=config['epochs'],
            validation_data=val_generator,
            callbacks=callbacks,
            verbose=1
        )
        
        # Log metrics
        for epoch in range(len(history.history['loss'])):
            mlflow.log_metric('train_loss', history.history['loss'][epoch], step=epoch)
            mlflow.log_metric('train_accuracy', history.history['accuracy'][epoch], step=epoch)
            mlflow.log_metric('val_loss', history.history['val_loss'][epoch], step=epoch)
            mlflow.log_metric('val_accuracy', history.history['val_accuracy'][epoch], step=epoch)
        
        # Plot and log training history
        plot_training_history(history)
        mlflow.log_artifact('training_history.png')
        
        # Save model
        model_dir = 'models'
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, 'cats_dogs_model.h5')
        model.save(model_path)
        print(f"\nModel saved to {model_path}")
        
        # Log model
        mlflow.tensorflow.log_model(model, "model")
        
        # Log confusion matrix
        mlflow.log_artifact('confusion_matrix.png')
        
        # Final metrics
        final_train_accuracy = history.history['accuracy'][-1]
        final_val_accuracy = history.history['val_accuracy'][-1]
        
        print("\n" + "=" * 50)
        print("Training Complete!")
        print(f"Final Training Accuracy: {final_train_accuracy:.4f}")
        print(f"Final Validation Accuracy: {final_val_accuracy:.4f}")
        print("=" * 50)


def main():
    """
    Main entry point for training script.
    """
    parser = argparse.ArgumentParser(description='Train Cats vs Dogs classifier')
    parser.add_argument('--train_dir', type=str, default='data/train',
                        help='Path to training data directory')
    parser.add_argument('--val_dir', type=str, default='data/validation',
                        help='Path to validation data directory')
    parser.add_argument('--epochs', type=int, default=20,
                        help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Batch size for training')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                        help='Learning rate')
    parser.add_argument('--image_size', type=int, default=224,
                        help='Image size (height/width)')
    
    args = parser.parse_args()
    
    # Training configuration
    config = {
        'epochs': args.epochs,
        'batch_size': args.batch_size,
        'learning_rate': args.learning_rate,
        'image_size': args.image_size,
        'optimizer': 'Adam',
        'loss_function': 'binary_crossentropy',
        'model_architecture': 'baseline_cnn'
    }
    
    # Train model
    train_model(args.train_dir, args.val_dir, config)


if __name__ == '__main__':
    main()
