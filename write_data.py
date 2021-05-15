import pandas as pd
import numpy as np
import datetime


def perform():
    df = pd.read_csv('./data.csv', names=['start_time', 'end_time', 'upload_mb', 'download_mb', 'total_mb'], header=0)
    df = df.sort_values('start_time')

    df['date'] = df['start_time'].apply(lambda x: '/'.join(str(x).split(' ')[0].split('-')))
    df['day_of_the_month'] = df['start_time'].apply(lambda x: datetime.datetime(*list(map(int, str(x).split(' ')[0].split('-')))).strftime("%d"))
    df['month'] = df['start_time'].apply(lambda x: datetime.datetime(*list(map(int, str(x).split(' ')[0].split('-')))).strftime("%m"))
    df['week'] = df['start_time'].apply(lambda x: datetime.datetime(*list(map(int, str(x).split(' ')[0].split('-')))).strftime("%U"))

    daily_usage = df.groupby('date').agg({'upload_mb': 'sum', 'download_mb': 'sum', 'total_mb': 'sum'})

    date_labels = str(list(daily_usage.reset_index()['date'].array))
    daily_upload_data = str(list(daily_usage['upload_mb'].array))
    daily_download_data = str(list(daily_usage['download_mb'].array))
    daily_total_data = str(list(daily_usage['total_mb'].array))
    with open('data_points.js', 'w') as f:
        f.write(f'date_labels = {date_labels}\n')
        f.write(f'daily_upload_data = {daily_upload_data}\n')
        f.write(f'daily_download_data = {daily_download_data}\n')
        f.write(f'daily_total_data = {daily_total_data}\n')
    f.close()

perform()