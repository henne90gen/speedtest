import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def convert_time(time_string):
    pattern = "%Y-%m-%dT%H:%M:%S.%fZ"
    time = datetime.strptime(time_string, pattern)
    if time.minute < 30:
        time = time.replace(minute=0)
    elif time.minute <= 59:
        time = time.replace(minute=30)
    return time


def main():
    df = pd.read_csv("speeds.csv")
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
        print(df)
    
    columns = ['server_host', 'share', 'server_url', 'server_sponsor',
               'server_name', 'server_lat', 'server_lon', 'server_d', 'server_latency',
               'server_country', 'server_cc', 'server_id', 'client_lat', 'client_loggedin',
               'client_lon', 'client_ispdlavg', 'client_isprating', 'client_ispulavg', 'client_isp',
               'client_country', 'client_ip', 'client_rating', 'run']
    df = df.drop(columns, axis=1)
    df = df.drop(['bytes_sent', 'bytes_received'], axis=1)
    df.ping *= 100000

    # Convert timestamp to datetime and make it the index
    df.timestamp = df.timestamp.map(convert_time)
    df = df.set_index(['timestamp'])
    
    # Take average of runs
    df = df.groupby([df.index.year, df.index.month, df.index.day, df.index.hour, df.index.minute]).mean()
    df.index = df.index.map(lambda x: datetime(*x))

    # Upsample and interpolate data
    df = df.resample('30T').asfreq().interpolate()

    print(df)
    df.plot.line()
    plt.show()


if __name__ == '__main__':
    main()
