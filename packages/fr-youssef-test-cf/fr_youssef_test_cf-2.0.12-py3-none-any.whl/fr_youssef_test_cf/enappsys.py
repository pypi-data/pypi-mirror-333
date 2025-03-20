import requests
import pandas as pd
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from io import StringIO
from .minio_driver import MinioDriver
from .clickhoused import ClickHouseInserter
from .data_transformer import DataTransformer
from .env_vars import *
from .core_env_vars import *
from .util import Util


renamed_columns = {'Day Ahead Price (EPEX)': 'epex_da_price',
                                'Day Ahead Price (Nordpool)': 'nordpool_da_price',
                                'SSP': 'system_sell_price',
                                'SBP': 'system_buy_price',
                                'Date (UTC)': 'date_utc'}

def enapsys_apii(batch_id):
    download_dir = os.path.join(local_download_path, batch_id)
    Util.create_download_dir(download_dir)
    data_source_host = "https://app.enappsys.com"
    data_source_path = "/datadownload?code=gb/elec/epex/latest&currency=GBP&minavmax=false&pass={PASSWORD}&res=hh&tag=csv&timezone=UTC&user={USERNAME}&start={START_DATE}&end={END_DATE}"

    corrected_start_date = '202502202300'
    corrected_end_date = '202503012300'

    source_path_formatted = data_source_path.format(USERNAME=enappsys_username,
                                                                PASSWORD=enappsys_secret,
                                                                START_DATE=corrected_start_date,
                                                                END_DATE=corrected_end_date)
    response = requests.get(data_source_host + source_path_formatted)
    response.raise_for_status()

    # Get the current date and time for filename
    archive_zone_bucket = "youssef-archieve-zone"
    object_id = 'bgs.test.enappsys.elecsystemimbprices'
    current_dt = datetime.now(tz=ZoneInfo('UTC')).strftime('%Y%m%d')
    business_path, domain, dataset, table = object_id.split('.')
    minio_base_key = f'{business_path}/{domain}/{dataset}/{table}'
    minio_archive_key = f'{minio_base_key}/{current_dt}_{batch_id}'
    minio = MinioDriver(aws_access_key_id, aws_secret_access_key, minio_endpoint)
    file_name = "elecsystemimbprices.csv"
    Util.write_file_to_download_dir(download_dir, file_name, response.text)
    downloaded_files = Util.list_local_objects(download_dir)
    minio.minio_upload_object(downloaded_files, download_dir, archive_zone_bucket, minio_archive_key)
    df = pd.read_csv(StringIO(response.text), skiprows=[1])

    df['Date (UTC)'] = pd.to_datetime(
    df['Date (UTC)'].str.replace(r'\[|\]', '', regex=True),
                                    format='%d/%m/%Y %H:%M'
                                ).dt.strftime('%Y-%m-%d %H:%M') + ' +00:00'
    df = df[['Date (UTC)', 'SSP', 'SBP']]
    df = df.rename(columns=renamed_columns)
    df = df.dropna(how='all', subset=df.columns.difference(['date_utc']))
    clickhouse_schema = {'system_sell_price': 'Float64',
                         'system_buy_price': 'Float64',
                         'date_utc': 'DateTime'}
    ingestion_tms = datetime.now(timezone.utc)
    ingestion_month = ingestion_tms.strftime('%Y-%m')
    df['_object_id'] = "bgs.test.enappsys.elecsystemimbprices"
    df["_ingestion_tms"] = ingestion_tms
    df['_ingestion_month'] = ingestion_month
    df["_batch_id"] = batch_id
    normaliser = DataTransformer(clickhouse_schema)
    df = normaliser.normalise_data(df)

    inserter = ClickHouseInserter()
    clickhouse_table_name = f'silver_bgs.`bgs.test.enappsys.elecsystemimbprices`'

    print(df)
    inserter.insert_data(df, clickhouse_table_name)
