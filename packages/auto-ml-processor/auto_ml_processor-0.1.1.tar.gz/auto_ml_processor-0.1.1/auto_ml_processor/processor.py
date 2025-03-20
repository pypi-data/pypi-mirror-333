import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score, classification_report
import xgboost as xgb
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib
import os
import requests
import io
import zipfile
from typing import Union, Dict, List, Tuple, Optional, Any
# For Hugging Face datasets
try:
    import datasets
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False
    print("Huggingface hasn't been loaded. For utilize it please setup 'dataset' library.")


class AutoMLProcessor:
    """
    A class to automate data preprocessing and model training for machine learning tasks.
    
    This class provides methods to:
    - Load data from various formats (CSV, Excel, etc.)
    - Handle missing values based on configurable thresholds
    - Automatically detect categorical and numerical features
    - Preprocess features (scaling, encoding)
    - Split data into train/test sets
    - Train various models (XGBoost, KNN, Random Forest)
    - Evaluate model performance
    - Save and load models
    """
    
    def __init__(self, random_state: int = 42, verbose: bool = True):
        """
        Initialize the AutoMLProcessor.
        
        Args:
            random_state (int): Random seed for reproducibility
            verbose (bool): Whether to print information during processing
        """
        self.random_state = random_state
        self.verbose = verbose
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.preprocessor = None
        self.task_type = None  # 'classification' or 'regression'
        self.categorical_cols = []
        self.numerical_cols = []
        
    def _print(self, message: str) -> None:
        """Print message if verbose is True."""
        if self.verbose:
            print(message)
            
    def load_data(self, file_path: str, source_type: str = 'local', **kwargs) -> pd.DataFrame:
        """
        Load data from a file or external source.
        
        Args:
            file_path (str): Path to the data file or identifier for external source
            source_type (str): Source type - 'local', 'url', 'huggingface', 'kaggle', 'openml'
            **kwargs: Additional arguments to pass to data loading functions
            
        Returns:
            pd.DataFrame: Loaded DataFrame
        """
        self._print(f"Loading data from {source_type} source: {file_path}")
        
        # Load from local file
        if source_type == 'local':
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path, **kwargs)
            elif file_path.endswith(('.xls', '.xlsx')):
                self.df = pd.read_excel(file_path, **kwargs)
            elif file_path.endswith('.json'):
                self.df = pd.read_json(file_path, **kwargs)
            elif file_path.endswith('.parquet'):
                self.df = pd.read_parquet(file_path, **kwargs)
            elif file_path.endswith('.feather'):
                self.df = pd.read_feather(file_path, **kwargs)
            elif file_path.endswith('.pickle') or file_path.endswith('.pkl'):
                self.df = pd.read_pickle(file_path, **kwargs)
            else:
                raise ValueError(f"Unsupported local file format: {file_path}")
        
        # Load from URL
        elif source_type == 'url':
            response = requests.get(file_path)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Try to determine file type from URL
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(io.StringIO(response.text), **kwargs)
            elif file_path.endswith(('.xls', '.xlsx')):
                self.df = pd.read_excel(io.BytesIO(response.content), **kwargs)
            elif file_path.endswith('.json'):
                self.df = pd.read_json(io.StringIO(response.text), **kwargs)
            elif file_path.endswith('.parquet'):
                self.df = pd.read_parquet(io.BytesIO(response.content), **kwargs)
            elif file_path.endswith('.zip'):
                # Handle zipped CSV files
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    # Find first CSV file in the zip
                    csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                    if not csv_files:
                        raise ValueError("No CSV file found in the ZIP archive")
                    with z.open(csv_files[0]) as f:
                        self.df = pd.read_csv(f, **kwargs)
            else:
                # Default to CSV if can't determine type
                try:
                    self.df = pd.read_csv(io.StringIO(response.text), **kwargs)
                except:
                    raise ValueError(f"Could not parse data from URL: {file_path}")
        
        # Load from Hugging Face datasets
        elif source_type == 'huggingface':
            if not HUGGINGFACE_AVAILABLE:
                raise ImportError("Hugging Face datasets package not installed. Install with: pip install datasets")
            
            # Parse dataset name and subset
            parts = file_path.split('/')
            dataset_name = parts[0]
            subset = parts[1] if len(parts) > 1 else None
            
            # Load dataset from Hugging Face
            if subset:
                dataset = datasets.load_dataset(dataset_name, subset)
            else:
                dataset = datasets.load_dataset(dataset_name)
            
            # Convert to DataFrame
            split = kwargs.get('split', 'train')
            self.df = dataset[split].to_pandas()
        
        # Load from Kaggle
        elif source_type == 'kaggle':
            try:
                import kaggle
            except ImportError:
                raise ImportError("Kaggle API package not installed. Install with: pip install kaggle")
            
            # Parse Kaggle dataset identifier (owner/dataset-name)
            # Use credentials from ~/.kaggle/kaggle.json
            dataset_path = kwargs.get('download_path', './kaggle_data')
            os.makedirs(dataset_path, exist_ok=True)
            
            # Download the dataset
            kaggle.api.dataset_download_files(file_path, path=dataset_path, unzip=True)
            
            # Find CSV files in the download directory
            csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
            if not csv_files:
                raise ValueError(f"No CSV file found in Kaggle dataset: {file_path}")
            
            # Load the first CSV file
            csv_path = os.path.join(dataset_path, csv_files[0])
            self.df = pd.read_csv(csv_path, **kwargs)
        
        # Load from OpenML
        elif source_type == 'openml':
            try:
                from sklearn.datasets import fetch_openml
            except ImportError:
                raise ImportError("scikit-learn not installed or outdated. Install with: pip install scikit-learn")
            
            # Fetch dataset from OpenML
            dataset_id = int(file_path) if file_path.isdigit() else file_path
            data = fetch_openml(name=dataset_id, version=kwargs.get('version', 1), as_frame=True)
            
            # Combine features and target
            self.df = data.data.copy()
            if hasattr(data, 'target') and data.target is not None:
                target_name = kwargs.get('target_name', 'target')
                self.df[target_name] = data.target
        
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
            
        self._print(f"Data loaded successfully with shape {self.df.shape}")
        return self.df
    
    def handle_missing_values(self, 
                             fill_na_threshold: float = 0.6, 
                             strategy: Dict[str, str] = None,
                             custom_values: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        
        Args:
            fill_na_threshold (float): Threshold for column removal (e.g., 0.6 means 
                                      remove columns with >= 60% missing values)
            strategy (Dict[str, str]): Dictionary mapping column names to imputation strategies
                                      ('mean', 'median', 'most_frequent', 'constant')
            custom_values (Dict[str, Any]): Dictionary mapping column names to custom imputation values
            
        Returns:
            pd.DataFrame: DataFrame with handled missing values
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        # Calculate percentage of missing values for each column
        missing_percentage = self.df.isnull().mean()
        
        # Remove columns with missing values above threshold
        cols_to_drop = missing_percentage[missing_percentage >= fill_na_threshold].index.tolist()
        if cols_to_drop:
            self._print(f"Dropping columns with ≥{fill_na_threshold*100}% missing values: {cols_to_drop}")
            self.df = self.df.drop(columns=cols_to_drop)
        
        # Handle remaining missing values
        strategy = strategy or {}
        custom_values = custom_values or {}
        
        for col in self.df.columns:
            if self.df[col].isnull().any():
                if col in custom_values:
                    self._print(f"Filling missing values in {col} with custom value: {custom_values[col]}")
                    self.df[col] = self.df[col].fillna(custom_values[col])
                elif col in strategy:
                    self._print(f"Filling missing values in {col} with strategy: {strategy[col]}")
                    if strategy[col] == 'mean':
                        self.df[col] = self.df[col].fillna(self.df[col].mean())
                    elif strategy[col] == 'median':
                        self.df[col] = self.df[col].fillna(self.df[col].median())
                    elif strategy[col] == 'most_frequent':
                        self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
                    elif strategy[col] == 'constant':
                        self.df[col] = self.df[col].fillna(0)
                    else:
                        raise ValueError(f"Unknown strategy: {strategy[col]}")
                else:
                    # Auto-detect strategy based on data type
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        self._print(f"Auto-filling missing values in numeric column {col} with mean")
                        self.df[col] = self.df[col].fillna(self.df[col].mean())
                    else:
                        self._print(f"Auto-filling missing values in non-numeric column {col} with most frequent value")
                        self.df[col] = self.df[col].fillna(self.df[col].mode()[0] if not self.df[col].mode().empty else "UNKNOWN")
        
        return self.df
    
    def _detect_feature_types(self) -> Tuple[List[str], List[str]]:
        """
        Automatically detect categorical and numerical columns.
        
        Returns:
            Tuple[List[str], List[str]]: Lists of categorical and numerical column names
        """
        categorical_cols = []
        numerical_cols = []
        
        for col in self.df.columns:
            # Skip target column
            if col == self.target_col:
                continue
                
            # Detect categorical columns
            if pd.api.types.is_categorical_dtype(self.df[col]) or \
               pd.api.types.is_object_dtype(self.df[col]) or \
               pd.api.types.is_bool_dtype(self.df[col]) or \
               (pd.api.types.is_numeric_dtype(self.df[col]) and self.df[col].nunique() < 10):
                categorical_cols.append(col)
            # Detect numerical columns
            elif pd.api.types.is_numeric_dtype(self.df[col]):
                numerical_cols.append(col)
                
        self._print(f"Detected {len(categorical_cols)} categorical features: {categorical_cols}")
        self._print(f"Detected {len(numerical_cols)} numerical features: {numerical_cols}")
        
        self.categorical_cols = categorical_cols
        self.numerical_cols = numerical_cols
        
        return categorical_cols, numerical_cols
    
    def _create_preprocessor(self) -> ColumnTransformer:
        """
        Create a column transformer for preprocessing features.
        
        Returns:
            ColumnTransformer: Scikit-learn preprocessor
        """
        # Detect feature types if not already done
        if not self.categorical_cols and not self.numerical_cols:
            self._detect_feature_types()
            
        # Define preprocessing for numerical columns
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        
        # Define preprocessing for categorical columns
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Combine preprocessing steps
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.numerical_cols),
                ('cat', categorical_transformer, self.categorical_cols)
            ])
            
        self.preprocessor = preprocessor
        return preprocessor
    
    def prepare_data(self, 
                    target_col: str, 
                    test_size: float = 0.2, 
                    stratify: bool = True,
                    drop_cols: List[str] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare data for model training by splitting into train/test sets and preprocessing.
        
        Args:
            target_col (str): Name of the target column
            test_size (float): Proportion of data to use for testing
            stratify (bool): Whether to stratify the split (for classification)
            drop_cols (List[str]): Additional columns to drop
            
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: X_train, X_test, y_train, y_test
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        self.target_col = target_col
        
        # Drop specified columns
        if drop_cols:
            self._print(f"Dropping additional columns: {drop_cols}")
            self.df = self.df.drop(columns=[col for col in drop_cols if col in self.df.columns])
            
        # Extract target variable
        y = self.df[target_col]
        X = self.df.drop(columns=[target_col])
        
        # Detect task type
        if pd.api.types.is_numeric_dtype(y) and y.nunique() > 10:
            self.task_type = 'regression'
            self._print(f"Detected regression task for target '{target_col}'")
            stratify_param = None
        else:
            self.task_type = 'classification'
            self._print(f"Detected classification task for target '{target_col}'")
            stratify_param = y if stratify else None
            
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=stratify_param
        )
        
        self._print(f"Data split into train ({self.X_train.shape[0]} samples) and test ({self.X_test.shape[0]} samples)")
        
        # Create and fit preprocessor
        preprocessor = self._create_preprocessor()
        
        # Transform data
        self.X_train_processed = preprocessor.fit_transform(self.X_train)
        self.X_test_processed = preprocessor.transform(self.X_test)
        
        self._print(f"Features processed: Train shape {self.X_train_processed.shape}, Test shape {self.X_test_processed.shape}")
        
        return self.X_train_processed, self.X_test_processed, self.y_train, self.y_test
        
    def train_model(self, 
                   model_name: str = 'xgboost', 
                   params: Dict[str, Any] = None) -> Any:
        """
        Train a model on the prepared data.
        
        Args:
            model_name (str): Name of the model to train ('xgboost', 'knn', 'random_forest')
            params (Dict[str, Any]): Parameters for the model
            
        Returns:
            Any: Trained model
        """
        if self.X_train_processed is None or self.y_train is None:
            raise ValueError("Data not prepared. Call prepare_data() first.")
            
        params = params or {}
        
        self._print(f"Training {model_name} model for {self.task_type} task")
        
        # Initialize model based on task type and model name
        if self.task_type == 'classification':
            if model_name.lower() == 'xgboost':
                model = xgb.XGBClassifier(random_state=self.random_state, **params)
            elif model_name.lower() == 'knn':
                model = KNeighborsClassifier(**params)
            elif model_name.lower() == 'random_forest':
                model = RandomForestClassifier(random_state=self.random_state, **params)
            else:
                raise ValueError(f"Unsupported model: {model_name}")
        else:  # regression
            if model_name.lower() == 'xgboost':
                model = xgb.XGBRegressor(random_state=self.random_state, **params)
            elif model_name.lower() == 'knn':
                model = KNeighborsRegressor(**params)
            elif model_name.lower() == 'random_forest':
                model = RandomForestRegressor(random_state=self.random_state, **params)
            else:
                raise ValueError(f"Unsupported model: {model_name}")
                
        # Train model
        model.fit(self.X_train_processed, self.y_train)
        self.model = model
        
        self._print(f"{model_name} model trained successfully")
        return model
    
    def evaluate_model(self) -> Dict[str, Any]:
        """
        Evaluate the trained model on test data.
        
        Returns:
            Dict[str, Any]: Dictionary of evaluation metrics
        """
        if self.model is None:
            raise ValueError("No model trained. Call train_model() first.")
            
        # Make predictions
        y_pred = self.model.predict(self.X_test_processed)
        
        # Calculate metrics based on task type
        if self.task_type == 'classification':
            metrics = {
                'accuracy': accuracy_score(self.y_test, y_pred),
                'classification_report': classification_report(self.y_test, y_pred, output_dict=True)
            }
            self._print(f"Model accuracy: {metrics['accuracy']:.4f}")
            
            # If model supports probability predictions
            if hasattr(self.model, 'predict_proba'):
                try:
                    y_prob = self.model.predict_proba(self.X_test_processed)
                    # Additional metrics could be added here (AUC, etc.)
                except:
                    pass
        else:  # regression
            metrics = {
                'mse': mean_squared_error(self.y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_pred)),
                'r2': r2_score(self.y_test, y_pred)
            }
            self._print(f"Model RMSE: {metrics['rmse']:.4f}, R²: {metrics['r2']:.4f}")
            
        return metrics
    
    def save_model(self, path: str) -> None:
        """
        Save the trained model and preprocessor to disk.
        
        Args:
            path (str): Directory path to save model files
        """
        if self.model is None or self.preprocessor is None:
            raise ValueError("No model or preprocessor to save. Train a model first.")
            
        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        
        # Save model
        model_path = os.path.join(path, "model.joblib")
        joblib.dump(self.model, model_path)
        
        # Save preprocessor
        preprocessor_path = os.path.join(path, "preprocessor.joblib")
        joblib.dump(self.preprocessor, preprocessor_path)
        
        # Save metadata
        metadata = {
            'task_type': self.task_type,
            'categorical_cols': self.categorical_cols,
            'numerical_cols': self.numerical_cols,
            'target_col': self.target_col,
            'model_type': type(self.model).__name__
        }
        metadata_path = os.path.join(path, "metadata.joblib")
        joblib.dump(metadata, metadata_path)
        
        self._print(f"Model and preprocessor saved to {path}")
        
    @classmethod
    def load_model(cls, path: str) -> 'AutoMLProcessor':
        """
        Load a trained model and preprocessor from disk.
        
        Args:
            path (str): Directory path where model files are saved
            
        Returns:
            AutoMLProcessor: Instance with loaded model and preprocessor
        """
        # Initialize new instance
        instance = cls(verbose=True)
        
        # Load model
        model_path = os.path.join(path, "model.joblib")
        instance.model = joblib.load(model_path)
        
        # Load preprocessor
        preprocessor_path = os.path.join(path, "preprocessor.joblib")
        instance.preprocessor = joblib.load(preprocessor_path)
        
        # Load metadata
        metadata_path = os.path.join(path, "metadata.joblib")
        metadata = joblib.load(metadata_path)
        
        # Set attributes from metadata
        for key, value in metadata.items():
            setattr(instance, key, value)
            
        instance._print(f"Model and preprocessor loaded from {path}")
        return instance
    
    def predict(self, data: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            data (Union[pd.DataFrame, np.ndarray]): New data for prediction
            
        Returns:
            np.ndarray: Predictions
        """
        if self.model is None or self.preprocessor is None:
            raise ValueError("No model or preprocessor. Either train or load a model first.")
            
        # Preprocess input data
        if isinstance(data, pd.DataFrame):
            processed_data = self.preprocessor.transform(data)
        else:
            processed_data = data
            
        # Make predictions
        predictions = self.model.predict(processed_data)
        return predictions

    def full_process(self, 
                    file_path: str, 
                    target_col: str,
                    fill_na_threshold: float = 0.6,
                    test_size: float = 0.2,
                    model_name: str = 'xgboost',
                    model_params: Dict[str, Any] = None,
                    save_path: Optional[str] = None,
                    source_type: str = 'local',
                    **kwargs) -> Dict[str, Any]:
        """
        Run the full data processing and modeling pipeline in one call.
        
        Args:
            file_path (str): Path to the data file or identifier for external source
            target_col (str): Name of the target column
            fill_na_threshold (float): Threshold for column removal
            test_size (float): Proportion of data to use for testing
            model_name (str): Name of the model to train
            model_params (Dict[str, Any]): Parameters for the model
            save_path (Optional[str]): Path to save the model (if None, model is not saved)
            source_type (str): Source type - 'local', 'url', 'huggingface', 'kaggle', 'openml'
            **kwargs: Additional arguments for data loading
            
        Returns:
            Dict[str, Any]: Dictionary with model evaluation metrics
        """
        # Load data
        self.load_data(file_path, source_type=source_type, **kwargs)
        
        # Handle missing values
        self.handle_missing_values(fill_na_threshold=fill_na_threshold)
        
        # Prepare data
        self.prepare_data(target_col=target_col, test_size=test_size)
        
        # Train model
        self.train_model(model_name=model_name, params=model_params)
        
        # Evaluate model
        metrics = self.evaluate_model()
        
        # Save model if path provided
        if save_path:
            self.save_model(save_path)
            
        return metrics