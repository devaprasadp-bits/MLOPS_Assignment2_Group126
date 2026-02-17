"""
Smoke tests to verify deployed service is working correctly.
Tests health endpoint and basic prediction functionality.
"""

import os
import sys
import requests
import time
from io import BytesIO
from PIL import Image


def create_test_image():
    """Create a dummy test image."""
    img = Image.new('RGB', (224, 224), color='blue')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def test_health_endpoint(api_url):
    """
    Test the health check endpoint.
    
    Args:
        api_url: Base URL of the API
    
    Returns:
        Boolean indicating success
    """
    try:
        print("Testing health endpoint...")
        response = requests.get(f"{api_url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed")
            print(f"  Status: {data.get('status')}")
            print(f"  Model loaded: {data.get('model_loaded')}")
            return True
        else:
            print(f"✗ Health check failed with status code: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"✗ Health check failed with error: {e}")
        return False


def test_prediction_endpoint(api_url):
    """
    Test the prediction endpoint with a sample image.
    
    Args:
        api_url: Base URL of the API
    
    Returns:
        Boolean indicating success
    """
    try:
        print("\nTesting prediction endpoint...")
        
        # Create test image
        test_image = create_test_image()
        
        # Send prediction request
        files = {'file': ('test_image.jpg', test_image, 'image/jpeg')}
        response = requests.post(f"{api_url}/predict", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Prediction successful")
            print(f"  Class: {data.get('class_label')}")
            print(f"  Probability: {data.get('probability')}")
            print(f"  Prediction time: {data.get('prediction_time_ms')}ms")
            
            # Validate response structure
            required_fields = ['class_label', 'probability', 'prediction_time_ms', 'timestamp']
            for field in required_fields:
                if field not in data:
                    print(f"✗ Missing required field: {field}")
                    return False
            
            # Validate class label
            if data['class_label'] not in ['cat', 'dog']:
                print(f"✗ Invalid class label: {data['class_label']}")
                return False
            
            # Validate probability range
            if not (0.0 <= data['probability'] <= 1.0):
                print(f"✗ Invalid probability: {data['probability']}")
                return False
            
            return True
        else:
            print(f"✗ Prediction failed with status code: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"✗ Prediction test failed with error: {e}")
        return False


def test_invalid_input(api_url):
    """
    Test that the API properly handles invalid input.
    
    Args:
        api_url: Base URL of the API
    
    Returns:
        Boolean indicating success
    """
    try:
        print("\nTesting invalid input handling...")
        
        # Send non-image file
        files = {'file': ('test.txt', BytesIO(b'not an image'), 'text/plain')}
        response = requests.post(f"{api_url}/predict", files=files, timeout=10)
        
        if response.status_code == 400:
            print("✓ Invalid input properly rejected")
            return True
        else:
            print(f"✗ Expected 400 status code, got {response.status_code}")
            return False
    
    except Exception as e:
        print(f"✗ Invalid input test failed with error: {e}")
        return False


def main():
    """Run all smoke tests."""
    # Get API URL from environment or use default
    api_url = os.environ.get('API_URL', 'http://localhost:8000')
    
    print("=" * 60)
    print("Running Smoke Tests")
    print(f"API URL: {api_url}")
    print("=" * 60)
    
    # Wait for service to be ready
    print("\nWaiting for service to be ready...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                print("Service is ready!")
                break
        except:
            pass
        
        if i < max_retries - 1:
            print(f"Retrying ({i+1}/{max_retries})...")
            time.sleep(5)
        else:
            print("Service is not responding. Exiting.")
            sys.exit(1)
    
    # Run tests
    results = []
    results.append(("Health Check", test_health_endpoint(api_url)))
    results.append(("Prediction", test_prediction_endpoint(api_url)))
    results.append(("Invalid Input", test_invalid_input(api_url)))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All smoke tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some smoke tests failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
