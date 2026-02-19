# Dataset Information

## Source
Kaggle: Dogs vs. Cats Dataset  
URL: https://www.kaggle.com/c/dogs-vs-cats/data

## Description
Binary classification dataset containing 25,000 labeled images of cats and dogs.

## Download Instructions

### Option 1: Kaggle CLI (Recommended)

```bash
# Install Kaggle CLI
pip install kaggle

# Setup Kaggle API credentials
# Download kaggle.json from https://www.kaggle.com/settings
mkdir ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Download dataset
kaggle competitions download -c dogs-vs-cats
unzip dogs-vs-cats.zip
unzip train.zip
```

### Option 2: Manual Download

1. Visit https://www.kaggle.com/c/dogs-vs-cats/data
2. Download train.zip
3. Extract to project directory
4. Organize files as described below

## Dataset Organization

After download, organize images into this structure:

```
data/
├── train/
│   ├── cats/
│   │   ├── cat.0.jpg
│   │   ├── cat.1.jpg
│   │   └── ...
│   └── dogs/
│       ├── dog.0.jpg
│       ├── dog.1.jpg
│       └── ...
├── validation/
│   ├── cats/
│   └── dogs/
└── test/
    ├── cats/
    └── dogs/
```

## Dataset Split Script

Use this Python script to split the dataset:

```python
import os
import shutil
from sklearn.model_selection import train_test_split

def split_dataset(source_dir, output_dir, train_ratio=0.8, val_ratio=0.1):
    """Split dataset into train/validation/test sets."""
    
    # Create output directories
    for split in ['train', 'validation', 'test']:
        for class_name in ['cats', 'dogs']:
            os.makedirs(f'{output_dir}/{split}/{class_name}', exist_ok=True)
    
    # Process cats
    cat_files = [f for f in os.listdir(source_dir) if f.startswith('cat.')]
    train_cats, temp_cats = train_test_split(cat_files, train_size=train_ratio, random_state=42)
    val_cats, test_cats = train_test_split(temp_cats, train_size=0.5, random_state=42)
    
    # Process dogs
    dog_files = [f for f in os.listdir(source_dir) if f.startswith('dog.')]
    train_dogs, temp_dogs = train_test_split(dog_files, train_size=train_ratio, random_state=42)
    val_dogs, test_dogs = train_test_split(temp_dogs, train_size=0.5, random_state=42)
    
    # Copy files
    for filename in train_cats:
        shutil.copy(f'{source_dir}/{filename}', f'{output_dir}/train/cats/{filename}')
    for filename in val_cats:
        shutil.copy(f'{source_dir}/{filename}', f'{output_dir}/validation/cats/{filename}')
    for filename in test_cats:
        shutil.copy(f'{source_dir}/{filename}', f'{output_dir}/test/cats/{filename}')
    
    for filename in train_dogs:
        shutil.copy(f'{source_dir}/{filename}', f'{output_dir}/train/dogs/{filename}')
    for filename in val_dogs:
        shutil.copy(f'{source_dir}/{filename}', f'{output_dir}/validation/dogs/{filename}')
    for filename in test_dogs:
        shutil.copy(f'{source_dir}/{filename}', f'{output_dir}/test/dogs/{filename}')
    
    print(f"Train: {len(train_cats)} cats, {len(train_dogs)} dogs")
    print(f"Val: {len(val_cats)} cats, {len(val_dogs)} dogs")
    print(f"Test: {len(test_cats)} cats, {len(test_dogs)} dogs")

# Run split
split_dataset('train', 'data')
```

## Dataset Statistics

- Total Images: 25,000
- Training: 20,000 images (80%)
- Validation: 2,500 images (10%)
- Test: 2,500 images (10%)
- Classes: 2 (cats, dogs)
- Image Format: JPEG
- Size: ~543 MB (compressed)

## Image Preprocessing

All images are preprocessed to:
- Size: 224x224 pixels
- Format: RGB (3 channels)
- Normalization: [0, 1] range
- Data Augmentation: rotation, flip, zoom (training only)

## Data Versioning

Track dataset with DVC:

```bash
dvc add data/
git add data.dvc .gitignore
git commit -m "Add dataset"
dvc push
```

## Notes

- Dataset is large (~1GB uncompressed)
- Use DVC for version control, not Git
- Preprocessing happens during training
- Augmentation applied only to training set
