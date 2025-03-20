# Auto ML Processor

A Python package for automated machine learning preprocessing and model training. This package streamlines common data preprocessing tasks and model training for classification and regression problems.

## Features

- **Automated data loading** from multiple sources:
  - Local files (CSV, Excel, JSON, Parquet, Feather, Pickle)
  - URLs (direct downloads with format detection)
  - Hugging Face datasets
  - Kaggle datasets
  - OpenML datasets
- **Intelligent missing value handling** with configurable thresholds
- **Automatic feature type detection** (categorical vs. numerical)
- **Standardized preprocessing pipeline** for feature engineering
- **Built-in model training** for common algorithms (XGBoost, KNN, Random Forest)
- **Simple evaluation and saving** of models
- **One-line full processing** option for quick execution

## Installation

```bash
pip install auto-ml-processor
```

## Quick Start

```python
from auto_ml_processor import AutoMLProcessor

# Initialize processor
processor = AutoMLProcessor()

# Process data and train model in one line
metrics = processor.full_process(
    file_path='your_data.csv',
    target_col='target_column',
    fill_na_threshold=0.6,  # Remove columns with ≥60% missing values
    model_name='xgboost'
)

print(f"Model performance: {metrics}")
```

## Loading Data from Different Sources

```python
# From a URL
processor.load_data(
    'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',
    source_type='url'
)

# From Hugging Face datasets
processor.load_data(
    'mnist',
    source_type='huggingface',
    split='train'  # Load the training split
)

# From Kaggle
processor.load_data(
    'uciml/iris',
    source_type='kaggle',
    download_path='./kaggle_data'
)

# From OpenML
processor.load_data(
    'iris',  # Dataset name or ID
    source_type='openml'
)
```

## Step-by-Step Usage

```python
# Initialize
processor = AutoMLProcessor(verbose=True)

# Load data
df = processor.load_data('dataset.csv')

# Handle missing values
processor.handle_missing_values(fill_na_threshold=0.6)

# Prepare data
processor.prepare_data(target_col='target', test_size=0.2)

# Train model
processor.train_model(model_name='knn')

# Evaluate
metrics = processor.evaluate_model()

# Save model
processor.save_model('output_directory')
```

## Making Predictions

```python
# Load saved model
loaded_processor = AutoMLProcessor.load_model('output_directory')

# Make predictions on new data
import pandas as pd
new_data = pd.read_csv('new_data.csv')
predictions = loaded_processor.predict(new_data)
```

## License

MIT License