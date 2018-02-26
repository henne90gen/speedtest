import speedtest
import pandas as pd


def do_speed_test():
    s = speedtest.Speedtest()
    print("Looking for best server...")
    s.get_best_server()
    print("Testing download...")
    s.download()
    print("Testing upload...")
    s.upload()
    print("Getting results...")
    s.results.share()
    return s.results.dict()


def flatten(result):
    for key in result.copy():
        if type(result[key]) == dict:
            for other_key in result[key]:
                result[key + "_" + other_key] = result[key][other_key]
            del result[key]
    return result


def save_data_frame(df, filename):
    print("Saving to csv")
    df = df.reset_index()
    df['index'] = df.index
    df.index = df['index']
    df = df.drop(['index'], axis=1)
    df.to_csv(filename)


def main():
    filename = "speeds.csv"
    df = pd.read_csv(filename, index_col='index')

    for i in range(3):
        print("Starting test #" + str(i + 1))
        result = do_speed_test()
        result = flatten(result)
        result_df = pd.DataFrame.from_records([result])
        df = df.append(result_df)
        save_data_frame(df, filename)


if __name__ == '__main__':
    main()
