import pandas as pd
import numpy as np
import warnings
import logging
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler

# Set up logging
LOGGER = logging.getLogger(__name__)

class InvalidDataError(Exception):
    """Custom exception for invalid data errors."""
    pass

class DataProcessor:
    """Preprocess and post-process data before and after synthetic data generation.

    Handles:
    - Type conversions (categorical ↔ numerical).
    - Feature transformations for Gaussian Copula.
    - Reverse transformations to restore original data types.
    """

    def __init__(self, metadata, enforce_rounding=True, enforce_min_max_values=True, model_kwargs=None, table_name=None, locales=['en_US']):
        self.metadata = metadata
        self.enforce_rounding = enforce_rounding
        self.enforce_min_max_values = enforce_min_max_values
        self.model_kwargs = model_kwargs or {}
        self.table_name = table_name
        self.locales = locales
        self._fitted = False
        self._prepared_for_fitting = False
        self.encoders = {}  # Stores encoders for categorical columns
        self.scalers = {}  # Stores scalers for numerical columns
        self.original_columns = None  # To restore column order

    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform the raw data into numerical space."""
        if self._fitted:
            warnings.warn(
                "This model has already been fitted. To use new preprocessed data, "
                "please refit the model using 'fit'."
            )

        self.validate(data)
        self.original_columns = data.columns  # Store original column order
        processed_data = self._preprocess(data)

        return processed_data

    def _preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handles encoding, scaling."""
        data = data.copy()

        for col, dtype in self.metadata.items():
            if dtype == "categorical":
                # Use Label Encoding for small categories, OneHot for larger
                encoder = LabelEncoder() if len(data[col].unique()) < 10 else OneHotEncoder(sparse=False, drop="first")
                transformed_data = self._encode_categorical(data[col], encoder)
                self.encoders[col] = encoder
                data.drop(columns=[col], inplace=True)
                data = pd.concat([data, transformed_data], axis=1)

            elif dtype == "numerical":
                scaler = StandardScaler(with_mean= False, with_std= False)
                data[col] = scaler.fit_transform(data[[col]])
                self.scalers[col] = scaler

            elif dtype == "boolean":
                data[col] = data[col].astype(int)  # Convert True/False to 1/0

            elif dtype == "datetime":
                data[col] = data[col].apply(lambda x: x.timestamp() if pd.notnull(x) else np.nan)  # Convert to Unix timestamp
            
            elif dtype == "timedelta": 
                data[col] = pd.to_timedelta(data[col]).dt.total_seconds()

        return data[self.original_columns]

    def postprocess(self, synthetic_data: pd.DataFrame) -> pd.DataFrame:
        """Transform numerical synthetic data back to its original format."""
        synthetic_data = synthetic_data.copy()

        for col, dtype in self.metadata.items():
            if dtype == "categorical" and col in self.encoders:
                encoder = self.encoders[col]
                synthetic_data[col] = self._decode_categorical(synthetic_data[col], encoder)

            elif dtype == "numerical" and col in self.scalers:
                scaler = self.scalers[col]
                synthetic_data[col] = scaler.inverse_transform(synthetic_data[[col]])

            elif dtype == "boolean":
                synthetic_data[col] = synthetic_data[col].round().astype(bool)

            elif dtype == "datetime":
                synthetic_data[col] = pd.to_datetime(synthetic_data[col], unit='s')

            elif dtype == "timedelta":
                synthetic_data[col] = pd.to_timedelta(synthetic_data[col], unit='s')

        return synthetic_data[self.original_columns]  # Restore original column order

    def validate(self, data: pd.DataFrame):
        """Validate input data."""
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")

        missing_columns = set(self.metadata.keys()) - set(data.columns)
        if missing_columns:
            raise InvalidDataError(f"Missing columns: {missing_columns}")

        primary_keys = [col for col, dtype in self.metadata.items() if dtype == "primary_key"]
        for key in primary_keys:
            if data[key].duplicated().any():
                raise InvalidDataError(f"Primary key '{key}' is not unique.")

    def _encode_categorical(self, series: pd.Series, encoder):
        """Encode categorical columns."""
        if isinstance(encoder, LabelEncoder):
            return pd.DataFrame(encoder.fit_transform(series), columns=[series.name])
        elif isinstance(encoder, OneHotEncoder):
            encoded_array = encoder.fit_transform(series.values.reshape(-1, 1))
            encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out([series.name]))
            return encoded_df

    def _decode_categorical(self, series: pd.Series, encoder):
        """Decode categorical columns."""
        if isinstance(encoder, LabelEncoder):
            return encoder.inverse_transform(series.astype(int))
        elif isinstance(encoder, OneHotEncoder):
            category_index = np.argmax(series.values, axis=1)
            return encoder.categories_[0][category_index]

    def _handle_missing_values(self, series: pd.Series):
        """Handle missing values based on column type."""
        if series.dtype in ["float64", "int64"]:
            return series.fillna(series.median())
        elif series.dtype == "object":
            return series.fillna(series.mode()[0])
        else:
            return series.fillna(0)
