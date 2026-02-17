"""
Unit tests for data preprocessing functions.
"""

import os
import sys
import pytest
import numpy as np
from PIL import Image
import io

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_preprocessing import (
    load_and_preprocess_image,
    preprocess_image_bytes,
    validate_image
)


@pytest.fixture
def sample_image():
    """Create a sample RGB image for testing."""
    img = Image.new('RGB', (224, 224), color='red')
    return img


@pytest.fixture
def sample_image_bytes(sample_image):
    """Convert sample image to bytes."""
    img_bytes = io.BytesIO()
    sample_image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


class TestImagePreprocessing:
    """Test cases for image preprocessing functions."""
    
    def test_load_and_preprocess_image_shape(self, tmp_path, sample_image):
        """Test that preprocessed image has correct shape."""
        # Save sample image
        img_path = tmp_path / "test_image.jpg"
        sample_image.save(img_path)
        
        # Load and preprocess
        result = load_and_preprocess_image(str(img_path), target_size=(224, 224))
        
        # Assert shape
        assert result is not None
        assert result.shape == (224, 224, 3)
    
    def test_load_and_preprocess_image_normalization(self, tmp_path, sample_image):
        """Test that image values are normalized to [0, 1]."""
        img_path = tmp_path / "test_image.jpg"
        sample_image.save(img_path)
        
        result = load_and_preprocess_image(str(img_path))
        
        # Check normalization
        assert result is not None
        assert np.min(result) >= 0.0
        assert np.max(result) <= 1.0
    
    def test_load_and_preprocess_image_invalid_path(self):
        """Test handling of invalid image path."""
        result = load_and_preprocess_image("invalid_path.jpg")
        assert result is None
    
    def test_preprocess_image_bytes_shape(self, sample_image_bytes):
        """Test preprocessing image from bytes."""
        result = preprocess_image_bytes(sample_image_bytes, target_size=(224, 224))
        
        assert result is not None
        assert result.shape == (1, 224, 224, 3)  # Batch dimension added
    
    def test_preprocess_image_bytes_normalization(self, sample_image_bytes):
        """Test that image bytes are normalized correctly."""
        result = preprocess_image_bytes(sample_image_bytes)
        
        assert np.min(result) >= 0.0
        assert np.max(result) <= 1.0
    
    def test_preprocess_image_bytes_invalid(self):
        """Test handling of invalid image bytes."""
        invalid_bytes = io.BytesIO(b"not an image")
        
        with pytest.raises(ValueError):
            preprocess_image_bytes(invalid_bytes)
    
    def test_validate_image_valid(self, tmp_path, sample_image):
        """Test validation of valid image."""
        img_path = tmp_path / "valid_image.jpg"
        sample_image.save(img_path)
        
        assert validate_image(str(img_path)) is True
    
    def test_validate_image_invalid(self, tmp_path):
        """Test validation of invalid image file."""
        # Create a non-image file
        invalid_path = tmp_path / "invalid.txt"
        invalid_path.write_text("not an image")
        
        assert validate_image(str(invalid_path)) is False
    
    def test_load_and_preprocess_different_sizes(self, tmp_path, sample_image):
        """Test preprocessing with different target sizes."""
        img_path = tmp_path / "test_image.jpg"
        sample_image.save(img_path)
        
        sizes = [(128, 128), (256, 256), (224, 224)]
        
        for size in sizes:
            result = load_and_preprocess_image(str(img_path), target_size=size)
            assert result.shape == (size[0], size[1], 3)


class TestDataValidation:
    """Test cases for data validation functions."""
    
    def test_validate_rgb_conversion(self, tmp_path):
        """Test that grayscale images are converted to RGB."""
        # Create grayscale image
        gray_img = Image.new('L', (224, 224), color=128)
        img_path = tmp_path / "gray_image.jpg"
        gray_img.save(img_path)
        
        # Load and check it's converted to RGB
        result = load_and_preprocess_image(str(img_path))
        assert result is not None
        assert result.shape == (224, 224, 3)
    
    def test_image_data_type(self, tmp_path, sample_image):
        """Test that preprocessed image has correct data type."""
        img_path = tmp_path / "test_image.jpg"
        sample_image.save(img_path)
        
        result = load_and_preprocess_image(str(img_path))
        
        # Should be float type after normalization
        assert result.dtype in [np.float32, np.float64]
