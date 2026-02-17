"""
Monitoring and performance tracking script for deployed model.
Tracks request metrics, latency, and model performance.
"""

import os
import json
import time
from datetime import datetime
from collections import defaultdict
import logging


class ModelMonitor:
    """Monitor model performance and collect metrics."""
    
    def __init__(self, log_file='logs/model_monitor.log'):
        """
        Initialize monitor.
        
        Args:
            log_file: Path to log file
        """
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Initialize metrics
        self.metrics = {
            'total_requests': 0,
            'successful_predictions': 0,
            'failed_predictions': 0,
            'total_latency': 0.0,
            'predictions_by_class': defaultdict(int),
            'hourly_requests': defaultdict(int)
        }
        
        # Setup logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def log_prediction(self, image_name, predicted_class, probability, latency_ms, success=True):
        """
        Log a prediction event.
        
        Args:
            image_name: Name of input image
            predicted_class: Predicted class (cat/dog)
            probability: Prediction confidence
            latency_ms: Prediction latency in milliseconds
            success: Whether prediction was successful
        """
        timestamp = datetime.utcnow().isoformat()
        hour = datetime.utcnow().strftime('%Y-%m-%d %H:00')
        
        # Update metrics
        self.metrics['total_requests'] += 1
        if success:
            self.metrics['successful_predictions'] += 1
            self.metrics['predictions_by_class'][predicted_class] += 1
        else:
            self.metrics['failed_predictions'] += 1
        
        self.metrics['total_latency'] += latency_ms
        self.metrics['hourly_requests'][hour] += 1
        
        # Log event
        log_entry = {
            'timestamp': timestamp,
            'image': image_name,
            'predicted_class': predicted_class,
            'probability': probability,
            'latency_ms': latency_ms,
            'success': success
        }
        
        self.logger.info(json.dumps(log_entry))
    
    def log_error(self, error_message, context=None):
        """
        Log an error event.
        
        Args:
            error_message: Description of error
            context: Additional context information
        """
        timestamp = datetime.utcnow().isoformat()
        
        log_entry = {
            'timestamp': timestamp,
            'type': 'error',
            'message': error_message,
            'context': context
        }
        
        self.logger.error(json.dumps(log_entry))
    
    def get_summary_stats(self):
        """
        Get summary statistics.
        
        Returns:
            Dictionary of summary metrics
        """
        avg_latency = (
            self.metrics['total_latency'] / self.metrics['total_requests']
            if self.metrics['total_requests'] > 0 else 0
        )
        
        success_rate = (
            self.metrics['successful_predictions'] / self.metrics['total_requests']
            if self.metrics['total_requests'] > 0 else 0
        )
        
        return {
            'total_requests': self.metrics['total_requests'],
            'successful_predictions': self.metrics['successful_predictions'],
            'failed_predictions': self.metrics['failed_predictions'],
            'success_rate': round(success_rate * 100, 2),
            'average_latency_ms': round(avg_latency, 2),
            'predictions_by_class': dict(self.metrics['predictions_by_class'])
        }
    
    def print_summary(self):
        """Print summary statistics to console."""
        stats = self.get_summary_stats()
        
        print("\n" + "=" * 60)
        print("Model Performance Summary")
        print("=" * 60)
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Successful Predictions: {stats['successful_predictions']}")
        print(f"Failed Predictions: {stats['failed_predictions']}")
        print(f"Success Rate: {stats['success_rate']}%")
        print(f"Average Latency: {stats['average_latency_ms']}ms")
        print("\nPredictions by Class:")
        for class_name, count in stats['predictions_by_class'].items():
            print(f"  {class_name}: {count}")
        print("=" * 60)


def collect_performance_metrics(predictions_file, ground_truth_file):
    """
    Collect performance metrics by comparing predictions with ground truth.
    
    Args:
        predictions_file: File containing predictions
        ground_truth_file: File containing ground truth labels
    
    Returns:
        Dictionary of performance metrics
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    # Load predictions and ground truth
    with open(predictions_file, 'r') as f:
        predictions = [line.strip() for line in f]
    
    with open(ground_truth_file, 'r') as f:
        ground_truth = [line.strip() for line in f]
    
    # Convert to binary (0: cat, 1: dog)
    pred_binary = [1 if p == 'dog' else 0 for p in predictions]
    truth_binary = [1 if t == 'dog' else 0 for t in ground_truth]
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(truth_binary, pred_binary),
        'precision': precision_score(truth_binary, pred_binary),
        'recall': recall_score(truth_binary, pred_binary),
        'f1_score': f1_score(truth_binary, pred_binary)
    }
    
    print("\nPost-Deployment Performance Metrics:")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1 Score: {metrics['f1_score']:.4f}")
    
    return metrics


if __name__ == '__main__':
    # Example usage
    monitor = ModelMonitor()
    
    # Simulate some predictions
    monitor.log_prediction('cat_001.jpg', 'cat', 0.95, 45.2, success=True)
    monitor.log_prediction('dog_002.jpg', 'dog', 0.88, 42.1, success=True)
    monitor.log_prediction('cat_003.jpg', 'cat', 0.92, 47.5, success=True)
    
    # Print summary
    monitor.print_summary()
