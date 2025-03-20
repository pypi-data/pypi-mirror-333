import pandas as pd
import numpy as np
import re
import logging


class DataTransformer:
    """
    Class responsible for converting the Pandas DataFrame columns to match the schema required by ClickHouse.
    Uses a predefined mapping to convert data types.
    """
    
    def __init__(self, schema: dict):
        """
        Initialize the DataNormalizer with the ClickHouse schema.

        :param schema: Dictionary of column names and their data types in the ClickHouse schema.
        """
        self.schema = schema


    def normalise_data(self, df: pd.DataFrame):
        """
        Normalize DataFrame columns to match ClickHouse schema using the data_type_mapping.

        :param df: Input DataFrame with raw data.
        :return: DataFrame with columns converted to match ClickHouse schema.
        """
        
        logging.info("Normalizing data to match ClickHouse schema")
        for column, clickhouse_dtype in self.schema.items():
            column = re.sub('[^0-9a-zA-Z_]+', '_', column).lower().replace('__', '_').strip('_')
            if column in df.columns:
                try:
                    # Fetch the ClickHouse-compatible type from the mapping
                    target_type = clickhouse_dtype.lower()
                    # Convert the column based on its target type for ClickHouse
                    if target_type in ["int16", "int32", "int64", "bigint64", "smallint16"]:
                        df[column] = pd.to_numeric(df[column], errors='raise').astype('Int64')
                    elif target_type in ["float32", "float64", "float", "double", "decimal"]:
                        df[column] = pd.to_numeric(df[column], errors='raise')
                    elif target_type in ["string", "varchar", "char"]:
                        # Preserve NaN values when converting to string
                        df[column] = df[column].astype("object").apply(lambda x: str(x) if pd.notna(x) else None)
                    elif target_type == "uint8":
                        df[column] = df[column].astype("bool").astype("UInt8")  # Convert bools to 0/1
                    elif target_type == "datetime":
                        df[column] = pd.to_datetime(df[column], errors='raise')
                    elif target_type == "date":
                        df[column] = pd.to_datetime(df[column], errors='raise').dt.date
                    elif target_type == "array":
                        df[column] = df[column].apply(lambda x: x if isinstance(x, list) else [])
                    elif target_type == "map":
                        df[column] = df[column].apply(lambda x: x if isinstance(x, dict) else {})
                    elif target_type == "tuple":
                        df[column] = df[column].apply(lambda x: tuple(x) if isinstance(x, (list, tuple)) else ())
                    else:
                        raise Exception(f'Unknown target type: {target_type}')
                except Exception as e:
                    logging.error(f"Error normalizing column {column}: {str(e)}")
                    raise
        df = df.replace({np.nan: None, pd.NaT: None})
        df = df.where(~pd.isna(df), None)
        df['_ingestion_tms'] = pd.to_datetime(df['_ingestion_tms'], errors='raise')
        return df
