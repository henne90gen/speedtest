import os
import pickle
import speedtest
import urllib.request
from datetime import datetime

def do_speed_test(s: speedtest.Speedtest):
    print("Testing download...")
    s.download()
    print("Testing upload...")
    s.upload()
    print("Getting results...")
    s.results.share()
    return s.results.dict()


def flatten(result: str):
    for key in result.copy():
        if type(result[key]) == dict:
            for other_key in result[key]:
                result[key + "_" + other_key] = result[key][other_key]
            del result[key]
    return result


def sort_and_filter_result_keys(result):
    return filter(lambda x: 'server_url2' not in x, sorted(result.keys()))


def save_to_csv(result: dict, filename: str):
    if not os.path.isfile(filename):
        header = ""
        for key in sort_and_filter_result_keys(result):
            if len(header) == 0:
                header = key
            else:
                header = header + ',' + key

        with open(filename, 'w+') as f:
            f.write(header + '\n')

    print("Saving to csv...")
    line = ""
    for key in sort_and_filter_result_keys(result):
        if len(line) == 0:
            line = str(result[key])
        else:
            line = line + ',' + str(result[key])

    with open(filename, 'a') as f:
        f.write(line + '\n')


def download_image(url: str, index: int, image_dir: str):
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    image_name = str(index) + url.split("/")[-1]
    urllib.request.urlretrieve(url, os.path.join(image_dir, image_name))


def main():
    filename = "speeds.csv"
    image_dir = "images"

    print("Starting speedtest at", datetime.now())

    s = speedtest.Speedtest()
    print("Looking for best server...")
    s.get_best_server()

    results = []
    for i in range(3):
        print("Starting test #" + str(i + 1))
        result = do_speed_test(s)
        result = flatten(result)

        result['run'] = i
        results.append(result)

        # Reusing the Speedtest object causes the image url to be the same for each of the three runs
        download_image(result['share'], i, image_dir)

    result['download'] = sum(map(lambda r: r['download'], results)) / len(results)
    result['upload'] = sum(map(lambda r: r['upload'], results)) / len(results)
    result['ping'] = sum(map(lambda r: r['ping'], results)) / len(results)

    save_to_csv(result, filename)

if __name__ == '__main__':
    main()
