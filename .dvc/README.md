# DVC Configuration for Data Versioning

## Setup Instructions

### 1. Initialize DVC
```bash
dvc init
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

### 2. Add Remote Storage (Choose one)

#### Option A: Local Remote
```bash
dvc remote add -d local /path/to/local/storage
```

#### Option B: AWS S3
```bash
dvc remote add -d s3remote s3://my-bucket/dvc-storage
dvc remote modify s3remote region us-east-1
```

#### Option C: Google Drive
```bash
dvc remote add -d gdrive gdrive://your-folder-id
```

### 3. Track Dataset

```bash
# Add data directory to DVC tracking
dvc add data/

# Commit the .dvc file
git add data.dvc .gitignore
git commit -m "Track dataset with DVC"

# Push data to remote storage
dvc push
```

### 4. Pull Data (For team members)

```bash
# Pull data from remote storage
dvc pull
```

## Dataset Structure

```
data/
├── train/
│   ├── cats/
│   └── dogs/
├── validation/
│   ├── cats/
│   └── dogs/
└── test/
    ├── cats/
    └── dogs/
```

## DVC Commands Reference

- `dvc add <file>` - Track file with DVC
- `dvc push` - Upload tracked data to remote storage
- `dvc pull` - Download tracked data from remote storage
- `dvc status` - Show changes in tracked files
- `dvc checkout` - Checkout data files to match .dvc files

## Data Pipeline

Create a DVC pipeline for data preprocessing:

```bash
dvc run -n preprocess \
  -d src/data_preprocessing.py \
  -d data/raw \
  -o data/processed \
  python src/data_preprocessing.py
```

## Notes

- Data files are not stored in Git repository
- Only .dvc metadata files and code are version controlled
- Use DVC for reproducibility across different environments
- Dataset size: ~1GB (25,000 cat/dog images)
