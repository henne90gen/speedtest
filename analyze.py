import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def convert_times(time_string):
    pattern = "%Y-%m-%dT%H:%M:%S.%fZ"
    time = datetime.strptime(time_string, pattern)
    if time.minute < 30:
        time = time.replace(minute=0)
    elif time.minute <= 59:
        time = time.replace(minute=30)
    return time


def main():
    df = pd.read_csv("speeds.csv")
    columns = ['server_host', 'share', 'server_url', 'server_url2', 'server_sponsor',
               'server_name', 'server_lat', 'server_lon', 'server_d', 'server_latency',
               'server_country', 'server_cc', 'server_id', 'client_lat', 'client_loggedin',
               'client_lon', 'client_ispdlavg', 'client_isprating', 'client_ispulavg', 'client_isp',
               'client_country', 'client_ip', 'client_rating', 'run']
    df = df.drop(columns, axis=1)
    df = df.drop(['bytes_sent', 'bytes_received'], axis=1)
    df.ping *= 100000
    df.timestamp = df.timestamp.map(convert_times)
    df = df.set_index(['timestamp'])
    print(df)
    times = pd.DatetimeIndex(df.index)
    df = df.groupby([times.year, times.month, times.day, times.hour, times.minute]).mean()

    def dummy(x):
        time = datetime(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4])
        print(time)
        return time
    df.index = df.index.map(dummy)
    df = df.resample('30T').asfreq().interpolate()
    print(df)
    df.plot.line()
    plt.show()


if __name__ == '__main__':
    main()
