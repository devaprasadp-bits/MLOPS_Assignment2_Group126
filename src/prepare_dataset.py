"""
Utility script to prepare and split the Cats vs Dogs dataset.
Run this after downloading the raw dataset from Kaggle.
"""

import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
import argparse


def count_files(directory, pattern):
    """Count files matching pattern in directory."""
    return len(list(Path(directory).glob(pattern)))


def split_dataset(source_dir, output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """
    Split Kaggle cats vs dogs dataset into train/validation/test sets.
    
    Args:
        source_dir: Directory containing raw images (cat.*.jpg, dog.*.jpg)
        output_dir: Output directory for organized dataset
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.001, "Ratios must sum to 1"
    
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    print("=" * 60)
    print("Cats vs Dogs Dataset Preparation")
    print("=" * 60)
    
    # Verify source directory
    if not source_path.exists():
        raise ValueError(f"Source directory not found: {source_dir}")
    
    # Create output directory structure
    print("\nCreating directory structure...")
    for split in ['train', 'validation', 'test']:
        for class_name in ['cats', 'dogs']:
            output_path.joinpath(split, class_name).mkdir(parents=True, exist_ok=True)
    print("Directory structure created")
    
    # Collect cat files
    print("\nCollecting cat images...")
    cat_files = sorted([f for f in os.listdir(source_path) if f.startswith('cat.')])
    print(f"Found {len(cat_files)} cat images")
    
    # Collect dog files
    print("Collecting dog images...")
    dog_files = sorted([f for f in os.listdir(source_path) if f.startswith('dog.')])
    print(f"Found {len(dog_files)} dog images")
    
    # Split cat files
    print("\nSplitting cat images...")
    train_cats, temp_cats = train_test_split(
        cat_files, 
        train_size=train_ratio, 
        random_state=42
    )
    val_size = val_ratio / (val_ratio + test_ratio)
    val_cats, test_cats = train_test_split(
        temp_cats, 
        train_size=val_size, 
        random_state=42
    )
    
    # Split dog files
    print("Splitting dog images...")
    train_dogs, temp_dogs = train_test_split(
        dog_files, 
        train_size=train_ratio, 
        random_state=42
    )
    val_dogs, test_dogs = train_test_split(
        temp_dogs, 
        train_size=val_size, 
        random_state=42
    )
    
    # Copy files to organized structure
    print("\nCopying files to organized structure...")
    
    # Training set
    print("Copying training set...")
    for filename in train_cats:
        shutil.copy(
            source_path / filename, 
            output_path / 'train' / 'cats' / filename
        )
    for filename in train_dogs:
        shutil.copy(
            source_path / filename, 
            output_path / 'train' / 'dogs' / filename
        )
    
    # Validation set
    print("Copying validation set...")
    for filename in val_cats:
        shutil.copy(
            source_path / filename, 
            output_path / 'validation' / 'cats' / filename
        )
    for filename in val_dogs:
        shutil.copy(
            source_path / filename, 
            output_path / 'validation' / 'dogs' / filename
        )
    
    # Test set
    print("Copying test set...")
    for filename in test_cats:
        shutil.copy(
            source_path / filename, 
            output_path / 'test' / 'cats' / filename
        )
    for filename in test_dogs:
        shutil.copy(
            source_path / filename, 
            output_path / 'test' / 'dogs' / filename
        )
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Dataset Split Complete!")
    print("=" * 60)
    print(f"\nTraining Set:")
    print(f"  Cats: {len(train_cats)}")
    print(f"  Dogs: {len(train_dogs)}")
    print(f"  Total: {len(train_cats) + len(train_dogs)}")
    
    print(f"\nValidation Set:")
    print(f"  Cats: {len(val_cats)}")
    print(f"  Dogs: {len(val_dogs)}")
    print(f"  Total: {len(val_cats) + len(val_dogs)}")
    
    print(f"\nTest Set:")
    print(f"  Cats: {len(test_cats)}")
    print(f"  Dogs: {len(test_dogs)}")
    print(f"  Total: {len(test_cats) + len(test_dogs)}")
    
    print(f"\nGrand Total: {len(cat_files) + len(dog_files)} images")
    print("=" * 60)
    
    # Verify
    print("\nVerifying file counts...")
    for split in ['train', 'validation', 'test']:
        cats_count = count_files(output_path / split / 'cats', '*.jpg')
        dogs_count = count_files(output_path / split / 'dogs', '*.jpg')
        print(f"{split.capitalize()}: {cats_count} cats, {dogs_count} dogs")
    
    print("\n✓ Dataset preparation complete!")
    print(f"Organized dataset saved to: {output_dir}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Prepare Cats vs Dogs dataset for training'
    )
    parser.add_argument(
        '--source', 
        type=str, 
        default='train',
        help='Source directory with raw images'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='data',
        help='Output directory for organized dataset'
    )
    parser.add_argument(
        '--train_ratio', 
        type=float, 
        default=0.8,
        help='Training set ratio'
    )
    parser.add_argument(
        '--val_ratio', 
        type=float, 
        default=0.1,
        help='Validation set ratio'
    )
    parser.add_argument(
        '--test_ratio', 
        type=float, 
        default=0.1,
        help='Test set ratio'
    )
    
    args = parser.parse_args()
    
    split_dataset(
        args.source,
        args.output,
        args.train_ratio,
        args.val_ratio,
        args.test_ratio
    )


if __name__ == '__main__':
    main()
