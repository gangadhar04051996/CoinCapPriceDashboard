tokencheck = "vKAI5fb3T51mZMx9DJeAU2ottcJPE6xm_mnnOrFh57drIpWInatooR2hU-ig7dlkM_t9wcEddeO1oPmRUQFXqw=="
org = "ORG_NAME"
token = '3p9FBX9OwpmxC4XB65kmmlmCZDNnaqsKa5PayIRS_-O034OkRKpN0Ra7s_jxV_B2pWLF9WcPr4LISpuaWNeCag=='
import pandas as pd
from influxdb_client import InfluxDBClient, WriteOptions
import influxdb_client, os

bucket="BUCKET2"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=tokencheck, org=org)
if client:
    print(True)
from influxdb_client.client.write_api import SYNCHRONOUS
csvlink = "C:/Users/tilak/Desktop/notebooks/DataSets/appstore_games.csv"
for df in pd.read_csv(csvlink, chunksize= 1000):
    df['Original Release Date'] = pd.DatetimeIndex(df['Original Release Date'])
    df['Current Version Release Date'] = pd.DatetimeIndex(df['Current Version Release Date'])
    with client.write_api(write_options=SYNCHRONOUS) as write_api:
        try:
            write_api.write(bucket=bucket,
                            record= df,
                            data_frame_measurement_name = 'Primary Genre',
                            data_frame_timestamp_column = 'Original Release Date',
                            data_frame_tag_columns=["Primary Genre"],
                            data_frame_field_columns=['ID', 'Name', 'Subtitle', 'Icon URL', 'Average User Rating',
    'User Rating Count', 'Price', 'In-app Purchases', 'Description',
    'Developer', 'Age Rating', 'Languages', 'Size', 'Primary Genre',
    'Genres', 'Original Release Date']
                            )
        except Exception as e:
            print("Falied to Upload the Data")
            print(e)
        



