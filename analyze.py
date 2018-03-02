import pandas as pd
from datetime import datetime

from bokeh.plotting import figure, save, output_file
from bokeh.models import ColumnDataSource

print('Done with imports')


def convert_time(time_string):
    pattern = "%Y-%m-%dT%H:%M:%S.%fZ"
    time = datetime.strptime(time_string, pattern)
    if time.minute < 30:
        time = time.replace(minute=0)
    elif time.minute <= 59:
        time = time.replace(minute=30)
    return time


def main():
    print('Analysing data')

    df = pd.read_csv("speeds.csv")

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
    df = df.groupby([df.index.year, df.index.month, df.index.day,
                     df.index.hour, df.index.minute]).mean()
    df.index = df.index.map(lambda x: datetime(*x))

    # Upsample and interpolate data
    df = df.resample('15T').asfreq().interpolate()

    print('Generating result')

    source = ColumnDataSource(df)

    plot = figure(sizing_mode='stretch_both')
    plot.line(x='index', y='download', source=source,
              legend='Download', line_color='red')
    plot.line(x='index', y='upload', source=source,
              legend='Upload', line_color='blue')
    plot.line(x='index', y='ping', source=source,
              legend='Ping', line_color='green')

    output_file('index.html')
    save(plot)


if __name__ == '__main__':
    main()
