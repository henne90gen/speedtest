import pandas as pd
from datetime import datetime, timedelta

from bokeh.plotting import figure, save, output_file
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool, BoxAnnotation

print('Done with imports')


def convert_time(time_string):
    pattern = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(time_string, pattern) + timedelta(hours=1)
    # if time.minute < 30:
    #     time = time.replace(minute=0)
    # elif time.minute <= 59:
    #     time = time.replace(minute=30)
    # return time + 


def create_hover_tool(name, display_data):
    return HoverTool(
        mode='vline',
        names=[name],
        tooltips=[
            ('Time', "@tooltip_datetime"),
            (name, display_data)
        ],
    )


def create_line(source, plot, name, color):
    plot.line(
        x='index',
        y=name.lower(),
        source=source,
        legend=name,
        line_color=color,
        name=name
    )


def main():
    print('Analysing data')

    df = pd.read_csv("speeds.csv")

    columns = ['server_host', 'share', 'server_url', 'server_sponsor',
               'server_name', 'server_lat', 'server_lon', 'server_d', 'server_latency',
               'server_country', 'server_cc', 'server_id', 'client_lat', 'client_loggedin',
               'client_lon', 'client_ispdlavg', 'client_isprating', 'client_ispulavg', 'client_isp',
               'client_country', 'client_ip', 'client_rating', 'run', 'bytes_sent', 'bytes_received']
    df = df.drop(columns, axis=1)

    df.ping /= 100
    df.download /= 1024 * 1024
    df.upload /= 1024 * 1024

    # Convert timestamp to datetime and make it the index
    df.timestamp = df.timestamp.map(convert_time)
    df = df.set_index(['timestamp'])

    # Take average of runs
    df = df.groupby([df.index.year, df.index.month, df.index.day,
                     df.index.hour, df.index.minute, df.index.second]).mean()
    df.index = df.index.map(lambda x: datetime(*x))

    # Upsample and interpolate data
    regular_intervall = df.resample('15T').asfreq()
    df = pd.concat([df, regular_intervall]).sort_index().interpolate()

    df['tooltip_datetime'] = df.index.map(
        lambda x: x.strftime("%H:%M - %d.%m.%Y"))

    print('Generating result')

    source = ColumnDataSource(df)

    plot = figure(sizing_mode='stretch_both', x_axis_type='datetime')

    create_line(source, plot, 'Download', 'red')
    create_line(source, plot, 'Upload', 'blue')
    create_line(source, plot, 'Ping', 'green')

    plot.xaxis.formatter = DatetimeTickFormatter(
        hours=["%H:%M"],
        days=["%d %B %Y"],
        months=["%B"],
        years=["%Y"],
    )
    plot.xaxis[0].ticker.desired_num_ticks = 15
    plot.yaxis.axis_label = "Mbit/s"
    plot.legend.click_policy = "hide"

    alpha = 0.15
    minimum = 2
    target = 3.8
    plot.add_layout(BoxAnnotation(top=minimum, fill_alpha=alpha, fill_color='red'))
    plot.add_layout(BoxAnnotation(bottom=minimum, top=target, fill_alpha=alpha, fill_color='yellow'))
    plot.add_layout(BoxAnnotation(bottom=target, fill_alpha=alpha, fill_color='green'))

    plot.add_tools(create_hover_tool("Download", "@download Mbit/s"))
    plot.add_tools(create_hover_tool("Upload", "@upload Mbit/s"))
    plot.add_tools(create_hover_tool("Ping", "@ping * 10^-2 s"))

    output_file('index.html')
    save(plot)


if __name__ == '__main__':
    main()
