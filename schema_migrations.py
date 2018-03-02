
def main():
    filename = 'speeds.csv'

    with open(filename, 'r') as f:
        lines = f.readlines()

    data = []
    for index, line in enumerate(lines):
        if index == 0:
            header = remove_server_url2_from_header(line)
            data.append(header)
        else:
            row = remove_server_url2_from_row(line, data[0])
            data.append(row)

    with open(filename, 'w+') as f:
        for d in data:
            line = ','.join(d)
            f.write(line)


def remove_server_url2_from_header(line):
    header = line.split(',')
    header = list(filter(lambda x: x != 'server_url2', header))
    return header


def remove_server_url2_from_row(line, header):
    row = line.split(',')
    if len(row) > len(header):
        del row[26]
    return row


if __name__ == '__main__':
    main()
