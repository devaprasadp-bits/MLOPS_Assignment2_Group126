"""
Unit tests for model inference functions.
"""

import os
import sys
import pytest
import numpy as np
from PIL import Image
import io

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model import build_baseline_cnn, get_model_summary


class TestModelArchitecture:
    """Test cases for model building and architecture."""
    
    def test_build_baseline_cnn_output_shape(self):
        """Test that model has correct output shape for binary classification."""
        model = build_baseline_cnn(input_shape=(224, 224, 3))
        
        # Output should be single neuron for binary classification
        assert model.output_shape == (None, 1)
    
    def test_build_baseline_cnn_input_shape(self):
        """Test that model accepts correct input shape."""
        model = build_baseline_cnn(input_shape=(224, 224, 3))
        
        # Input should be 224x224x3
        assert model.input_shape == (None, 224, 224, 3)
    
    def test_build_baseline_cnn_compilation(self):
        """Test that model is properly compiled with optimizer and loss."""
        model = build_baseline_cnn()
        
        # Check compilation
        assert model.optimizer is not None
        assert model.loss == 'binary_crossentropy'
    
    def test_model_prediction_shape(self):
        """Test that model prediction returns correct shape."""
        model = build_baseline_cnn()
        
        # Create dummy input
        dummy_input = np.random.rand(1, 224, 224, 3)
        
        # Get prediction
        prediction = model.predict(dummy_input, verbose=0)
        
        # Check shape
        assert prediction.shape == (1, 1)
    
    def test_model_prediction_range(self):
        """Test that model predictions are in valid probability range [0, 1]."""
        model = build_baseline_cnn()
        
        # Create dummy input
        dummy_input = np.random.rand(5, 224, 224, 3)
        
        # Get predictions
        predictions = model.predict(dummy_input, verbose=0)
        
        # Check range (sigmoid output)
        assert np.all(predictions >= 0.0)
        assert np.all(predictions <= 1.0)
    
    def test_get_model_summary(self):
        """Test that model summary is generated correctly."""
        model = build_baseline_cnn()
        
        summary = get_model_summary(model)
        
        # Summary should contain key information
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert 'conv2d' in summary.lower()
        assert 'dense' in summary.lower()
    
    def test_build_with_custom_learning_rate(self):
        """Test building model with custom learning rate."""
        learning_rate = 0.0001
        model = build_baseline_cnn(learning_rate=learning_rate)
        
        # Check optimizer learning rate
        assert model.optimizer is not None
        assert abs(model.optimizer.learning_rate.numpy() - learning_rate) < 1e-6
    
    def test_build_with_different_input_shape(self):
        """Test building model with different input dimensions."""
        input_shape = (128, 128, 3)
        model = build_baseline_cnn(input_shape=input_shape)
        
        assert model.input_shape == (None, 128, 128, 3)
        
        # Test prediction works
        dummy_input = np.random.rand(1, 128, 128, 3)
        prediction = model.predict(dummy_input, verbose=0)
        assert prediction.shape == (1, 1)


class TestModelMetrics:
    """Test cases for model metrics and evaluation."""
    
    def test_model_has_accuracy_metric(self):
        """Test that model includes accuracy metric."""
        model = build_baseline_cnn()
        
        metric_names = [m.name for m in model.metrics]
        assert 'accuracy' in metric_names
    
    def test_model_has_precision_metric(self):
        """Test that model includes precision metric."""
        model = build_baseline_cnn()
        
        metric_names = [m.name for m in model.metrics]
        # Check for precision metric (name may vary)
        assert any('precision' in name.lower() for name in metric_names)
    
    def test_model_has_recall_metric(self):
        """Test that model includes recall metric."""
        model = build_baseline_cnn()
        
        metric_names = [m.name for m in model.metrics]
        # Check for recall metric (name may vary)
        assert any('recall' in name.lower() for name in metric_names)


class TestModelInference:
    """Test cases for model inference utilities."""
    
    def test_batch_prediction(self):
        """Test that model can handle batch predictions."""
        model = build_baseline_cnn()
        
        batch_sizes = [1, 8, 16]
        
        for batch_size in batch_sizes:
            dummy_input = np.random.rand(batch_size, 224, 224, 3)
            predictions = model.predict(dummy_input, verbose=0)
            assert predictions.shape == (batch_size, 1)
    
    def test_single_image_inference(self):
        """Test inference on single image."""
        model = build_baseline_cnn()
        
        # Single image with batch dimension
        single_image = np.random.rand(1, 224, 224, 3)
        prediction = model.predict(single_image, verbose=0)
        
        assert prediction.shape == (1, 1)
        assert 0.0 <= prediction[0][0] <= 1.0
    
    def test_model_deterministic_inference(self):
        """Test that model gives same output for same input."""
        model = build_baseline_cnn()
        
        # Same input
        test_input = np.random.rand(1, 224, 224, 3)
        
        # Multiple predictions
        pred1 = model.predict(test_input, verbose=0)
        pred2 = model.predict(test_input, verbose=0)
        
        # Should be identical (deterministic)
        np.testing.assert_array_almost_equal(pred1, pred2)
