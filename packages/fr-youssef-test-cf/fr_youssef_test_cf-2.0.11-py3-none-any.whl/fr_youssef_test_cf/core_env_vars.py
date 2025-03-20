import os

log_level = os.getenv('LOG_LEVEL', 'INFO')

minio_endpoint = os.getenv('MINIO_ENDPOINT')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


clickhouse_host = os.getenv('CLICKHOUSE_ENDPOINT')
clickhouse_port = os.getenv('CLICKHOUSE_PORT')
clickhouse_user = os.getenv('CLICKHOUSE_USERNAME')
clickhouse_secret = os.getenv('CLICKHOUSE_PASSWORD')

local_download_path = os.getenv('LOCAL_DOWNLOAD_PATH')