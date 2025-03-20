import clickhouse_connect
import logging
import pandas as pd
from .core_env_vars import *

class ClickHouseInserter:
    """
    Class to handle the insertion of normalized data into a ClickHouse table.
    """
    def __init__(self):
        """
        Initialize the ClickHouse Connection.
        """
        self.client = clickhouse_connect.create_client(
            host=clickhouse_host.replace('https://', ''),
            port=clickhouse_port,
            username=clickhouse_user,
            password=clickhouse_secret,
            verify=True,
            interface='https',
            settings={
                'connect_timeout': 3600,
                'receive_timeout': 3600,
                'send_timeout': 3600,
                'session_timeout': 3600
            }
        )

    def insert_data(self, df: pd.DataFrame, table_name: str):
        """
        Insert the normalized data into a ClickHouse table.

        :param df: DataFrame containing the normalized data.
        :param table_name: Name of the ClickHouse table where data will be inserted.
        """
        try:
            logging.info(f"Inserting data into ClickHouse table {table_name}")
            self.client.insert_df(table_name, df)
            logging.info(f"Data inserted successfully into {table_name}")
        except Exception as e:
            logging.error(f"Error inserting data into ClickHouse: {str(e)}")
            raise
